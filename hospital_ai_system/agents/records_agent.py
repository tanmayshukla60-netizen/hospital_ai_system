from typing import Optional, Dict, Any, List

from data.db import Database


class RecordsAgent:
    def __init__(self, db: Database):
        self.db = db

    # -------- Patient helpers --------

    def find_patient_by_phone_or_name(
        self, phone: Optional[str], name: Optional[str]
    ) -> Optional[Dict[str, Any]]:
        """
        Try to find a patient first by phone, then by exact name.
        Returns a dict row or None.
        """
        phone = (phone or "").strip()
        name = (name or "").strip()

        if phone:
            row = self.db.execute(
                "SELECT * FROM patients WHERE phone = ? LIMIT 1;",
                (phone,),
                fetchone=True,
            )
            if row:
                return row

        if name:
            row = self.db.execute(
                "SELECT * FROM patients WHERE name = ? ORDER BY id DESC LIMIT 1;",
                (name,),
                fetchone=True,
            )
            if row:
                return row

        return None

    def list_patients(self) -> List[Dict[str, Any]]:
        return self.db.execute(
            "SELECT * FROM patients ORDER BY id DESC;",
            (),
            fetchall=True,
        )

    def get_patient(self, patient_id: int) -> Optional[Dict[str, Any]]:
        return self.db.execute(
            "SELECT * FROM patients WHERE id = ?;",
            (patient_id,),
            fetchone=True,
        )

    # -------- Visit helpers --------

    def create_visit(
        self,
        patient_id: int,
        age: Optional[int],
        gender: Optional[str],
        height: Optional[float],
        weight: Optional[float],
        symptoms: str,
    ) -> int:
        visit_id = self.db.insert(
            """
            INSERT INTO visits (
                patient_id, symptoms, age, gender, height, weight,
                predicted_issues, risk_level, allocated_room, status
            )
            VALUES (?, ?, ?, ?, ?, ?, NULL, NULL, NULL, 'ongoing');
            """,
            (patient_id, symptoms, age, gender, height, weight),
        )
        return visit_id

    def update_visit_prediction(
        self,
        visit_id: int,
        predicted_issues: str,
        risk_level: str,
    ) -> None:
        self.db.execute(
            """
            UPDATE visits
            SET predicted_issues = ?, risk_level = ?
            WHERE id = ?;
            """,
            (predicted_issues, risk_level, visit_id),
            commit=True,
        )

    def update_visit_room(self, visit_id: int, room_number: str) -> None:
        self.db.execute(
            """
            UPDATE visits
            SET allocated_room = ?
            WHERE id = ?;
            """,
            (room_number, visit_id),
            commit=True,
        )

    def set_visit_status(self, visit_id: int, status: str) -> None:
        self.db.execute(
            "UPDATE visits SET status = ? WHERE id = ?;",
            (status, visit_id),
            commit=True,
        )

    def get_visit(self, visit_id: int) -> Optional[Dict[str, Any]]:
        return self.db.execute(
            "SELECT * FROM visits WHERE id = ?;",
            (visit_id,),
            fetchone=True,
        )

    def get_visit_with_patient(self, visit_id: int) -> Optional[Dict[str, Any]]:
        return self.db.execute(
            """
            SELECT
                v.*,
                p.name AS patient_name,
                p.phone AS patient_phone,
                p.age AS patient_age,
                p.gender AS patient_gender
            FROM visits v
            JOIN patients p ON v.patient_id = p.id
            WHERE v.id = ?;
            """,
            (visit_id,),
            fetchone=True,
        )
