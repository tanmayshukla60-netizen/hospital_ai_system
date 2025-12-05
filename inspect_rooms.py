# inspect_rooms.py
from data.db import Database

def main():
    db = Database()

    rows = db.execute(
        "SELECT id, room_number, doctor_name, status, current_patient_id FROM rooms;",
        (),
        fetchall=True,
    )

    print("----- ROOMS TABLE -----")
    print("Total rows:", len(rows))
    for r in rows:
        print(
            f"ID={r['id']}, room_number={r['room_number']}, "
            f"doctor={r['doctor_name']}, status={r['status']}, "
            f"current_patient_id={r['current_patient_id']}"
        )

if __name__ == '__main__':
    main()
