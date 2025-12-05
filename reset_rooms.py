# reset_rooms.py
from data.db import Database

def main():
    db = Database()

    # Set every room to free and clear current patient
    db.execute(
        "UPDATE rooms SET status = 'free', current_patient_id = NULL;",
        (),
        commit=True,
    )

    print("✅ All rooms reset to FREE.")

if __name__ == "__main__":
    main()
