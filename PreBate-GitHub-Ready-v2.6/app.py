
import streamlit as st
from datetime import datetime
from io import BytesIO
from pathlib import Path
import base64

st.set_page_config(
    page_title="PreBate – Estate Readiness",
    page_icon="🧾",
    layout="centered",
    initial_sidebar_state="collapsed",
)

def first_existing(paths):
    for p in paths:
        try:
            if p.exists():
                return p
        except Exception:
            continue
    return None

APP_DIR = Path(__file__).parent.resolve()
CANDIDATES = [
    APP_DIR / "assets" / "prebate_logo.png",
    Path.cwd() / "assets" / "prebate_logo.png",
    APP_DIR.parent / "assets" / "prebate_logo.png",
    Path("/mount/src/prebate-pilot/assets/prebate_logo.png"),
]
LOGO_PATH = first_existing(CANDIDATES)

def logo_html_base64(path: Path) -> str:
    try:
        b64 = base64.b64encode(path.read_bytes()).decode("ascii")
        return f"""
        <div class="logo-wrap">
          <img class="logo" alt="PreBate" src="data:image/png;base64,{b64}" />
        </div>
        """
    except Exception:
        return """
        <div class="logo-fallback">
          <div class="brand">PreBate</div>
          <div class="tag">Estate Readiness</div>
        </div>
        """

st.markdown("""
<style>
  .block-container { padding-top: 1rem; padding-bottom: 2rem; }
  .logo-wrap { display:flex; justify-content:center; margin: .5rem 0 0.5rem; }
  .logo { width: 100%; max-width: 680px; height: auto; display:block; }
  .logo-fallback { text-align:center; margin:.5rem 0 .5rem; }
  .logo-fallback .brand { font-weight:800; font-size:1.6rem; color:#10243D; }
  .logo-fallback .tag { color:#64748B; }
  .hero { text-align:center; }
  .hero h1 { font-size: 2.0rem; margin: .25rem 0; color: #10243D; }
  .hero p { color: #111827; max-width: 780px; margin: 0 auto .75rem; font-size: 1.05rem; }
  .pb-btn { margin-bottom: .5rem; }
  .pb-btn button {
      width: 100% !important;
      height: 88px !important;
      border-radius: 18px !important;
      font-size: 28px !important;
      font-weight: 700 !important;
      box-shadow: 0 8px 18px rgba(0,0,0,0.06) !important;
      border: none !important;
  }
  .pb-btn.yes button   { background: #16A34A !important; color: #FFFFFF !important; }
  .pb-btn.no  button   { background: #DC2626 !important; color: #FFFFFF !important; }
  .pb-btn.maybe button { background: #F59E0B !important; color: #111827 !important; }
  .question-text { font-size: 1.35rem; font-weight: 700; color: #0f172a; margin: .25rem 0 1rem; }
  .pill { display:inline-block; padding: .35rem .75rem; border-radius:999px; font-weight:700; color:#fff; }
  .pill-low { background:#16A34A; }
  .pill-mod { background:#F59E0B; }
  .pill-high { background:#DC2626; }
  @media (max-width: 600px) {
    .hero h1 { font-size: 1.6rem; }
    .pb-btn button { height: 80px !important; font-size: 24px !important; }
  }
</style>
""", unsafe_allow_html=True)

if LOGO_PATH is not None and LOGO_PATH.exists():
    st.markdown(logo_html_base64(LOGO_PATH), unsafe_allow_html=True)
else:
    st.markdown(logo_html_base64(Path()), unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>PreBate – Estate Readiness</h1>
  <p>Helping you prepare your estate with easy-to-use guidance.</p>
  <hr/>
</div>
""", unsafe_allow_html=True)

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
    if not rule:
        return True
    for k,v in rule.items():
        if st.session_state.get("answers", {}).get(k) != v:
            return False
    return True

def next_index(idx):
    n = len(QUESTIONS)
    while idx < n and not cond_ok(QUESTIONS[idx]):
        idx += 1
    return idx

if "step" not in st.session_state: st.session_state.step = 0
if "answers" not in st.session_state: st.session_state.answers = {}
if "completed" not in st.session_state: st.session_state.completed = False
st.session_state.step = next_index(st.session_state.step)

total_showable = sum(1 for q in QUESTIONS if cond_ok(q))
answered = sum(1 for q in QUESTIONS if cond_ok(q) and q["id"] in st.session_state.answers)
st.progress(int((answered/total_showable)*100) if total_showable else 0,
            text=f"{answered} of {total_showable} answered")

if st.session_state.step < len(QUESTIONS):
    q = QUESTIONS[st.session_state.step]
    st.markdown(f'<div class="question-text">{q["text"]}</div>', unsafe_allow_html=True)

    if q["type"] == "ynm":
        c1, c2, c3 = st.columns(3, gap="small")
        with c1:
            st.markdown('<div class="pb-btn yes">', unsafe_allow_html=True)
            if st.button("✅ Yes", use_container_width=True, key=f"{q['id']}_yes"):
                st.session_state.answers[q["id"]] = "Yes"
                st.session_state.step = next_index(st.session_state.step + 1)
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="pb-btn maybe">', unsafe_allow_html=True)
            if st.button("❓ Not sure", use_container_width=True, key=f"{q['id']}_maybe"):
                st.session_state.answers[q["id"]] = "Not sure"
                st.session_state.step = next_index(st.session_state.step + 1)
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="pb-btn no">', unsafe_allow_html=True)
            if st.button("❌ No", use_container_width=True, key=f"{q['id']}_no"):
                st.session_state.answers[q["id"]] = "No"
                st.session_state.step = next_index(st.session_state.step + 1)
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        c1, c2 = st.columns(2, gap="small")
        with c1:
            st.markdown('<div class="pb-btn yes">', unsafe_allow_html=True)
            if st.button("✅ Yes", use_container_width=True, key=f"{q['id']}_yes"):
                st.session_state.answers[q["id"]] = "Yes"
                st.session_state.step = next_index(st.session_state.step + 1)
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="pb-btn no">', unsafe_allow_html=True)
            if st.button("❌ No", use_container_width=True, key=f"{q['id']}_no"):
                st.session_state.answers[q["id"]] = "No"
                st.session_state.step = next_index(st.session_state.step + 1)
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    back_col, _ = st.columns([1,4])
    with back_col:
        if st.button("← Back", use_container_width=True, help="Go to previous question", key=f"{q['id']}_back"):
            i = st.session_state.step - 1
            while i >= 0 and (not cond_ok(QUESTIONS[i]) or QUESTIONS[i]["id"] not in st.session_state.answers):
                i -= 1
            if i >= 0:
                st.session_state.step = i
            st.rerun()

else:
    st.session_state.completed = True

if st.session_state.completed:
    a = st.session_state.answers
    probate_risk = 0; dispute_risk = 0; actions = []
    def add(x):
        if x not in actions: actions.append(x)

    if a.get("q_country") == "No": add("Laws vary outside Ireland—ensure local estate planning aligned to your jurisdiction.")
    if a.get("q_partner") == "No": probate_risk += 1; add("If single, ensure you have a valid will to direct assets clearly.")
    if a.get("q_children") == "Yes": add("Add guardianship and inheritance clauses for dependents in your will.")
    if a.get("q_divorce") == "Yes": probate_risk += 1; add("Review titles and beneficiaries after separation/divorce.")

    if a.get("q_property_sole") == "Yes": probate_risk += 2; add("Consider adding a joint owner (joint tenants), using a trust, or updating your will for solely-owned property.")
    if a.get("q_property_coown") == "Yes" and a.get("q_property_joint_tenants") == "No": probate_risk += 1; add("Consider joint tenancy where appropriate to enable survivorship.")
    if a.get("q_property_registered") in ["No","Not sure"]: probate_risk += 1; add("Register any unregistered property with the Land Registry (get a folio number).")
    if a.get("q_property_abroad") == "Yes": probate_risk += 1; add("Create a local will or plan for assets held outside Ireland.")

    if a.get("q_bank_sole") == "Yes": probate_risk += 1; add("For sole accounts, consider joint holder or pay-on-death nomination (if available).")
    if a.get("q_caregiver_access") == "Yes":
        if a.get("q_caregiver_official") == "Yes":
            dispute_risk += 1; add("Document the intent of caregiver/joint access (assistance vs inheritance) in writing with your solicitor.")
        else:
            dispute_risk += 2; probate_risk += 1; add("Revoke informal access. Consider an Enduring Power of Attorney (EPA) if help is needed."); add("Keep a simple log of legitimate expenses paid by helpers on your behalf.")
    if a.get("q_bank_joint") == "No": add("Consider a joint account for shared household expenses to ease continuity for a partner.")
    if a.get("q_investments") == "Yes": probate_risk += 1; add("Hold investments via nominee accounts or trusts to simplify transfer.")
    if a.get("q_multiple_brokers") == "Yes": add("Consolidate accounts to reduce admin burden on your executor.")

    if a.get("q_life") == "Yes" and a.get("q_life_beneficiary") == "No": probate_risk += 1; add("Add a named beneficiary to life insurance so it bypasses probate.")
    if a.get("q_pension") == "Yes" and a.get("q_pension_beneficiary") == "No": probate_risk += 1; add("File a pension beneficiary nomination with your provider.")
    if a.get("q_death_in_service") == "Yes": add("Confirm your employer nomination for death-in-service benefits.")

    if a.get("q_will") == "No": probate_risk += 2; add("Make a valid will—without one, intestacy rules apply.")
    if a.get("q_will") == "Yes" and a.get("q_will_recent") == "No": probate_risk += 1; add("Review/update your will (aim every 3 years or upon life changes).")
    if a.get("q_will_stored") == "No": add("Store your will with your solicitor or register a copy with the Probate Office.")
    if a.get("q_executor_informed") == "No": add("Inform your executor that they are named and where documents are kept.")
    if a.get("q_lifetime_gifts") == "Yes": add("Have a solicitor review documentation for lifetime gifts/trusts.")

    if a.get("q_business") == "Yes": probate_risk += 1; add("Create a succession/shareholder plan for your business interests.")
    if a.get("q_farmland") == "Yes": add("Explore Agricultural or Business Relief to optimize tax and transfer.")
    if a.get("q_digital") == "Yes": add("Document a digital asset plan (locations, instructions, and access).")
    if a.get("q_expect_inherit") == "Yes": add("Coordinate your plan if you expect to inherit—timing/structure can reduce complexity.")

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

    def build_pdf():
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, Image as RLImage
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="TitlePB", fontSize=18, leading=22, textColor=colors.HexColor("#10243D"), spaceAfter=12))
        styles.add(ParagraphStyle(name="H2PB", fontSize=13, leading=16, textColor=colors.HexColor("#10243D"), spaceAfter=6))
        styles.add(ParagraphStyle(name="BodyPB", fontSize=11, leading=16, textColor=colors.HexColor("#111827")))
        story = [Paragraph("PreBate – Estate Readiness Report", styles["TitlePB"]),
                 Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["BodyPB"]),
                 Spacer(1, 8),
                 Paragraph(f"<b>Probate Risk:</b> {probate_label} (score {probate_risk})", styles["BodyPB"]),
                 Paragraph(f"<b>Dispute Risk:</b> {dispute_label} (score {dispute_risk})", styles["BodyPB"]),
                 Spacer(1, 10),
                 Paragraph("Recommended Actions", styles["H2PB"])]
        if actions:
            items = [ListItem(Paragraph(x, styles["BodyPB"])) for x in actions]
            story.append(ListFlowable(items, bulletType='1', start='1'))
        else:
            story.append(Paragraph("No immediate actions detected.", styles["BodyPB"]))
        doc.build(story)
        pdf = buffer.getvalue(); buffer.close(); return pdf

    pdf_bytes = build_pdf()
    st.download_button("Download Report (PDF)", data=pdf_bytes, file_name="prebate_report.pdf", mime="application/pdf")

    if st.button("Start Over"):
        st.session_state.step = 0; st.session_state.answers = {}; st.session_state.completed = False; st.rerun()
