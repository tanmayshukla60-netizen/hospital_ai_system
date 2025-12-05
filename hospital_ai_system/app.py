import streamlit as st
from datetime import datetime

from core.orch_main import Orchestrator



# =========================================================
# GLOBAL PAGE CONFIG + FUTURISTIC THEME
# =========================================================
st.set_page_config(
    page_title="Hospital Multi-Agent AI System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_css():
    st.markdown(
        """
    <style>
    /* ---------- GLOBAL ---------- */
    .stApp {
        background:
          radial-gradient(circle at 0% 0%, #1b2351 0, transparent 55%),
          radial-gradient(circle at 100% 0%, #3d1048 0, transparent 55%),
          radial-gradient(circle at 20% 80%, #0d5846 0, transparent 60%),
          linear-gradient(135deg, #02030a 0%, #050817 45%, #02030b 100%);
        color: #f5f7ff;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", sans-serif;
    }
    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 1.4rem;
        padding-left: 2.6rem;
        padding-right: 2.6rem;
    }

    /* Hide default Streamlit menu/footer */
    #MainMenu, footer {visibility: hidden;}
    header {background: transparent;}

    /* ---------- SIDEBAR ---------- */
    section[data-testid="stSidebar"] {
        background: rgba(3, 6, 25, 0.98);
        border-right: 1px solid rgba(113, 160, 255, 0.45);
        box-shadow: 16px 0 45px rgba(0, 0, 0, 0.85);
        backdrop-filter: blur(22px);
    }
    .sidebar-brand {
        padding: 0.8rem 0.4rem 0.6rem 0.2rem;
        border-bottom: 1px solid rgba(120, 160, 255, 0.35);
        margin-bottom: 0.6rem;
    }
    .sidebar-brand-title {
        font-size: 1.05rem;
        font-weight: 650;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }
    .sidebar-badge {
        font-size: 0.65rem;
        padding: 0.1rem 0.5rem;
        border-radius: 999px;
        border: 1px solid rgba(137, 212, 255, 0.75);
        background: radial-gradient(circle at 0 0, rgba(40, 160, 255, 0.38), transparent 60%);
        color: #dff5ff;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }

    /* Radio buttons (navigation) */
    div[role="radiogroup"] > label {
        border-radius: 999px !important;
        border: 1px solid transparent !important;
        padding: 0.3rem 0.9rem !important;
        margin-bottom: 0.15rem !important;
        transition: all 0.13s ease-out !important;
        font-size: 0.86rem !important;
    }
    div[role="radiogroup"] > label:hover {
        background: rgba(73, 110, 255, 0.12) !important;
        border-color: rgba(117, 159, 255, 0.7) !important;
    }
    div[role="radiogroup"] > label[data-baseweb="radio"] > div:first-child {
        display: none !important; /* hide default dots */
    }
    div[role="radiogroup"] > label[aria-checked="true"] {
        background: radial-gradient(circle at 0 0, rgba(69, 200, 255, 0.6), rgba(40, 120, 255, 0.95)) !important;
        color: #020308 !important;
        box-shadow: 0 0 18px rgba(112, 199, 255, 0.85);
        border-color: transparent !important;
    }

    /* ---------- CARDS ---------- */
    .glass-card {
        background: linear-gradient(135deg, rgba(21, 27, 74, 0.96), rgba(8, 10, 35, 0.98));
        border-radius: 22px;
        padding: 1.6rem 1.9rem;
        border: 1px solid rgba(143, 180, 255, 0.45);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.88);
        backdrop-filter: blur(20px);
    }
    .glass-soft {
        background: linear-gradient(135deg, rgba(14, 18, 55, 0.96), rgba(6, 9, 30, 0.97));
        border-radius: 20px;
        padding: 1.0rem 1.2rem;
        border: 1px solid rgba(110, 145, 230, 0.5);
        box-shadow: 0 14px 40px rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(16px);
    }

    /* ---------- TYPOGRAPHY & ACCENTS ---------- */
    h1, h2, h3, h4 {
        font-weight: 650 !important;
        letter-spacing: 0.02em;
    }
    .accent {
        color: #81f3ff;
        text-shadow: 0 0 16px rgba(129, 243, 255, 0.9);
    }
    .accent-soft {
        color: #ff9fdc;
        text-shadow: 0 0 14px rgba(255, 159, 220, 0.8);
    }
    .subtle {
        opacity: 0.75;
        font-size: 0.85rem;
    }

    .chip {
        display: inline-flex;
        align-items: center;
        padding: 0.18rem 0.7rem;
        border-radius: 999px;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.09em;
        border: 1px solid rgba(123, 215, 255, 0.6);
        color: #caf3ff;
        background: rgba(5, 32, 60, 0.8);
        margin-right: 0.35rem;
        margin-bottom: 0.25rem;
    }
    .chip-pill {
        background: radial-gradient(circle at 0 0, rgba(255, 155, 214, 0.35), transparent 60%);
        border-color: rgba(255, 155, 214, 0.85);
        color: #ffe2f4;
    }

    .dot-live {
        display:inline-block;
        width:9px;
        height:9px;
        border-radius:50%;
        background:#32ff8f;
        box-shadow:0 0 14px rgba(50,255,143,0.9);
        margin-right:6px;
    }

    .metric-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        color: rgba(200, 209, 255, 0.78);
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: 680;
    }

    .stButton>button {
        background: radial-gradient(circle at top left, #54f8ff, #226eff);
        color: #02030a;
        border-radius: 999px;
        border: none;
        padding: 0.65rem 1.7rem;
        font-weight: 600;
        letter-spacing: 0.03em;
        box-shadow: 0 0 18px rgba(84, 213, 255, 0.95);
        transition: all 0.13s ease-out;
    }
    .stButton>button:hover {
        transform: translateY(-1px) scale(1.01);
        box-shadow: 0 0 28px rgba(150, 232, 255, 1);
    }

    /* Dataframe glass look */
    .dataframe {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid rgba(125, 162, 255, 0.7);
    }
    </style>
    """,
        unsafe_allow_html=True,
    )



load_css()


def render_header(title: str, subtitle: str = ""):
    col1, col2 = st.columns([0.74, 0.26])
    with col1:
        st.markdown(
            f"""
            <div class="glass-soft">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:1.2rem;">
                <div>
                  <div class="chip-pill" style="margin-bottom:0.35rem;">
                    🧠 SECURE MULTI-AGENT HOSPITAL ORCHESTRATOR
                  </div>
                  <div style="font-size:2.1rem;font-weight:720;margin-top:0.05rem;">
                    <span class="accent">⚕ {title}</span>
                  </div>
                  <div class="subtle" style="margin-top:0.35rem;">{subtitle}</div>
                </div>
                <div style="text-align:right;font-size:0.8rem;">
                  <div style="margin-bottom:0.25rem;">
                    <span class="dot-live"></span>
                    <span style="opacity:0.8;">Agents online</span>
                  </div>
                  <div class="metric-label" style="margin-bottom:0.1rem;">Session</div>
                  <div style="font-size:0.86rem;opacity:0.75;">
                    {datetime.now().strftime('%d %b %Y • %H:%M')}
                  </div>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="glass-soft" style="text-align:right;">
              <div class="metric-label">Privacy Mode</div>
              <div class="metric-value accent-soft">Zero PHI</div>
              <div style="font-size:0.75rem;opacity:0.68;margin-top:0.35rem;">
                Names & IDs are anonymized before LLM or agent handoff.
              </div>
              <div style="margin-top:0.55rem;">
                <span class="chip">RBAC</span>
                <span class="chip">Audit Trail</span>
                <span class="chip">Anomaly Guard</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# ORCHESTRATOR SESSION
# =========================================================
def get_orchestrator() -> Orchestrator:
    if "orchestrator" not in st.session_state:
        st.session_state["orchestrator"] = Orchestrator()
    return st.session_state["orchestrator"]


# =========================================================
# PAGES
# =========================================================
def page_reception_flow(orch: Orchestrator):
    render_header(
        "Reception – Automated Patient Flow",
        "From identity to visit, diagnosis, room allocation & PDF – fully orchestrated.",
    )
    st.markdown("<br/>", unsafe_allow_html=True)

    # Initialise session state keys
    defaults = {
        "reception_search_done": False,
        "reception_patient": None,
        "reception_error": None,
        "reception_name": "",
        "reception_phone": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    col_steps, col_main = st.columns([0.24, 0.76])

    # Left: pipeline view
    with col_steps:
        st.markdown(
            """
            <div class="glass-soft">
              <div class="metric-label">Flow Pipeline</div><br/>
              <div class="chip chip-pill">1 • Identity</div><br/>
              <div class="chip">2 • Visit Snapshot</div><br/>
              <div class="chip">3 • AI Diagnosis</div><br/>
              <div class="chip">4 • Room Assignment</div><br/>
              <div class="chip">5 • PDF & Billing</div><br/><br/>
              <div style="font-size:0.8rem;opacity:0.7;">
                Each step is a specialized agent with scoped access and full security logging.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_main:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Step 1 · Basic Identity (Name + Phone)")

        # STEP 1: search existing patient
        with st.form("reception_search_form"):
            name = st.text_input(
                "Patient Name", value=st.session_state["reception_name"]
            )
            phone = st.text_input(
                "Phone Number", value=st.session_state["reception_phone"]
            )
            search_submit = st.form_submit_button("Search / Identify Patient")

        if search_submit:
            st.session_state["reception_name"] = name.strip()
            st.session_state["reception_phone"] = phone.strip()

            patient, error = orch.find_patient(
                name=st.session_state["reception_name"],
                phone=st.session_state["reception_phone"],
            )
            st.session_state["reception_patient"] = patient
            st.session_state["reception_error"] = error
            st.session_state["reception_search_done"] = True

        # After search
        if st.session_state["reception_search_done"]:
            patient = st.session_state["reception_patient"]
            error = st.session_state["reception_error"]

            if error:
                st.error(error)
                st.markdown("</div>", unsafe_allow_html=True)
                return

            if patient:
                st.success(
                    f"Existing patient found – ID: {patient['id']} | Name: {patient['name']} | Phone: {patient['phone']}"
                )
                st.write(
                    f"Saved details – Age: {patient.get('age')}, Gender: {patient.get('gender')}, "
                    f"Height: {patient.get('height')}, Weight: {patient.get('weight')}"
                )
            else:
                st.info("New patient – please fill in details below.")

            st.markdown("---")
            st.subheader("Step 2 · Visit Details & Orchestration")

            # Pre-fill with saved data if existing
            if patient:
                default_age = patient.get("age") or 0
                default_gender = patient.get("gender") or ""
                default_height = patient.get("height") or 0.0
                default_weight = patient.get("weight") or 0.0
            else:
                default_age = 0
                default_gender = ""
                default_height = 0.0
                default_weight = 0.0

            with st.form("reception_visit_form"):
                c1, c2 = st.columns(2)
                with c1:
                    age = st.number_input(
                        "Age",
                        min_value=0,
                        max_value=120,
                        step=1,
                        value=int(default_age),
                        key="reception_age",
                    )
                    height = st.number_input(
                        "Height (cm)",
                        min_value=0.0,
                        step=0.1,
                        value=float(default_height),
                        key="reception_height",
                    )
                with c2:
                    gender = st.selectbox(
                        "Gender",
                        options=["", "Male", "Female", "Other"],
                        index=(
                            ["", "Male", "Female", "Other"].index(default_gender)
                            if default_gender in ["Male", "Female", "Other"]
                            else 0
                        ),
                        key="reception_gender",
                    )
                    weight = st.number_input(
                        "Weight (kg)",
                        min_value=0.0,
                        step=0.1,
                        value=float(default_weight),
                        key="reception_weight",
                    )

                symptoms = st.text_area(
                    "Current Symptoms",
                    key="reception_symptoms",
                )

                auto_assign_room = st.checkbox(
                    "Automatically assign room now", value=True
                )
                generate_pdf = st.checkbox(
                    "Generate visit PDF booklet", value=True
                )

                process_submit = st.form_submit_button(
                    "Process Visit (Register → Visit → Diagnosis → Room)"
                )

            if process_submit:
                if (
                    not st.session_state["reception_name"]
                    or not st.session_state["reception_phone"]
                ):
                    st.error("Name and phone are required.")
                    st.markdown("</div>", unsafe_allow_html=True)
                    return

                # 1) Register / update patient
                patient_id, err1 = orch.register_patient(
                    name=st.session_state["reception_name"],
                    phone=st.session_state["reception_phone"],
                    age=int(age) if age > 0 else None,
                    gender=gender if gender else None,
                    height=float(height) if height > 0 else None,
                    weight=float(weight) if weight > 0 else None,
                )
                if err1:
                    st.error(err1)
                    st.markdown("</div>", unsafe_allow_html=True)
                    return

                # 2) Create visit
                visit_id, err2 = orch.create_visit(
                    patient_id=patient_id,
                    age=int(age) if age > 0 else None,
                    gender=gender if gender else None,
                    height=float(height) if height > 0 else None,
                    weight=float(weight) if weight > 0 else None,
                    symptoms=symptoms,
                )
                if err2:
                    st.error(err2)
                    st.markdown("</div>", unsafe_allow_html=True)
                    return

                # 3) Run diagnosis
                visit_after_diag, err3 = orch.run_diagnosis_for_visit(visit_id)
                if err3:
                    st.error(err3)
                    st.markdown("</div>", unsafe_allow_html=True)
                    return

                st.success(f"Visit created with ID: {visit_id}")
                st.write("Diagnosis result:")
                st.write(
                    f"- Predicted Issues: {visit_after_diag.get('predicted_issues')}"
                )
                st.write(f"- Risk Level: {visit_after_diag.get('risk_level')}")

                # 4) Room assignment
                if auto_assign_room:
                    assigned_room_info, err4 = orch.assign_room(visit_id)
                    if err4:
                        st.warning(f"Room assignment issue: {err4}")
                    elif assigned_room_info:
                        room = assigned_room_info["room"]
                        st.success(
                            f"Assigned Room {room['room_number']} ({room.get('doctor_name', 'Doctor')})"
                        )

                # 5) PDF
                if generate_pdf:
                    pdf_path, err5 = orch.generate_visit_report_pdf(visit_id)
                    if err5:
                        st.warning(f"PDF generation issue: {err5}")
                    else:
                        try:
                            with open(pdf_path, "rb") as f:
                                pdf_bytes = f.read()

                            st.success("Visit summary PDF generated.")
                            st.download_button(
                                label="Download Visit PDF",
                                data=pdf_bytes,
                                file_name=f"visit_{visit_id}.pdf",
                                mime="application/pdf",
                            )
                        except FileNotFoundError:
                            st.warning(f"PDF file not found at: {pdf_path}")

        st.markdown("</div>", unsafe_allow_html=True)


def page_register_patient(orch: Orchestrator):
    render_header(
        "Register / Find Patient (Manual)",
        "Direct access to the patient registry agent.",
    )
    st.markdown("<br/>", unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    name = st.text_input("Name")
    phone = st.text_input("Phone Number")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    gender = st.selectbox("Gender", ["", "Male", "Female", "Other"])
    height = st.number_input("Height (cm)", min_value=0.0, step=0.1)
    weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1)

    if st.button("Register / Find"):
        if not name or not phone:
            st.error("Name and phone are required.")
        else:
            patient_id, error = orch.register_patient(
                name=name,
                phone=phone,
                age=int(age) if age > 0 else None,
                gender=gender if gender else None,
                height=float(height) if height > 0 else None,
                weight=float(weight) if weight > 0 else None,
            )
            if error:
                st.error(error)
            else:
                st.success(f"Patient ID: {patient_id}")

    st.markdown("</div>", unsafe_allow_html=True)


def page_create_visit_and_predict(orch: Orchestrator):
    render_header(
        "Create Visit & Run Diagnosis (Manual)",
        "Manual control path for debugging the diagnostic agent.",
    )
    st.markdown("<br/>", unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    patient_id_str = st.text_input("Patient ID")
    age = st.number_input("Visit Age (snapshot)", min_value=0, max_value=120, step=1)
    gender = st.selectbox("Visit Gender (snapshot)", ["", "Male", "Female", "Other"])
    height = st.number_input("Visit Height (cm)", min_value=0.0, step=0.1)
    weight = st.number_input("Visit Weight (kg)", min_value=0.0, step=0.1)
    symptoms = st.text_area("Symptoms")

    if st.button("Create Visit & Predict"):
        if not patient_id_str:
            st.error("Patient ID is required.")
        else:
            try:
                patient_id = int(patient_id_str)
            except ValueError:
                st.error("Patient ID must be a number.")
            else:
                visit_id, error = orch.create_visit(
                    patient_id=patient_id,
                    age=int(age) if age > 0 else None,
                    gender=gender if gender else None,
                    height=float(height) if height > 0 else None,
                    weight=float(weight) if weight > 0 else None,
                    symptoms=symptoms,
                )
                if error:
                    st.error(error)
                else:
                    st.success(f"Visit created with ID: {visit_id}")

                    visit, error2 = orch.run_diagnosis_for_visit(visit_id)
                    if error2:
                        st.error(error2)
                    elif visit:
                        st.subheader("Diagnosis Result")
                        st.write(f"Predicted Issues: {visit.get('predicted_issues')}")
                        st.write(f"Risk Level: {visit.get('risk_level')}")

    st.markdown("</div>", unsafe_allow_html=True)


def page_assign_room(orch: Orchestrator):
    render_header(
        "Assign Room (Manual)",
        "Human-in-the-loop control for the room allocation agent.",
    )
    st.markdown("<br/>", unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    visit_id_str = st.text_input("Visit ID")

    if st.button("Assign Room to Visit"):
        if not visit_id_str:
            st.error("Visit ID is required.")
        else:
            try:
                visit_id = int(visit_id_str)
            except ValueError:
                st.error("Visit ID must be a number.")
            else:
                result, error = orch.assign_room(visit_id)
                if error:
                    st.error(error)
                elif result:
                    room = result["room"]
                    visit = result["visit"]
                    st.success(
                        f"Assigned Room {room['room_number']} ({room['doctor_name']})"
                    )
                    st.write("Updated Visit:")
                    st.json(visit)

    st.markdown("</div>", unsafe_allow_html=True)


def page_generate_bill(orch: Orchestrator):
    render_header(
        "Generate Consultation Bill",
        "Billing agent with anomaly-checked, logged access.",
    )
    st.markdown("<br/>", unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    visit_id_str = st.text_input("Visit ID")
    consultation_fee = st.number_input("Consultation Fee", min_value=0.0, step=50.0)

    if st.button("Generate Bill"):
        if not visit_id_str:
            st.error("Visit ID is required.")
        else:
            try:
                visit_id = int(visit_id_str)
            except ValueError:
                st.error("Visit ID must be a number.")
            else:
                bill, error = orch.generate_bill(visit_id, consultation_fee)
                if error:
                    st.error(error)
                elif bill:
                    st.success(f"Bill ID: {bill['id']}")
                    st.write(f"Total Amount: ₹{bill['total_amount']}")
                    st.json(bill)

    st.markdown("</div>", unsafe_allow_html=True)


def page_security_logs(orch: Orchestrator):
    import pandas as pd

    render_header(
        "Security & Access Logs",
        "Central view of every agent action, denied request and anomaly.",
    )
    st.markdown("<br/>", unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    logs = orch.get_security_logs(limit=500)

    if not logs:
        st.info("No logs yet.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # Make sure we have a DataFrame
    df = pd.DataFrame(logs)

    # Normalize column names for easier lookup
    col_map = {c.lower(): c for c in df.columns}

    # Try to detect status / result column
    status_col = None
    for candidate in ["result", "status", "outcome", "action_result"]:
        if candidate in col_map:
            status_col = col_map[candidate]
            break

    # Try to detect agent column
    agent_col = None
    for candidate in ["agent", "agent_name", "source"]:
        if candidate in col_map:
            agent_col = col_map[candidate]
            break

    total_events = len(df)

    blocked_events = 0
    status_counts = None
    if status_col is not None:
        status_series = df[status_col].astype(str).str.upper()
        blocked_events = status_series.isin(["DENIED", "BLOCKED", "ERROR"]).sum()
        status_counts = status_series.value_counts().sort_index()

    unique_agents = df[agent_col].nunique() if agent_col is not None else None

    # --------- Top metrics row --------- #
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="metric-label">Total Events</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{total_events}</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="metric-label">Blocked / Denied</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="metric-value accent-soft">{blocked_events}</div>',
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown('<div class="metric-label">Unique Agents</div>', unsafe_allow_html=True)
        if unique_agents is not None:
            st.markdown(f'<div class="metric-value">{unique_agents}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="metric-value">–</div>', unsafe_allow_html=True)

    st.markdown("---")

    # --------- Status distribution chart --------- #
    if status_counts is not None and len(status_counts) > 0:
        st.subheader("Event distribution by status")
        chart_df = status_counts.reset_index()
        chart_df.columns = ["Status", "Count"]
        chart_df = chart_df.set_index("Status")
        st.bar_chart(chart_df)

    st.subheader("Raw security events")
    st.dataframe(df, use_container_width=True)

    st.markdown(
        """
        <br/>
        <div class="glass-soft">
            <span class="chip chip-pill">Zero-Trust</span>
            <span class="chip">RBAC</span>
            <span class="chip">Anomaly Rules</span>
            <span class="chip">Audit Trail</span>
            <p style="font-size:0.9rem;opacity:0.8;margin-top:0.5rem;">
                Every <strong>DENIED</strong> or <strong>BLOCKED</strong> event is a signal for
                intrusion detection – tagged with agent, action and policy reason.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)



# =========================================================
# MAIN
# =========================================================
# =========================================================
# MAIN
# =========================================================
def main():
    orch = get_orchestrator()

    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
              <div class="sidebar-brand-title">🏥 AURORA GENERAL</div>
              <div style="margin-top:0.25rem;">
                <span class="sidebar-badge">MULTI-AGENT · ZERO-TRUST</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Navigation radio INSIDE sidebar
        page = st.radio(
            "Go to",
            (
                "Reception (Auto Flow)",
                "Register Patient (Manual)",
                "Create Visit & Predict (Manual)",
                "Assign Room (Manual)",
                "Generate Bill",
                "Security Logs",
            ),
            label_visibility="collapsed",
        )

        st.markdown("---")

        # Admin tools INSIDE sidebar
        with st.expander("Admin Tools", expanded=False):
            if st.button("Reset all rooms to FREE"):
                orch.reset_all_rooms()
                st.success("All rooms have been reset to FREE.")

        st.markdown(
            """
            <small>
            <b>Security Mode:</b> Zero-trust · Agent-scoped access<br/>
            <b>Data Residency:</b> On-prem / VPC<br/>
            </small>
            """,
            unsafe_allow_html=True,
        )

    # Page routing (outside sidebar)
    if page == "Reception (Auto Flow)":
        page_reception_flow(orch)
    elif page == "Register Patient (Manual)":
        page_register_patient(orch)
    elif page == "Create Visit & Predict (Manual)":
        page_create_visit_and_predict(orch)
    elif page == "Assign Room (Manual)":
        page_assign_room(orch)
    elif page == "Generate Bill":
        page_generate_bill(orch)
    elif page == "Security Logs":
        page_security_logs(orch)


if __name__ == "__main__":
    main()

