import os
from pathlib import Path

# This will create the project inside the SAME folder as this script
BASE_DIR = Path(__file__).parent / "hospital_ai_system"

# Folders to create inside hospital_ai_system
DIRS = [
    "core",
    "agents",
    "data",
    "reports",
    "logs",
    "tests",
]

# Files to create (path is relative to hospital_ai_system)
FILES = {
    "app.py": "",
    "config.py": "",
    "requirements.txt": "",
    "README.md": "# Hospital AI System\n",
    "core/__init__.py": "",
    "core/orchestrator.py": "",
    "core/models.py": "",
    "agents/__init__.py": "",
    "agents/intake_agent.py": "",
    "agents/records_agent.py": "",
    "agents/diagnosis_agent.py": "",
    "agents/room_agent.py": "",
    "agents/billing_agent.py": "",
    "agents/security_agent.py": "",
    "data/__init__.py": "",
    "data/db.py": "",
    "data/schema.sql": "",
    "data/seed_data.py": "",
    "reports/__init__.py": "",
    "reports/pdf_generator.py": "",
    "logs/.gitkeep": "",
    "tests/__init__.py": "",
    "tests/test_basic_flow.py": "",
}

def create_project_structure():
    print(f"Creating project at: {BASE_DIR}")

    # Create base directory
    BASE_DIR.mkdir(exist_ok=True)

    # Create subdirectories
    for d in DIRS:
        dir_path = BASE_DIR / d
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  [DIR ] {dir_path}")

    # Create files
    for rel_path, content in FILES.items():
        file_path = BASE_DIR / rel_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  [FILE] {file_path}")

    print("\nDone! 🎉")

if __name__ == "__main__":
    create_project_structure()
