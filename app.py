# FRAUDGUARD — UI Updated: Mint & Teal Minimal (Perfect Balance)
# ONLY UI / placement changes. No logic changes.
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import time
import base64
from io import BytesIO
import random
import requests
import plotly.graph_objects as go
import gdown
import os

os.environ["PANDAS_PARQUET_ENGINE"] = "auto"

# ==========================
# THEME PALETTE (Mint & Teal Minimal)
# ==========================
PALETTE = {
    "primary": "#0D9488",       # Teal (line)
    "secondary": "#14B8A6",     # Mint (markers / accents)
    "accent": "#99F6E4",        # Soft aqua
    "text": "#1E293B",          # Charcoal navy
    "muted": "#6B7280",         # Grey labels
    "background": "#FFFFFF"     # Pure white background
}

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(page_title="FraudGuard", page_icon="🛡️", layout="wide")

# =====================================================
# REMOVE ALL TOP SPACING (FINAL FIX)
# =====================================================
st.markdown("""
<style>

/* Remove Streamlit built-in header */
header[data-testid="stHeader"] {
    display: none !important;
    height: 0 !important;
}

/* Remove top padding from main container */
[data-testid="stAppViewContainer"] {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

/* Remove hidden padding Streamlit adds to the first block */
section.main {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

/* Remove padding inside block container */
div.block-container {
    padding-top: 0px !important;
    margin-top: 0px !important;
}

/* FORCE remove any remaining top spacing */
section.main > div:first-child {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

/* Ensure the title sits at the absolute top */
.fintech-title {
    margin-top: 0px !important;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# STYLES (Mint & Teal Minimal)
# =====================================================
st.markdown(
    f"""
<style>
html, body, [data-testid="stAppViewContainer"] {{
    background: {PALETTE['background']} !important;
    color: {PALETTE['text']} !important;
    font-family: "Inter", "Segoe UI", "Helvetica Neue", Arial, sans-serif;
}}

/* container sizing */
.block-container {{
    padding: 10px 20px !important;
    max-width: 1400px;
    margin: auto;
}}

/* Title - gradient mint-teal */
.fintech-title {{
    text-align: center;
    font-size: 2.9rem;
    font-weight: 800;
    margin: 6px 0 2px 0;
    background: linear-gradient(90deg, {PALETTE['primary']}, {PALETTE['secondary']});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

/* Subtitle */
.fintech-sub {{
    text-align: center;
    font-size: 0.95rem;
    color: {PALETTE['muted']};
    margin-bottom: 12px;
}}

/* Tabs */
.stTabs [data-baseweb="tab"] {{
    font-size: 1.02rem !important;
    font-weight: 700 !important;
    padding: 8px 16px !important;
    color: {PALETTE['muted']} !important;
}}
.stTabs [aria-selected="true"] {{
    color: {PALETTE['primary']} !important;
    border-bottom: 3px solid {PALETTE['secondary']} !important;
}}

/* Buttons */
.stButton>button {{
    background: linear-gradient(90deg, {PALETTE['primary']}, {PALETTE['secondary']}) !important;
    color: white !important;
    border-radius: 10px !important;
    padding: 8px 14px !important;
    font-weight:700 !important;
    border:none !important;
    box-shadow: 0 6px 18px rgba(20,184,166,0.10);
}}
.stButton>button:disabled {{ opacity:0.6 !important; }}

/* Section title gradient */
.section-title {{
    font-size:1.15rem; 
    font-weight:800;
    background: linear-gradient(90deg, {PALETTE['primary']}, {PALETTE['secondary']});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom:8px;
}}

/* Card base */
.card {{
    background: #FFFFFF;
    border-radius:14px;
    padding:14px;
    box-shadow: 0 6px 18px rgba(20,184,166,0.06);
    border-left:6px solid {PALETTE['accent']};
    margin-bottom:10px;
}}

/* Live card specifics */
.live-card {{
    display:flex; justify-content:space-between; align-items:center;
}}
.live-amount {{ font-size:1.5rem; font-weight:800; color:{PALETTE['text']}; }}
.live-meta {{ color:{PALETTE['muted']}; font-size:0.9rem; }}
.live-decision {{
    font-size:1.2rem; font-weight:800;
    background: linear-gradient(90deg, {PALETTE['primary']}, {PALETTE['secondary']});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}
.live-risk {{ font-size:0.95rem; color:{PALETTE['muted']}; }}

/* Risk left border overrides */
.live-high {{ border-left-color: #EF4444 !important; }}
.live-medium {{ border-left-color: #F59E0B !important; }}
.live-low {{ border-left-color: #10B981 !important; }}

/* Upload box */
.upload-box {{
    border: 2px dashed rgba(20,184,166,0.20);
    padding:12px;
    border-radius:12px;
    background: #FFFFFF;
}}

/* Kpi */
.kpi-card {{
    background:#FFFFFF; padding:14px; border-radius:12px; border:1px solid rgba(20,184,166,0.06);
}}
.kpi-number {{
    font-size:2.4rem; font-weight:900;
    background: linear-gradient(90deg, {PALETTE['primary']}, {PALETTE['secondary']});
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}}

/* Responsive tweaks */
@media (max-width: 900px) {{
    .fintech-title {{ font-size:2.2rem; }}
    .live-amount {{ font-size:1.2rem; }}
}}
</style>
""", unsafe_allow_html=True)

# =====================================================
# TITLE
# =====================================================
st.markdown('<h1 class="fintech-title">FraudGuard</h1>', unsafe_allow_html=True)
#st.markdown('<div class="fintech-sub">Compact & balanced fraud monitoring — Mint & Teal Minimal</div>', unsafe_allow_html=True)
@st.cache_resource
def load_models():

    import os
    import gdown
    import joblib
    import pandas as pd
    import numpy as np
    from xgboost import XGBClassifier
    import keras

    os.makedirs("models", exist_ok=True)

    # =======================
    # GOOGLE DRIVE FILES
    # =======================
    FILES = {
        "bundle": {
            "url": "https://drive.google.com/uc?id=17PzAxmCehh_nGLT1gchjmkyEVDojdG5f",
            "path": "models/model_bundle.pkl"
        },
        "features": {
            "url": "https://drive.google.com/uc?id=1BQmhFK2TqM2HwwhW3HJo5T8pYvyRbdM3",
            "path": "models/scaled_features.pkl"
        },
        "xgb": {
            "url": "https://drive.google.com/uc?id=1rTuOkxINXJj7QWxASuD5Far_kAyJb-A6",
            "path": "models/xgb_model.json"
        },
        "autoencoder": {
            "url": "https://drive.google.com/uc?id=1uHcR911V_4M-wsPIC4HaP_xmkjXZcrDh",
            "path": "models/autoencoder_savedmodel"
        },
        "copod": {
            "url": "https://drive.google.com/uc?id=15wWaZJ73H8FDJwzTVzUS_6gdBETH8oJD",
            "path": "models/copod.pkl"
        }
    }

    def download(url, path, is_folder = False):
        if not os.path.exists(path):
            return 
        
        if is_folder:
            gdown.download_folder(url, output=path, quiet=False)
        else:
            gdown.download(url, path, quiet=False)
    # ---- download everything ----
    for name, f in FILES.items():
        if name == "autoencoder":
            download(f["url"], f["path"], is_folder=True)
        else:
            download(f["url"], f["path"], is_folder=False)


    # ---- load metadata ----
    bundle = joblib.load(FILES["bundle"]["path"])
    top3 = bundle["top3_names"]
    scalers = bundle["norm_scalers"]
    weights = bundle["weights"]

    # ---- load features ----
    df = pd.read_pickle(FILES["features"]["path"])
    features = [c for c in df.columns if c != "Class"]

    # ---- load models ----
    models_dict = {}

    xgb = XGBClassifier()
    xgb.load_model(FILES["xgb"]["path"])
    models_dict["XGBoost (Supervised)"] = xgb

    autoencoder = keras.models.load_model(
    FILES["autoencoder"]["path"],
    compile=False
    )
    models_dict["Autoencoder"] = autoencoder

    copod = joblib.load(FILES["copod"]["path"])
    models_dict["COPOD"] = copod

    # ---- prototypes ----
    normal_mean = df[df["Class"] == 0][features].mean().values.astype(np.float32)
    fraud_mean = df[df["Class"] == 1][features].mean().values.astype(np.float32)

    return models_dict, top3, scalers, weights, features, normal_mean, fraud_mean



# Load models for use
models_dict, top3_models, scalers, weights, features, NORMAL_PROTO, FRAUD_PROTO = load_models()

# =====================================================
# PREDICTION & RULE BOOST (unchanged)
# =====================================================
def rule_boost_fast(amounts, hours):
    a = np.asarray(amounts, float)
    h = np.asarray(hours, int)
    b = np.zeros(len(a))
    b[a >= 5000] += 0.50
    b[(a >= 2000) & (a < 5000)] += 0.35
    b[(a >= 1000) & (a < 2000)] += 0.20
    b[h <= 5] += 0.30
    return b

def predict_single(amount, hour):
    hour = int(hour) % 24
    amount = float(amount)
    base = FRAUD_PROTO if (amount > 3000 and hour <= 5) else NORMAL_PROTO
    X = base.copy().reshape(1, -1)

    if "Amount_log" in features: X[0, features.index("Amount_log")] = np.log1p(amount)
    if "Amount" in features:     X[0, features.index("Amount")] = amount
    if "Hour" in features:       X[0, features.index("Hour")] = hour

    for f in ["sin_hour","sin_Hour","cos_hour","cos_Hour"]:
        if f in features:
            idx = features.index(f)
            X[0, idx] = np.sin(2*np.pi*hour/24) if "sin" in f.lower() else np.cos(2*np.pi*hour/24)

    scores = {}
    for name in top3_models:
        m = models_dict[name]
        if "XGBoost" in name:
            scores[name] = m.predict_proba(X)[0,1]
        elif "Autoencoder" in name:
            rec = m.predict(X, verbose=0)
            mse = float(np.mean((X-rec)**2))
            scores[name] = np.clip(mse/10, 0, 1)
        else:
            scores[name] = float(1/(1+np.exp(-m.decision_function(X)[0])))

    norm = [scalers[n].transform([[scores[n]]])[0][0] for n in top3_models]
    ml_score = sum(w*n for w,n in zip(weights, norm))
    final = float(np.clip(ml_score + rule_boost_fast([amount], [hour])[0], 0, 1))

    decision = "BLOCK" if final >= 0.5 else "ALLOW"
    level = "HIGH RISK" if final >= 0.7 else "MEDIUM RISK" if final >= 0.3 else "LOW RISK"
    return {"risk": round(final*100,2), "decision": decision, "level": level}

def predict_bulk(amounts, hours):
    amounts = np.asarray(amounts, float)
    hours = np.asarray(hours, int) % 24
    use_fraud = (amounts > 3000) & (hours <= 5)
    X = np.where(use_fraud[:, None], FRAUD_PROTO, NORMAL_PROTO)

    if "Amount_log" in features: X[:, features.index("Amount_log")] = np.log1p(amounts)
    if "Amount" in features:     X[:, features.index("Amount")] = amounts
    if "Hour" in features:       X[:, features.index("Hour")] = hours

    for f in ["sin_hour","sin_Hour","cos_hour","cos_Hour"]:
        if f in features:
            i = features.index(f)
            X[:, i] = np.sin(2*np.pi*hours/24) if "sin" in f.lower() else np.cos(2*np.pi*hours/24)

    all_scores = []
    for name in top3_models:
        m = models_dict[name]
        if "XGBoost" in name:
            p = m.predict_proba(X)[:,1]
        elif "Autoencoder" in name:
            rec = m.predict(X, verbose=0)
            mse = np.mean((X-rec)**2, axis=1)
            p = np.clip(mse/10, 0, 1)
        else:
            p = 1/(1+np.exp(-m.decision_function(X)))
        all_scores.append(p)

    ml = sum(w*scalers[n].transform(s.reshape(-1,1)).flatten()
             for w,n,s in zip(weights, top3_models, all_scores))

    final = np.clip(ml + rule_boost_fast(amounts, hours), 0, 1)
    out = pd.DataFrame()
    out["Risk %"] = np.round(final*100, 2)
    out["Decision"] = np.where(final >= 0.5, "BLOCK", "ALLOW")
    out["Level"] = np.where(final >= 0.7, "HIGH RISK", np.where(final >= 0.3, "MEDIUM RISK", "LOW RISK"))
    return out

import google.generativeai as genai
# Configure Gemini (unchanged - uses st.secrets)
genai.configure(api_key=st.secrets["gemini"]["api_key"])

def get_ai_suggestions(amount, hour, level):
    prompt = f"""
    You are a fraud detection expert. 
    Amount: {amount}
    Hour: {hour}
    Risk Level: {level}

    Give EXACTLY 2 short actionable suggestions for users to reduce risk.
    Keep them in plain text, no numbering.
    """

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        text = response.text.strip()
        tips = [t.strip("-• ") for t in text.split("\n")][:2]
        if len(tips) < 2:
            tips += ["Use trusted device", "Avoid night transactions"]
        return tips
    except Exception as e:
        return [f"AI error: {e}", "Fallback: Use trusted device & avoid night transactions."]

# =====================================================
# Ensure session storage variables exist
# =====================================================
if "live_running" not in st.session_state:
    st.session_state.live_running = False
if "live_stop_request" not in st.session_state:
    st.session_state.live_stop_request = False
if "manual_result" not in st.session_state:
    st.session_state.manual_result = None
if "bulk_results" not in st.session_state:
    st.session_state.bulk_results = None
if "bulk_results_df" not in st.session_state:
    st.session_state.bulk_results_df = None
if "live_risk_list" not in st.session_state:
    st.session_state.live_risk_list = []

# =====================================================
# Tabs (balanced)
# =====================================================
tab1, tab2, tab3 = st.tabs(["Live Stream","Manual Test","Bulk Scanner"])

# =====================================================
# TAB 1 — LIVE STREAMING (Perfect Balanced Layout)
# =====================================================
with tab1:
    st.markdown('<div class="section-title">Live Streaming</div>', unsafe_allow_html=True)

    # Top row: Controls (left) + Chart (right)
    controls_col, chart_top_col = st.columns([1.2, 1])

    # ----------- CONTROLS -----------
    with controls_col:
        btn_start, btn_stop = st.columns([1,1])

        with btn_start:
            st.button(
                "Start Live Demo",
                disabled=st.session_state.live_running,
                use_container_width=True,
                on_click=lambda: st.session_state.update({"live_running": True})
            )
        with btn_stop:
            st.button(
                "Stop Live Demo",
                disabled=not st.session_state.live_running,
                use_container_width=True,
                on_click=lambda: st.session_state.update({"live_running": False})
            )

        st.markdown(
            f'<div style="margin-top:6px;color:{PALETTE["muted"]};">'
            'Live transactions stream — updates every second'
            '</div>',
            unsafe_allow_html=True
        )

    # ----------- CHART PLACEHOLDER (TOP RIGHT) -----------
    chart_ph = chart_top_col.empty()

    # --- Card directly under controls (NO GAP, NO NEW ROW) ---
    card_area = controls_col.container()
    card_ph = card_area.empty()
    sug_ph = card_area.empty()

    # REMOVE spacing above the card completely
    card_ph.markdown("<div style='margin-top:-45px'></div>", unsafe_allow_html=True)

    # ----------- Chart Title (Gradient) -----------
    gradient_title = f"""
    <span style="
        background: -webkit-linear-gradient(90deg, {PALETTE['primary']}, {PALETTE['secondary']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size:18px;
        font-weight:800;
    ">
    Live Risk Trend
    </span>
    """

    # ----------- CHART RENDER FUNCTION -----------
    def render_live_chart():
        fig = go.Figure()

        yvals = st.session_state.live_risk_list if st.session_state.live_risk_list else [0]

        fig.add_trace(go.Scatter(
            y=yvals,
            mode="lines+markers",
            line=dict(color=PALETTE["primary"], width=3),
            marker=dict(color=PALETTE["secondary"], size=6)
        ))

        fig.update_layout(
            title=dict(text=gradient_title, x=0.5),
            height=250,
            margin=dict(l=6, r=6, t=50, b=6),
            yaxis=dict(range=[0, 100], title="Risk (%)"),
            xaxis=dict(showticklabels=False)
        )

        chart_ph.plotly_chart(fig, use_container_width=True)

    # ----------- LIVE STREAM LOOP -----------
    if st.session_state.live_running:
        while st.session_state.live_running:

            amt = max(1.0, np.random.lognormal(4.5, 1.0))
            hr = np.random.randint(0, 24)

            # occasional fraud spikes
            if np.random.rand() < 0.22:
                amt = np.random.choice([5600, 9800, 12500])
                hr = np.random.randint(0, 5)

            res = predict_single(amt, hr)

            # determine risk color class
            cls = (
                "live-high" if res["level"] == "HIGH RISK" else
                "live-medium" if res["level"] == "MEDIUM RISK" else
                "live-low"
            )

            # -------- render card --------
            card_html = f"""
            <div class="card live-card {cls}">
                <div>
                    <div class="live-amount">${amt:,.2f}</div>
                    <div class="live-meta">@ {hr:02d}:00</div>
                </div>
                <div style="text-align:right;">
                    <div class="live-decision">{res['decision']}</div>
                    <div class="live-risk">Risk {res['risk']}% — {res['level']}</div>
                </div>
            </div>
            """
            card_ph.markdown(card_html, unsafe_allow_html=True)

            # -------- render suggestions --------
            if res["level"] in ["HIGH RISK", "MEDIUM RISK"]:
                tips = get_ai_suggestions(amt, hr, res["level"])
                sug_html = (
                    "<div class='card'><b>Suggestions:</b><ul style='margin-top:6px;margin-bottom:6px;'>"
                    + "".join(f"<li style='margin-bottom:4px'>{t}</li>" for t in tips)
                    + "</ul></div>"
                )
                sug_ph.markdown(sug_html, unsafe_allow_html=True)
            else:
                sug_ph.empty()

            # update graph data
            st.session_state.live_risk_list.append(res["risk"])
            st.session_state.live_risk_list = st.session_state.live_risk_list[-60:]

            render_live_chart()
            time.sleep(1)

            if not st.session_state.live_running:
                break

    else:
        # chart still shows even when stopped
        render_live_chart()
        card_ph.markdown(
            f'<div class="card"><div style="color:{PALETTE["muted"]}">'
            'Click Start Live Demo to begin the live stream.'
            '</div></div>',
            unsafe_allow_html=True
        )
        sug_ph.empty()


# =====================================================
# TAB 2 — MANUAL TEST (Balanced: Inputs left, Result right)
# =====================================================
with tab2:
    st.markdown('<div class="section-title">Manual Test</div>', unsafe_allow_html=True)

    left, right = st.columns([0.45, 0.55])

    with left:
        # Inputs placed in a mint-outlined card
        #st.markdown('<div class="card"><div style="padding-bottom:6px;"><strong>Transaction Inputs</strong></div>', unsafe_allow_html=True)
        amount_val = st.number_input("Amount ($)", 0.01, 100000.0, 1200.0)
        hour_text = st.text_input("Hour (1–12)", value="3")
        try:
            hour_12 = int(hour_text)
            hour_valid = 1 <= hour_12 <= 12
        except:
            hour_valid = False
        am_pm = st.selectbox("AM / PM", ["AM", "PM"])
        if hour_valid:
            hour_24 = hour_12 % 12 if am_pm == "AM" else hour_12 % 12 + 12
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("ANALYZE"):
            if not hour_valid:
                st.warning("Please enter hour as integer between 1 and 12.")
            else:
                st.session_state.manual_result = predict_single(amount_val, hour_24)

    with right:
        # Result card
        if st.session_state.get("manual_result") and ('hour_24' in locals() or 'hour_24' in globals()):
            r = st.session_state.manual_result
            cls = ("live-high" if r["level"] == "HIGH RISK" else "live-medium" if r["level"] == "MEDIUM RISK" else "live-low")
            st.markdown(f"""
                <div class="card {cls}">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <div class="live-amount">${amount_val:,.2f}</div>
                            <div class="live-meta">@ {hour_24:02d}:00</div>
                        </div>
                        <div style="text-align:right;">
                            <div class="live-decision">{r['decision']}</div>
                            <div class="live-risk">Risk {r['risk']}% — {r['level']}</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            if r["level"] in ["HIGH RISK", "MEDIUM RISK"]:
                st.markdown('<div class="card"><strong>Suggestions</strong></div>', unsafe_allow_html=True)
                tips = get_ai_suggestions(amount_val, hour_24, r["level"])
                for tip in tips:
                    st.markdown(f"- {tip}")

# =====================================================
# TAB 3 — BULK SCANNER (Balanced 3-column grid)
# =====================================================
with tab3:
    st.markdown('<div class="section-title">Bulk Scanner</div>', unsafe_allow_html=True)

    formats = {
        "CSV": "csv",
        "Excel (XLSX)": "xlsx",
        "JSON": "json",
        "Feather": "feather",
        "Parquet": "parquet"
    }

    col_left, col_center, col_right = st.columns([1,1,1])

    sample_df = pd.DataFrame({
        "Amount":[1200,5600,75.5,9800,300],
        "Hour":[14,3,19,1,11]
    })

    # LEFT — Download Sample
    with col_left:
        st.markdown('<div class="card"><div style="margin-bottom:8px;"><strong>Download Sample File</strong></div>', unsafe_allow_html=True)
        sample_fmt = st.selectbox("Sample Format", list(formats.keys()), key="sample_fmt")
        fmt = formats[sample_fmt]
        buf = BytesIO()
        if fmt=="csv":
            data = sample_df.to_csv(index=False).encode()
            mime="text/csv"; name="sample.csv"
        elif fmt=="xlsx":
            sample_df.to_excel(buf, index=False); data=buf.getvalue()
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"; name="sample.xlsx"
        elif fmt=="json":
            data=sample_df.to_json(orient="records").encode()
            mime="application/json"; name="sample.json"
        elif fmt=="feather":
            sample_df.to_feather(buf); data=buf.getvalue()
            mime="application/octet-stream"; name="sample.feather"
        else:
            sample_df.to_parquet(buf, index=False); data=buf.getvalue()
            mime="application/octet-stream"; name="sample.parquet"
        st.download_button("Download Sample", data, name, mime, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # CENTER — Upload & Scan
    with col_center:
        st.markdown('<div class="card"><div style="margin-bottom:8px;"><strong>Upload File to Scan</strong></div>', unsafe_allow_html=True)
        uploaded = st.file_uploader("Upload", type=["csv","xlsx","json","feather","parquet"])
        if uploaded:
            ext = uploaded.name.split(".")[-1].lower()
            if ext=="csv": df=pd.read_csv(uploaded)
            elif ext=="xlsx": df=pd.read_excel(uploaded)
            elif ext=="json": df=pd.read_json(uploaded)
            elif ext=="feather": df=pd.read_feather(uploaded)
            else: df=pd.read_parquet(uploaded)
            st.success(f"Loaded {len(df):,} rows")
            if st.button("SCAN ALL", use_container_width=True):
                with st.spinner("Scanning..."):
                    amounts = pd.to_numeric(df["Amount"], errors="coerce").fillna(100)
                    hours = pd.to_numeric(df["Hour"], errors="coerce").fillna(12).astype(int)
                    results = predict_bulk(amounts, hours)
                    final_df = pd.concat([df.reset_index(drop=True), results], axis=1)
                    suggestions = []
                    for idx, row in final_df.iterrows():
                        if row["Decision"] == "ALLOW":
                            suggestions.append("Safe — No suggestion needed")
                            continue
                        prompt = f"""
                        Fraud Transaction Detected:
                        Amount: {row['Amount']}
                        Hour: {row['Hour']}
                        Risk Level: {row['Level']}

                        Give EXACTLY 2 short suggestions to reduce fraud risk.
                        """
                        try:
                            model = genai.GenerativeModel("gemini-2.5-flash")
                            resp = model.generate_content(prompt)
                            text = resp.text.strip()
                            tips = [t.strip("-• ") for t in text.split("\n")][:2]
                            if len(tips) < 2:
                                tips += ["Avoid late night payments", "Use verified payment apps"]
                            suggestions.append(" | ".join(tips))
                        except:
                            suggestions.append("AI limit reached — Manual review required")
                    final_df["AI_Suggestions"] = suggestions
                    st.session_state.bulk_results_df = final_df
                st.success("Scan Completed!")
        st.markdown('</div>', unsafe_allow_html=True)

    # RIGHT — Download Results & Preview
    with col_right:
        st.markdown('<div class="card"><div style="margin-bottom:8px;"><strong>Download Scanned File</strong></div>', unsafe_allow_html=True)
        if st.session_state.bulk_results_df is not None:
            out_fmt = st.selectbox("Output Format", list(formats.keys()), key="out_fmt")
            fmt = formats[out_fmt]
            buf = BytesIO()
            if fmt=="csv":
                data=st.session_state.bulk_results_df.to_csv(index=False).encode()
                mime="text/csv"; name="results.csv"
            elif fmt=="xlsx":
                st.session_state.bulk_results_df.to_excel(buf, index=False); data=buf.getvalue()
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"; name="results.xlsx"
            elif fmt=="json":
                data=st.session_state.bulk_results_df.to_json(orient="records").encode()
                mime="application/json"; name="results.json"
            elif fmt=="feather":
                st.session_state.bulk_results_df.to_feather(buf); data=buf.getvalue()
                mime="application/octet-stream"; name="results.feather"
            else:
                st.session_state.bulk_results_df.to_parquet(buf, index=False); data=buf.getvalue()
                mime="application/octet-stream"; name="results.parquet"
            st.download_button("Download Results", data, name, mime, use_container_width=True)
            # preview (first 10 rows)
            st.markdown('<div style="margin-top:10px;"><strong>Preview</strong></div>', unsafe_allow_html=True)
            st.dataframe(st.session_state.bulk_results_df.head(10))
        else:
            st.markdown('<div style="color:{muted}">No scanned results yet — upload and scan to generate results.</div>'.format(muted=PALETTE["muted"]), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
