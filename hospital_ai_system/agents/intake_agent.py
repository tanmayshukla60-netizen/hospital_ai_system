from typing import Optional, Dict, Any

from data.db import Database


class IntakeAgent:
    def __init__(self, db: Database):
        self.db = db

    def register_or_get_patient(
        self,
        name: str,
        phone: str,
        age: Optional[int] = None,
        gender: Optional[str] = None,
        height: Optional[float] = None,
        weight: Optional[float] = None,
    ) -> int:
        # Check if patient already exists by phone
        existing = self.db.execute(
            "SELECT * FROM patients WHERE phone = ?;",
            (phone,),
            fetchone=True,
        )
        if existing:
            # Optionally update demographics if provided
            patient_id = existing["id"]
            self.db.execute(
                """
                UPDATE patients
                SET name = COALESCE(?, name),
                    age = COALESCE(?, age),
                    gender = COALESCE(?, gender),
                    height = COALESCE(?, height),
                    weight = COALESCE(?, weight)
                WHERE id = ?;
                """,
                (name, age, gender, height, weight, patient_id),
                commit=True,
            )
            return patient_id

        # Insert new patient
        patient_id = self.db.insert(
            """
            INSERT INTO patients (name, phone, age, gender, height, weight)
            VALUES (?, ?, ?, ?, ?, ?);
            """,
            (name, phone, age, gender, height, weight),
        )
        return patient_id
