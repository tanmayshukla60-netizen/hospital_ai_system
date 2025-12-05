from pathlib import Path
from typing import Dict, Any

from fpdf import FPDF


def generate_visit_pdf(visit_with_patient: Dict[str, Any], output_dir: str = "reports/generated") -> str:
    """
    Generate a simple PDF booklet for a visit.
    Returns the path to the generated PDF file.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    visit_id = visit_with_patient["id"]
    patient_name = visit_with_patient.get("patient_name", "Unknown")
    patient_phone = visit_with_patient.get("patient_phone", "Unknown")
    symptoms = visit_with_patient.get("symptoms", "")
    predicted_issues = visit_with_patient.get("predicted_issues", "")
    risk_level = visit_with_patient.get("risk_level", "")
    allocated_room = visit_with_patient.get("allocated_room", "")
    status = visit_with_patient.get("status", "")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Hospital Visit Summary", ln=True, align="C")

    pdf.ln(5)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Visit ID: {visit_id}", ln=True)
    pdf.cell(0, 8, f"Patient: {patient_name}", ln=True)
    pdf.cell(0, 8, f"Phone: {patient_phone}", ln=True)
    pdf.ln(3)

    pdf.cell(0, 8, f"Status: {status}", ln=True)
    pdf.cell(0, 8, f"Allocated Room: {allocated_room}", ln=True)
    pdf.ln(3)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Symptoms:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 6, symptoms or "N/A")
    pdf.ln(3)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Predicted Issues:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 6, predicted_issues or "N/A")
    pdf.ln(3)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Risk Level:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, risk_level or "N/A", ln=True)

    pdf_path = Path(output_dir) / f"visit_{visit_id}.pdf"
    pdf.output(str(pdf_path))

    return str(pdf_path)
