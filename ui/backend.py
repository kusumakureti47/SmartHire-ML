"""
Thin adapter between the Streamlit UI and your existing SmartHire backend.
It does NOT modify src/. It imports your modules, calls your functions and normalises the output.

If your function names differ, put the right name first in the *_FUNCS lists below.
Nothing is faked: if a call fails, the real error is returned and shown in the UI.
"""
import importlib, inspect, io, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ---- EDIT HERE if your function names differ -------------------------------------------
PREDICT = ("src.predict_category", ["predict_category", "predict_resume_category", "predict", "get_category"])
RECOMMEND = ("src.job_recommender", ["recommend_jobs", "get_job_recommendations", "recommend", "get_recommendations"])
SKILLGAP = ("src.skill_gap", ["skill_gap_analysis", "analyze_skill_gap", "analyse_skill_gap", "skill_gap", "get_skill_gap"])
CLEAN = ("src.data.preprocess", ["clean_text", "clean_resume", "preprocess_text", "preprocess"])  # optional
TOP_N = 5
# ----------------------------------------------------------------------------------------


def _fn(spec):
    mod_name, names = spec
    mod = importlib.import_module(mod_name)
    for n in names:
        f = getattr(mod, n, None)
        if callable(f):
            return f
    raise AttributeError(f"No function found in {mod_name}. Tried {names}. "
                         f"Available: {[n for n in dir(mod) if not n.startswith('_')]}")


def _call(fn, text=None, job=None, top_n=TOP_N):
    """Bind arguments by parameter name; first required parameter defaults to the resume text."""
    kwargs, first = {}, True
    for name, p in inspect.signature(fn).parameters.items():
        if p.kind in (p.VAR_POSITIONAL, p.VAR_KEYWORD):
            continue
        l = name.lower()
        if l in ("n", "k", "limit") or "top" in l:
            kwargs[name] = top_n
        elif job is not None and ("job" in l or "required" in l or "target" in l):
            kwargs[name] = job
        elif "resume" in l or "text" in l or "skill" in l or (first and p.default is p.empty):
            kwargs[name] = text
        first = False
    return fn(**kwargs)


def extract_text(uploaded) -> str:
    """Read text from an uploaded PDF or DOCX (Streamlit UploadedFile)."""
    name, data = uploaded.name.lower(), uploaded.getvalue()
    if name.endswith(".pdf"):
        from pypdf import PdfReader
        text = "\n".join((pg.extract_text() or "") for pg in PdfReader(io.BytesIO(data)).pages)
    elif name.endswith(".docx"):
        from docx import Document
        d = Document(io.BytesIO(data))
        text = "\n".join(p.text for p in d.paragraphs)
        for t in d.tables:
            text += "\n" + "\n".join(c.text for r in t.rows for c in r.cells)
    else:
        raise ValueError("Only PDF and DOCX files are supported.")
    if not text.strip():
        raise ValueError("No readable text found. Scanned/image-only PDFs need OCR first.")
    return text


def _clean(text):
    try:
        return _call(_fn(CLEAN), text)
    except Exception:
        return text


# ---- normalisers -------------------------------------------------------------------------
def _pick(d, keys, default=None):
    low = {str(k).lower().replace(" ", "").replace("_", ""): v for k, v in d.items()}
    for k in keys:
        if k.replace("_", "") in low and low[k.replace("_", "")] is not None:
            return low[k.replace("_", "")]
    return default


def _as_list(v):
    if v is None:
        return []
    if isinstance(v, str):
        return [s.strip() for s in v.replace("|", ",").replace(";", ",").split(",") if s.strip()]
    return [str(s) for s in v]


def _pct(v):
    if v is None:
        return None
    try:
        v = float(v)
    except Exception:
        return None
    return v * 100 if v <= 1 else v


def normalise_prediction(res):
    conf = None
    if isinstance(res, dict):
        label = _pick(res, ["category", "label", "prediction", "predicted_category", "role"])
        conf = _pct(_pick(res, ["confidence", "probability", "score"]))
        if label is None and res and all(isinstance(v, (int, float)) for v in res.values()):
            label = max(res, key=res.get); conf = _pct(res[label])
    elif isinstance(res, (list, tuple)):
        label = res[0]
        conf = _pct(res[1]) if len(res) > 1 else None
    else:
        label = res
    if hasattr(label, "item"):
        label = label.item()
    return {"label": str(label), "confidence": conf}


def normalise_jobs(res):
    if hasattr(res, "to_dict"):
        res = res.to_dict("records")
    jobs = []
    for r in list(res)[:TOP_N]:
        if not isinstance(r, dict):
            raise TypeError("Job recommender must return a DataFrame or list of dicts with a title column.")
        jobs.append({
            "title": _pick(r, ["jobtitle", "title", "job", "role", "jobrole", "position"], "Untitled role"),
            "company": _pick(r, ["company", "companyname", "organization"]),
            "score": _pct(_pick(r, ["score", "similarity", "matchscore", "matchpercentage", "cosinesimilarity", "match"])),
            "skills": _pick(r, ["keyskills", "skills", "requiredskills", "skillsrequired", "jobskills"], ""),
            "raw": r,
        })
    return jobs


def normalise_gap(res):
    if isinstance(res, dict):
        matched = _as_list(_pick(res, ["matched", "matchedskills", "skillsmatched", "matching", "common"]))
        missing = _as_list(_pick(res, ["missing", "missingskills", "skillsmissing", "gap"]))
        pct = _pct(_pick(res, ["percentage", "matchpercentage", "skillmatch", "matchpercent", "match", "score"]))
    else:
        res = list(res)
        matched, missing = _as_list(res[0]), _as_list(res[1])
        pct = _pct(res[2]) if len(res) > 2 else None
    if pct is None and (matched or missing):
        pct = 100 * len(matched) / (len(matched) + len(missing))
    return {"matched": matched, "missing": missing, "percent": pct}


# ---- public API used by the pages --------------------------------------------------------
def predict_category(text):
    return normalise_prediction(_call(_fn(PREDICT), _clean(text)))


def recommend_jobs(text):
    return normalise_jobs(_call(_fn(RECOMMEND), _clean(text), top_n=TOP_N))


def skill_gap(text, job):
    return normalise_gap(_call(_fn(SKILLGAP), text, job=job.get("skills") or job["title"]))


def run_analysis(text):
    """Runs all three models. Each step fails independently so one error never hides the others."""
    out = {"category": None, "jobs": [], "gap": None, "errors": []}
    for key, step in (("category", lambda: predict_category(text)), ("jobs", lambda: recommend_jobs(text))):
        try:
            out[key] = step()
        except Exception as ex:
            out["errors"].append(f"{key}: {type(ex).__name__}: {ex}")
    if out["jobs"]:
        try:
            out["gap"] = skill_gap(text, out["jobs"][0])
        except Exception as ex:
            out["errors"].append(f"skill gap: {type(ex).__name__}: {ex}")
    return out