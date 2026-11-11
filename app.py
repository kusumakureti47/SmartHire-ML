"""SmartHire AI - Streamlit entry point. Run:  streamlit run app.py"""
import streamlit as st
from ui import components as C, views

st.set_page_config(page_title="SmartHire AI", page_icon="🎯", layout="wide")
C.inject_css()
ss = st.session_state
ss.setdefault("page", "Dashboard"); ss.setdefault("user", "Student"); ss.setdefault("signed_in", True)

NAV = [("Dashboard", "dashboard"), ("Resume Upload", "upload_file"), ("Resume Analysis", "analytics"),
       ("Job Recommendations", "work"), ("Role Prediction", "psychology"), ("Skill Gap Analysis", "query_stats"),
       ("Profile / Settings", "settings"), ("Logout", "logout")]


def logout():
    for k in ("resume_name", "resume_text", "analysis", "activity"): ss.pop(k, None)
    ss.signed_in, ss.page = False, "Dashboard"
    st.rerun()


if not ss.signed_in:
    C.header("Signed out", "—")
    with C.card():
        C.section("Sign in")
        name = st.text_input("Your name", ss.user)
        if st.button("Continue", type="primary"):
            ss.user, ss.signed_in = name.strip() or "Student", True; st.rerun()
    st.stop()

clicked = C.sidebar(NAV, ss.page)
if clicked == "Logout": logout()
if clicked: ss.page = clicked; st.rerun()

status = "Uploaded" if ss.get("resume_name") else "Not uploaded"
if C.header(ss.user, status): logout()
views.PAGES[ss.page]()