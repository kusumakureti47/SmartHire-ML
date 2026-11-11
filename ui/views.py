"""One function per page. All displayed numbers come from ui.backend (your ML models)."""
from datetime import datetime
import streamlit as st
from ui import backend, components as C

ss = st.session_state


def log(msg):
    ss.setdefault("activity", []).append((datetime.now().strftime("%d %b %H:%M"), msg))


def _a():
    return ss.get("analysis")


def _need_resume():
    st.info("Upload and analyze a resume first.")
    if st.button("Go to Resume Upload", type="primary"):
        ss.page = "Resume Upload"; st.rerun()


def _errors(a):
    for er in a["errors"]:
        st.error(er)


def dashboard():
    a = _a()
    C.banner(f"Hi <b>{ss.user}</b>, welcome to SmartHire AI. Your resume analysis from the trained models is shown below.")
    cat = a["category"]["label"] if a and a["category"] else "—"
    pct = f'{a["gap"]["percent"]:.0f}%' if a and a["gap"] and a["gap"]["percent"] is not None else "—"
    top = f'{a["jobs"][0]["score"]:.1f}%' if a and a["jobs"] and a["jobs"][0]["score"] is not None else "—"
    with C.card():
        c = st.columns(4)
        with c[0]: C.stat("Resume status", "Uploaded" if ss.get("resume_name") else "Not uploaded", pink=True)
        with c[1]: C.stat("Predicted category", cat)
        with c[2]: C.stat("Skill match", pct)
        with c[3]: C.stat("Best job match", top)
    if a: _errors(a)
    with C.card():
        C.section("Top 5 recommended jobs")
        C.job_list(a["jobs"] if a else [])
    l, r = st.columns(2)
    with l, C.card():
        C.section("Skills matched"); C.chips(a["gap"]["matched"] if a and a["gap"] else [], "ok", "Run an analysis to see matched skills.")
    with r, C.card():
        C.section("Missing skills"); C.chips(a["gap"]["missing"] if a and a["gap"] else [], "bad", "Run an analysis to see missing skills.")
    with C.card():
        C.section("Recent analysis activity"); C.activity(ss.get("activity", []))
    C.footer_note()


def upload():
    C.banner("Upload your resume as <b>PDF</b> or <b>DOCX</b>, then run the analysis.")
    with C.card():
        C.section("Resume Upload")
        f = st.file_uploader("Choose a resume", type=["pdf", "docx"], label_visibility="collapsed")
        if f and st.button("Analyze resume", type="primary", icon=":material/analytics:"):
            try:
                with st.spinner("Reading resume and running models..."):
                    text = backend.extract_text(f)
                    ss.resume_name, ss.resume_text = f.name, text
                    log(f"Uploaded {f.name}")
                    ss.analysis = backend.run_analysis(text)
                    ss.pop("gap_custom", None)
                    log("Completed resume analysis")
                ss.page = "Dashboard"; st.rerun()
            except Exception as ex:
                st.error(str(ex))
        if ss.get("resume_name"):
            C.info_table([("Current resume", ss.resume_name), ("Characters extracted", f'{len(ss.resume_text):,}')])


def analysis():
    a = _a()
    if not a: return _need_resume()
    with C.card():
        C.section("Resume Analysis")
        words = len(ss.resume_text.split())
        C.info_table([("File", ss.resume_name), ("Word count", words),
                      ("Predicted category", a["category"]["label"] if a["category"] else "—"),
                      ("Skill match", f'{a["gap"]["percent"]:.1f}%' if a["gap"] and a["gap"]["percent"] is not None else "—")])
    _errors(a)
    with C.card():
        C.section("Extracted text preview")
        st.text_area("Text", ss.resume_text[:3000], height=220, label_visibility="collapsed", disabled=True)


def jobs():
    a = _a()
    if not a: return _need_resume()
    _errors(a)
    with C.card():
        C.section("Job Recommendations (TF-IDF + cosine similarity)")
        C.job_list(a["jobs"])
    for j in a["jobs"]:
        with st.expander(f'{j["title"]}'):
            C.info_table([(k, v) for k, v in j["raw"].items() if v not in (None, "") and len(str(v)) < 400])


def role():
    a = _a()
    if not a: return _need_resume()
    _errors(a)
    with C.card():
        C.section("Role Prediction (TF-IDF + Logistic Regression)")
        cat = a["category"]
        C.info_table([("Predicted category", cat["label"] if cat else "—"),
                      ("Model confidence", f'{cat["confidence"]:.1f}%' if cat and cat["confidence"] is not None
                       else "Not returned by predict_category.py")])


def gap():
    a = _a()
    if not a or not a["jobs"]: return _need_resume()
    titles = [f'{i+1}. {j["title"]}' for i, j in enumerate(a["jobs"])]
    with C.card():
        C.section("Skill Gap Analysis")
        idx = titles.index(st.selectbox("Compare my resume with", titles))
    try:
        g = a["gap"] if idx == 0 else backend.skill_gap(ss.resume_text, a["jobs"][idx])
    except Exception as ex:
        return st.error(f"{type(ex).__name__}: {ex}")
    if not g: return _errors(a)
    with C.card():
        C.stat("Skill match percentage", f'{g["percent"]:.1f}%' if g["percent"] is not None else "—", pink=True)
        st.progress(min(100, int(g["percent"] or 0)) / 100)
    l, r = st.columns(2)
    with l, C.card():
        C.section("Skills matched"); C.chips(g["matched"], "ok", "No matched skills.")
    with r, C.card():
        C.section("Missing skills"); C.chips(g["missing"], "bad", "No missing skills.")


def settings():
    with C.card():
        C.section("Profile / Settings")
        name = st.text_input("Display name", ss.user)
        if st.button("Save changes", type="primary"):
            ss.user = name.strip() or ss.user; log("Updated profile"); st.rerun()
    with C.card():
        if st.button("Clear resume and results", icon=":material/delete:"):
            for k in ("resume_name", "resume_text", "analysis", "activity"): ss.pop(k, None)
            st.rerun()


PAGES = {"Dashboard": dashboard, "Resume Upload": upload, "Resume Analysis": analysis,
         "Job Recommendations": jobs, "Role Prediction": role, "Skill Gap Analysis": gap,
         "Profile / Settings": settings}