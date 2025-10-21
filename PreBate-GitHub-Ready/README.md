# PreBate – Estate Readiness Pilot (Streamlit)

A simple, seniors‑friendly wizard that helps people spot probate risks in Ireland and get a personalized action plan. One question at a time. Big buttons. PDF report.

## Features
- Single‑question flow with large, high‑contrast buttons (Yes / No / Not sure)
- Caregiver/financial access question to flag dispute risks
- Probate + Dispute risk scoring
- Personalized action checklist
- PDF download (with logo)

## Local Run
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud
1. Push this folder to a new GitHub repo, e.g. `prebate-pilot`.
2. Go to https://share.streamlit.io → **New app**.
3. Choose:  
   - **Repository:** `YOURUSERNAME/prebate-pilot`  
   - **Branch:** `main`  
   - **App file:** `app.py`
4. Click **Deploy**. Share the URL.

## Deploy to Hugging Face Spaces
1. Create a Space → choose **Streamlit**.
2. Upload `app.py`, `requirements.txt`, `.streamlit/config.toml`, and the `assets/` folder.
3. Wait for the build → share the URL.

## Customizing
- Replace `assets/prebate_logo.png` with your own logo (same name/path).
- Update `.streamlit/config.toml` to tweak the theme.
- Adjust questions/logic in `app.py` (look for the `QUESTIONS` list and the scoring section).

> **Note:** This pilot is for educational purposes and does not constitute legal advice. Consult a solicitor for personalized guidance.
