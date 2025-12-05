from typing import Optional, Dict, Any

from data.db import Database


class RoomAgent:
    def __init__(self, db: Database):
        self.db = db

    def assign_room(self, patient_id: int, visit_id: int) -> Optional[Dict[str, Any]]:
        """
        Find the first free room, mark it occupied for this patient,
        and record the room on the visit row.

        Returns the room dict if assigned, or None if no free room.
        """

        # 1) Find first free room
        room = self.db.execute(
            "SELECT * FROM rooms WHERE status = 'free' ORDER BY id LIMIT 1;",
            (),
            fetchone=True,
        )
        if not room:
            # No room currently available
            return None

        # 2) Mark room as occupied and attach patient
        self.db.execute(
            """
            UPDATE rooms
            SET status = 'occupied',
                current_patient_id = ?
            WHERE id = ?;
            """,
            (patient_id, room["id"]),
            commit=True,
        )

        # 3) Store which room this visit is using
        #    (so that we can free it later in free_room_for_visit)
        self.db.execute(
            """
            UPDATE visits
            SET allocated_room = ?
            WHERE id = ?;
            """,
            (room["room_number"], visit_id),
            commit=True,
        )

        return room

    def free_room_for_visit(self, visit: Dict[str, Any]) -> None:
        """
        Free the room associated with this visit.

        Expects `visit` to contain an `allocated_room` field.
        If it's missing / empty, this does nothing.
        """
        room_number = visit.get("allocated_room")
        if not room_number:
            # No room stored on visit – nothing to free
            return

        # Free the room associated with this visit
        self.db.execute(
            """
            UPDATE rooms
            SET status = 'free',
                current_patient_id = NULL
            WHERE room_number = ?;
            """,
            (room_number,),
            commit=True,
        )
