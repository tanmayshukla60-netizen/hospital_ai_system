from datetime import datetime
from typing import Dict, Set, List, Any, Optional

from data.db import Database


class SecurityAgent:
    """
    Handles permissions + access logging + unauthorized detection.
    """

    def __init__(self, db: Database):
        self.db = db
        # Define allowed actions per agent
        self.permissions: Dict[str, Set[str]] = {
            "IntakeAgent": {"identity_read", "identity_write", "create_visit"},
            "RecordsAgent": {"patient_read", "visit_read", "visit_write"},
            "DiagnosisAgent": {"visit_read_anonymized"},
            "RoomAgent": {"room_read", "room_write"},
            "BillingAgent": {"billing_create", "billing_read", "visit_basic_read"},
            "SecurityAgent": {"logs_read"},
        }

    def check_permission(
        self,
        agent_name: str,
        action: str,
        resource_type: Optional[str],
        resource_id: Optional[str],
        notes: str = "",
    ) -> bool:
        allowed_actions = self.permissions.get(agent_name, set())
        is_allowed = action in allowed_actions

        status = "ALLOWED" if is_allowed else "DENIED"
        timestamp = datetime.utcnow().isoformat(timespec="seconds")

        self.db.insert(
            """
            INSERT INTO access_logs
            (timestamp, agent_name, action, resource_type, resource_id, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """,
            (timestamp, agent_name, action, resource_type, str(resource_id) if resource_id else None, status, notes),
        )

        return is_allowed

    def get_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        return self.db.execute(
            """
            SELECT * FROM access_logs
            ORDER BY id DESC
            LIMIT ?;
            """,
            (limit,),
            fetchall=True,
        )
