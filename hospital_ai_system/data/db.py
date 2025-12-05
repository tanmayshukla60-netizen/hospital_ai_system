import sqlite3
from pathlib import Path
from typing import Any, Iterable, List, Optional, Dict

from config import DB_PATH, DEFAULT_ROOMS


class Database:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._ensure_db_dir()
        self._init_db()
        self._seed_rooms_if_empty()

    def _ensure_db_dir(self):
        # DB in current directory – ensure path is valid
        db_file = Path(self.db_path)
        if db_file.parent and not db_file.parent.exists():
            db_file.parent.mkdir(parents=True, exist_ok=True)

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cur = conn.cursor()

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL UNIQUE,
                    age INTEGER,
                    gender TEXT,
                    height REAL,
                    weight REAL
                );
                """
            )

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS visits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER NOT NULL,
                    symptoms TEXT,
                    age INTEGER,
                    gender TEXT,
                    height REAL,
                    weight REAL,
                    predicted_issues TEXT,
                    risk_level TEXT,
                    allocated_room TEXT,
                    status TEXT,
                    FOREIGN KEY(patient_id) REFERENCES patients(id)
                );
                """
            )

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS rooms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    room_number TEXT NOT NULL UNIQUE,
                    doctor_name TEXT,
                    status TEXT,
                    current_patient_id INTEGER
                );
                """
            )

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS bills (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    visit_id INTEGER NOT NULL,
                    total_amount REAL,
                    items_json TEXT,
                    created_at TEXT,
                    FOREIGN KEY(visit_id) REFERENCES visits(id)
                );
                """
            )

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS access_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    agent_name TEXT NOT NULL,
                    action TEXT NOT NULL,
                    resource_type TEXT,
                    resource_id TEXT,
                    status TEXT NOT NULL,
                    notes TEXT
                );
                """
            )

            conn.commit()

    def _seed_rooms_if_empty(self):
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) as cnt FROM rooms;")
            row = cur.fetchone()
            if row["cnt"] == 0:
                for room in DEFAULT_ROOMS:
                    cur.execute(
                        "INSERT INTO rooms (room_number, doctor_name, status, current_patient_id) "
                        "VALUES (?, ?, 'free', NULL);",
                        (room["room_number"], room["doctor_name"]),
                    )
                conn.commit()

    def execute(
        self,
        query: str,
        params: Iterable[Any] = (),
        *,
        fetchone: bool = False,
        fetchall: bool = False,
        commit: bool = False,
    ) -> Optional[Any]:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute(query, tuple(params))
            result = None
            if fetchone:
                row = cur.fetchone()
                result = dict(row) if row is not None else None
            elif fetchall:
                rows = cur.fetchall()
                result = [dict(r) for r in rows]
            if commit:
                conn.commit()
            return result

    def insert(self, query: str, params: Iterable[Any] = ()) -> int:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute(query, tuple(params))
            conn.commit()
            return cur.lastrowid
