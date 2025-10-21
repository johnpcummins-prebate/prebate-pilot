
import streamlit as st
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, Image as RLImage

st.set_page_config(page_title="PreBate – Estate Readiness Pilot", page_icon="🧾", layout="centered")

# THEME
PRIMARY = "#10243D"
ACCENT = "#2E7BF6"
SUCCESS = "#16A34A"
WARNING = "#F59E0B"
DANGER  = "#DC2626"
MUTED   = "#475569"

# Global CSS for big buttons and readability
st.markdown(f"""
<style>
  .hero {{ text-align:center; }}
  .hero h1 {{ font-size: 2.2rem; margin: .25rem 0; color: {PRIMARY}; }}
  .hero p {{ color: #111827; max-width: 760px; margin: 0 auto; font-size: 1.05rem; }}
  .pill {{
    display:inline-block; padding: .35rem .75rem; border-radius:999px; font-weight:700; color:#fff;
  }}
  .pill-low {{ background:{SUCCESS}; }}
  .pill-mod {{ background:{WARNING}; }}
  .pill-high {{ background:{DANGER}; }}
  .question-text {{ font-size: 1.4rem; font-weight: 700; color: #0f172a; margin: .5rem 0 1rem; }}
</style>
""", unsafe_allow_html=True)

# Header (logo + intro)
st.image("assets/prebate_logo.png", use_container_width=True)
st.markdown("""
<div class="hero">
  <h1>PreBate – Estate Readiness Pilot</h1>
  <p>One question at a time. Large, clear options. Built to be simple and seniors‑friendly.</p>
  <hr/>
</div>
""", unsafe_allow_html=True)

# Define questions with optional conditions (skip logic)
QUESTIONS = [
    {"id":"q_country", "text":"Do you currently live in Ireland?", "type":"yn", "opts":["Yes","No"]},
    {"id":"q_partner", "text":"Are you married, in a civil partnership, or cohabiting?", "type":"yn", "opts":["Yes","No"]},
    {"id":"q_children", "text":"Do you have children or dependents?", "type":"yn", "opts":["Yes","No"]},
    {"id":"q_divorce", "text":"Have you ever been separated or divorced?", "type":"yn", "opts":["Yes","No"]},
    {"id":"q_property_sole", "text":"Do you own property in your sole name?", "type":"yn", "opts":["Yes","No"]},
    {"id":"q_property_coown", "text":"Do you co-own property with someone else?", "type":"yn", "opts":["Yes","No"]},
    {"id":"q_property_joint_tenants", "text":"If co-owned, is it owned as joint tenants (not tenants-in-common)?", "type":"yn", "opts":["Yes","No"], "show_if":{"q_property_coown":"Yes"}},
    {"id":"q_property_registered", "text":"Is your property registered with the Land Registry (has a folio number)?", "type":"ynm", "opts":["Yes","Not sure","No"]},
    {"id":"q_property_abroad", "text":"Do you own property outside Ireland?", "type":"yn", "opts":["Yes","No"]},
    {"id":"q_bank_sole", "text":"Do you hold any bank accounts in your sole name?", "type":"yn", "opts":["Yes","No"]},
    {"id":"q_caregiver_access", "text":"Does anyone other than you have access to your bank accounts or finances — even informally (family, friend, or carer)?", "type":"yn", "opts":["Yes","No"]},
    {"id":"q_caregiver_official", "text":"Is this person officially named (joint holder) or do they have an Enduring Power of Attorney?", "type":"yn", "opts":["Yes","No"], "show_if":{"q_caregiver_access":"Yes"}},
    {"id":"q_bank_joint", "text":"Do you have joint bank accounts?", "type":"yn", "opts":["Yes","No"]},
    {"id":"q_investments", "text":"Do you hold shares, bonds, or crypto in your own name?", "type":"yn", "opts":["Yes","No"]},
    {"id":"q_multiple_brokers", "text":"Do you hold savings/investments at multiple banks or brokers?", "type":"yn", "opts":["Yes","No"]},
    {"id":"q_life", "text":"Do you have life insurance?", "type":"yn", "opts":["Yes","No"]},
    {"id":"q_life_beneficiary", "text":"Have you named a beneficiary on your life policy?", "type":"yn", "opts":["Yes","No"], "show_if":{"q_life":"Yes"}},
    {"id":"q_pension", "text":"Do you have a private or occupational pension?", "type":"yn", "opts":["Yes","No"]},
    {"id":"q_pension_beneficiary", "text":"Have you filed a nomination of beneficiary for your pension?", "type":"yn", "opts":["Yes","No"], "show_if":{"q_pension":"Yes"}},
    {"id":"q_death_in_service", "text":"Do you have death-in-service benefits via your employer?", "type":"yn", "opts":["Yes","No"]},
    {"id":"q_will", "text":"Do you have a valid will?", "type":"yn", "opts":["Yes","No"]},
    {"id":"q_will_recent", "text":"Was your will updated within the last 3 years?", "type":"yn", "opts":["Yes","No"], "show_if":{"q_will":"Yes"}},
    {"id":"q_will_stored", "text":"Is your will securely stored and accessible?", "type":"yn", "opts":["Yes","No"]},
    {"id":"q_executor_informed", "text":"Does your executor know they are named in your will?", "type":"yn", "opts":["Yes","No"]},
    {"id":"q_lifetime_gifts", "text":"Have you made any lifetime gifts or set up any trusts?", "type":"yn", "opts":["Yes","No"]},
    {"id":"q_business", "text":"Do you own or co-own a business?", "type":"yn", "opts":["Yes","No"]},
    {"id":"q_farmland", "text":"Do you own farmland, forestry, or development land?", "type":"yn", "opts":["Yes","No"]},
    {"id":"q_digital", "text":"Do you have important digital assets (e.g., crypto wallets, domains, social/media accounts)?", "type":"yn", "opts":["Yes","No"]},
    {"id":"q_expect_inherit", "text":"Do you expect to inherit significant assets yourself in the near future?", "type":"yn", "opts":["Yes","No"]},
]

def cond_ok(q):
    rule = q.get("show_if")
    if not rule: return True
    for k,v in rule.items():
        if st.session_state.get("answers", {}).get(k) != v:
            return False
    return True

def next_index(idx):
    n = len(QUESTIONS)
    while idx < n and not cond_ok(QUESTIONS[idx]):
        idx += 1
    return idx

# Init session state
if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "completed" not in st.session_state:
    st.session_state.completed = False

# Ensure we're on a valid showable question
st.session_state.step = next_index(st.session_state.step)

# Progress
total_showable = sum(1 for q in QUESTIONS if cond_ok(q))
answered = sum(1 for q in QUESTIONS if cond_ok(q) and q["id"] in st.session_state.answers)
st.progress(int((answered/total_showable)*100) if total_showable else 0, text=f"{answered} of {total_showable} answered")

# Render current question or results
if st.session_state.step < len(QUESTIONS):
    q = QUESTIONS[st.session_state.step]
    st.markdown(f'<div class="question-text">{q["text"]}</div>', unsafe_allow_html=True)

    # Render big buttons
    if q["type"] == "ynm":
        cols = st.columns(3, gap="large")
        with cols[0]:
            if st.button("🟢 Yes", use_container_width=True):
                st.session_state.answers[q["id"]] = "Yes"
                st.session_state.step = next_index(st.session_state.step + 1)
                st.rerun()
        with cols[1]:
            if st.button("🟡 Not sure", use_container_width=True):
                st.session_state.answers[q["id"]] = "Not sure"
                st.session_state.step = next_index(st.session_state.step + 1)
                st.rerun()
        with cols[2]:
            if st.button("🔴 No", use_container_width=True):
                st.session_state.answers[q["id"]] = "No"
                st.session_state.step = next_index(st.session_state.step + 1)
                st.rerun()
    else:
        cols = st.columns(2, gap="large")
        with cols[0]:
            if st.button("🟢 Yes", use_container_width=True):
                st.session_state.answers[q["id"]] = "Yes"
                st.session_state.step = next_index(st.session_state.step + 1)
                st.rerun()
        with cols[1]:
            if st.button("🔴 No", use_container_width=True):
                st.session_state.answers[q["id"]] = "No"
                st.session_state.step = next_index(st.session_state.step + 1)
                st.rerun()

    # Back button
    back_col, _ = st.columns([1,4])
    with back_col:
        if st.button("← Back", use_container_width=True, help="Go to previous question"):
            i = st.session_state.step - 1
            while i >= 0 and (not cond_ok(QUESTIONS[i]) or QUESTIONS[i]["id"] not in st.session_state.answers):
                i -= 1
            if i >= 0:
                st.session_state.step = i
            st.rerun()

else:
    st.session_state.completed = True

# RESULTS
if st.session_state.completed:
    a = st.session_state.answers
    probate_risk = 0
    dispute_risk = 0
    actions = []

    def add(x):
        if x not in actions: actions.append(x)

    # Personal
    if a.get("q_country") == "No":
        add("Laws vary outside Ireland—ensure local estate planning aligned to your jurisdiction.")
    if a.get("q_partner") == "No":
        probate_risk += 1; add("If single, ensure you have a valid will to direct assets clearly.")
    if a.get("q_children") == "Yes":
        add("Add guardianship and inheritance clauses for dependents in your will.")
    if a.get("q_divorce") == "Yes":
        probate_risk += 1; add("Review titles and beneficiaries after separation/divorce.")

    # Property
    if a.get("q_property_sole") == "Yes":
        probate_risk += 2; add("Consider adding a joint owner (joint tenants), using a trust, or updating your will for solely-owned property.")
    if a.get("q_property_coown") == "Yes" and a.get("q_property_joint_tenants") == "No":
        probate_risk += 1; add("Convert co-owned property to joint tenancy where appropriate to enable automatic survivorship.")
    if a.get("q_property_registered") in ["No", "Not sure"]:
        probate_risk += 1; add("Register any unregistered property with the Land Registry (get a folio number).")
    if a.get("q_property_abroad") == "Yes":
        probate_risk += 1; add("Create a local will or plan for assets held outside Ireland.")

    # Banking & caregiver
    if a.get("q_bank_sole") == "Yes":
        probate_risk += 1; add("For sole accounts, consider joint holder or pay-on-death nomination (if available).")
    if a.get("q_caregiver_access") == "Yes":
        if a.get("q_caregiver_official") == "Yes":
            dispute_risk += 1; add("Document the intent of caregiver/joint access (assistance vs inheritance) in writing with your solicitor.")
        else:
            dispute_risk += 2; probate_risk += 1
            add("Revoke informal access (shared cards/PINs). Establish an Enduring Power of Attorney (EPA) if help is needed.")
            add("Keep a simple log of legitimate expenses paid by helpers on your behalf.")
    if a.get("q_bank_joint") == "No":
        add("Consider a joint account for shared household expenses to ease continuity for a partner.")
    if a.get("q_investments") == "Yes":
        probate_risk += 1; add("Hold investments via nominee accounts or trusts to simplify transfer.")
    if a.get("q_multiple_brokers") == "Yes":
        add("Consolidate accounts to reduce admin burden on your executor.")

    # Insurance & pensions
    if a.get("q_life") == "Yes" and a.get("q_life_beneficiary") == "No":
        probate_risk += 1; add("Add a named beneficiary to life insurance so it bypasses probate.")
    if a.get("q_pension") == "Yes" and a.get("q_pension_beneficiary") == "No":
        probate_risk += 1; add("File a pension beneficiary nomination with your provider.")
    if a.get("q_death_in_service") == "Yes":
        add("Confirm your employer nomination for death-in-service benefits.")

    # Will & planning
    if a.get("q_will") == "No":
        probate_risk += 2; add("Create a valid will—without one, intestacy rules apply.")
    if a.get("q_will") == "Yes" and a.get("q_will_recent") == "No":
        probate_risk += 1; add("Review/update your will (aim every 3 years or upon life changes).")
    if a.get("q_will_stored") == "No":
        add("Store your will with your solicitor or register a copy with the Probate Office.")
    if a.get("q_executor_informed") == "No":
        add("Inform your executor that they are named and where documents are kept.")
    if a.get("q_lifetime_gifts") == "Yes":
        add("Have a solicitor review documentation for lifetime gifts/trusts.")

    # Special assets
    if a.get("q_business") == "Yes":
        probate_risk += 1; add("Create a succession/shareholder plan for your business interests.")
    if a.get("q_farmland") == "Yes":
        add("Explore Agricultural or Business Relief to optimize tax and transfer.")
    if a.get("q_digital") == "Yes":
        add("Document a digital asset plan (locations, instructions, and access).")
    if a.get("q_expect_inherit") == "Yes":
        add("Coordinate your plan if you expect to inherit—timing/structure can reduce complexity.")

    # Labels
    def label(score, thresholds=(2,4)):
        if score <= thresholds[0]: return "Low"
        elif score <= thresholds[1]: return "Moderate"
        else: return "High"

    probate_label = label(probate_risk)
    dispute_label = "Low" if dispute_risk == 0 else ("Elevated" if dispute_risk == 1 else "Critical")
    pill_p = "pill-low" if probate_label=="Low" else ("pill-mod" if probate_label=="Moderate" else "pill-high")
    pill_d = "pill-low" if dispute_label=="Low" else ("pill-mod" if dispute_label=="Elevated" else "pill-high")

    st.markdown(f'<div style="text-align:center;margin-top:12px;"><span class="pill {pill_p}">Probate: {probate_label}</span> &nbsp; <span class="pill {pill_d}">Dispute: {dispute_label}</span></div>', unsafe_allow_html=True)
    st.markdown("### Recommended Actions")
    for i, act in enumerate(actions, start=1):
        st.markdown(f"{i}. {act}")

    # PDF
    def build_pdf():
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="TitlePB", fontSize=18, leading=22, textColor=colors.HexColor(PRIMARY), spaceAfter=12))
        styles.add(ParagraphStyle(name="H2PB", fontSize=13, leading=16, textColor=colors.HexColor(PRIMARY), spaceAfter=6))
        styles.add(ParagraphStyle(name="BodyPB", fontSize=11, leading=16, textColor=colors.HexColor("#111827")))
        story = []
        try:
            story.append(RLImage("assets/prebate_logo.png", width=220, height=66))
        except Exception:
            pass
        story.append(Paragraph("PreBate – Estate Readiness Report", styles["TitlePB"]))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["BodyPB"]))
        story.append(Spacer(1, 8))
        story.append(Paragraph(f"<b>Probate Risk:</b> {probate_label} (score {probate_risk})", styles["BodyPB"]))
        story.append(Paragraph(f"<b>Dispute Risk:</b> {dispute_label} (score {dispute_risk})", styles["BodyPB"]))
        story.append(Spacer(1, 10))
        story.append(Paragraph("Recommended Actions", styles["H2PB"]))
        if actions:
            items = [ListItem(Paragraph(x, styles["BodyPB"])) for x in actions]
            story.append(ListFlowable(items, bulletType='1', start='1'))
        else:
            story.append(Paragraph("No immediate actions detected.", styles["BodyPB"]))
        story.append(Spacer(1, 18))
        story.append(Paragraph('<font color="#6B7280">This report is for educational purposes and does not constitute legal advice. Consult a solicitor for personalized guidance.</font>', styles["BodyPB"]))
        doc.build(story)
        pdf = buffer.getvalue()
        buffer.close()
        return pdf

    pdf_bytes = build_pdf()
    st.download_button("Download Report (PDF)", data=pdf_bytes, file_name="prebate_report.pdf", mime="application/pdf")

    if st.button("Start Over"):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.session_state.completed = False
        st.rerun()
