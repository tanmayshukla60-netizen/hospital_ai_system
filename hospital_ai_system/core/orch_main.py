from typing import Optional, Tuple, Dict, Any

from data.db import Database
from agents.intake_agent import IntakeAgent
from agents.records_agent import RecordsAgent
from agents.diagnosis_agent import DiagnosisAgent
from agents.room_agent import RoomAgent
from agents.billing_agent import BillingAgent
from agents.security_agent import SecurityAgent

# Try to import PDF generator if available
try:
    from reports.pdf_generator import generate_visit_pdf  # type: ignore
except ImportError:
    generate_visit_pdf = None


class Orchestrator:
    def __init__(self):
        # You can keep these prints while debugging if you like
        # print("ORCH_MAIN: Orchestrator __init__")
        self.db = Database()
        self.security = SecurityAgent(self.db)
        self.intake = IntakeAgent(self.db)
        self.records = RecordsAgent(self.db)
        self.diagnosis = DiagnosisAgent()
        self.room_agent = RoomAgent(self.db)
        self.billing = BillingAgent(self.db)

    # ---------- Patient lookup ----------

    def find_patient(
        self, name: str, phone: str
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Receptionist first step: check if patient already exists.
        """
        if not self.security.check_permission(
            "IntakeAgent", "identity_read", "patient", None, "find_patient"
        ):
            return None, "Permission denied for IntakeAgent identity_read"

        patient = self.records.find_patient_by_phone_or_name(phone=phone, name=name)
        return patient, None

    # ---------- Patient & Visit ----------

    def register_patient(
        self,
        name: str,
        phone: str,
        age: Optional[int],
        gender: Optional[str],
        height: Optional[float],
        weight: Optional[float],
    ) -> Tuple[Optional[int], Optional[str]]:
        if not self.security.check_permission(
            "IntakeAgent", "identity_write", "patient", None, "register_or_get_patient"
        ):
            return None, "Permission denied for IntakeAgent identity_write"

        patient_id = self.intake.register_or_get_patient(
            name=name,
            phone=phone,
            age=age,
            gender=gender,
            height=height,
            weight=weight,
        )
        return patient_id, None

    def create_visit(
        self,
        patient_id: int,
        age: Optional[int],
        gender: Optional[str],
        height: Optional[float],
        weight: Optional[float],
        symptoms: str,
    ) -> Tuple[Optional[int], Optional[str]]:
        if not self.security.check_permission(
            "IntakeAgent", "create_visit", "visit", None, "create_visit"
        ):
            return None, "Permission denied for IntakeAgent create_visit"

        visit_id = self.records.create_visit(
            patient_id=patient_id,
            age=age,
            gender=gender,
            height=height,
            weight=weight,
            symptoms=symptoms,
        )
        return visit_id, None

    def run_diagnosis_for_visit(
        self, visit_id: int
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        visit = self.records.get_visit(visit_id)
        if not visit:
            return None, "Visit not found"

        # Only anonymized clinical data goes to DiagnosisAgent
        if not self.security.check_permission(
            "DiagnosisAgent",
            "visit_read_anonymized",
            "visit",
            str(visit_id),
            "predict_issues",
        ):
            return None, "Permission denied for DiagnosisAgent visit_read_anonymized"

        age = visit.get("age") or 0
        gender = visit.get("gender") or ""
        height = visit.get("height") or 0.0
        weight = visit.get("weight") or 0.0
        symptoms = visit.get("symptoms") or ""

        predicted_issues, risk_level = self.diagnosis.predict(
            symptoms=symptoms,
            age=int(age) if age is not None else 0,
            gender=str(gender),
            height=float(height) if height is not None else 0.0,
            weight=float(weight) if weight is not None else 0.0,
        )

        self.records.update_visit_prediction(visit_id, predicted_issues, risk_level)
        updated = self.records.get_visit(visit_id)
        return updated, None

    # ---------- Room Allocation ----------

    def assign_room(
        self, visit_id: int
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        visit = self.records.get_visit(visit_id)
        if not visit:
            return None, "Visit not found"

        if not self.security.check_permission(
            "RoomAgent", "room_read", "room", None, "assign_room"
        ):
            return None, "Permission denied for RoomAgent room_read"

        if not self.security.check_permission(
            "RoomAgent", "room_write", "room", None, "assign_room"
        ):
            return None, "Permission denied for RoomAgent room_write"

        patient_id = visit["patient_id"]
        room = self.room_agent.assign_room(patient_id=patient_id, visit_id=visit_id)
        if not room:
            return None, "No free rooms available"

        self.records.update_visit_room(visit_id, room["room_number"])
        updated_visit = self.records.get_visit(visit_id)
        return {"room": room, "visit": updated_visit}, None

    def complete_visit(self, visit_id: int) -> Optional[str]:
        visit = self.records.get_visit(visit_id)
        if not visit:
            return "Visit not found"
        self.room_agent.free_room_for_visit(visit)
        self.records.set_visit_status(visit_id, "completed")
        return None

    # ---------- Billing ----------

    def generate_bill(
        self, visit_id: int, consultation_fee: float
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Generate a bill for this visit.
        When billing is successful, free the room used by this visit
        and mark the visit as completed.
        """
        visit = self.records.get_visit(visit_id)
        if not visit:
            return None, "Visit not found"

        if not self.security.check_permission(
            "BillingAgent", "billing_create", "bill", None, "generate_bill"
        ):
            return None, "Permission denied for BillingAgent billing_create"

        # 1) Create the bill
        bill = self.billing.generate_bill(visit_id, consultation_fee)

        # 2) Free the room associated with this visit (if any)
        self.room_agent.free_room_for_visit(visit)

        # 3) Mark visit as completed
        self.records.set_visit_status(visit_id, "completed")

        return bill, None

    # ---------- Reports ----------

    def generate_visit_report_pdf(
        self, visit_id: int
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Generate a visit PDF if the PDF generator is available.
        Otherwise return a friendly error message.
        """
        visit_with_patient = self.records.get_visit_with_patient(visit_id)
        if not visit_with_patient:
            return None, "Visit not found"

        if generate_visit_pdf is None:
            return None, "PDF generation module not configured."

        pdf_path = generate_visit_pdf(visit_with_patient)
        return pdf_path, None

    # ---------- Security Logs & Admin ----------

    def get_security_logs(self, limit: int = 100):
        return self.security.get_logs(limit=limit)

    def reset_all_rooms(self) -> None:
        """
        Admin / demo helper:
        Mark every room as FREE and clear current_patient_id.
        Does NOT create or delete any rooms.
        """
        self.db.execute(
            "UPDATE rooms SET status = 'free', current_patient_id = NULL;",
            (),
            commit=True,
        )
