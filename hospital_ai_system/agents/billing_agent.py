import json
from datetime import datetime
from typing import Dict, Any

from data.db import Database


class BillingAgent:
    def __init__(self, db: Database):
        self.db = db

    def generate_bill(self, visit_id: int, consultation_fee: float) -> Dict[str, Any]:
        items = [
            {"item": "Consultation Fee", "amount": float(consultation_fee)},
        ]
        total_amount = float(consultation_fee)
        created_at = datetime.utcnow().isoformat(timespec="seconds")

        bill_id = self.db.insert(
            """
            INSERT INTO bills (visit_id, total_amount, items_json, created_at)
            VALUES (?, ?, ?, ?);
            """,
            (visit_id, total_amount, json.dumps(items), created_at),
        )

        bill = self.db.execute(
            "SELECT * FROM bills WHERE id = ?;",
            (bill_id,),
            fetchone=True,
        )
        return bill
