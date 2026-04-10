"""
app.py — Rain Tomorrow Classifier — Streamlit Frontend
=======================================================
Premium Streamlit UI for predicting whether it will rain tomorrow in Australia.
"""

import os
import numpy as np
import pandas as pd
import joblib
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import date

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="☁️ Rain Tomorrow — Australia",
    page_icon="🌧️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ---- Google Font ---- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ---- Dark gradient background ---- */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    min-height: 100vh;
}

/* ---- Sidebar ---- */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.04);
    border-right: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
}
section[data-testid="stSidebar"] * {
    color: #e0e0f0 !important;
}

/* ---- Glass card ---- */
.glass-card {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 28px;
    backdrop-filter: blur(14px);
    margin-bottom: 20px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.glass-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(100,80,255,0.25);
}

/* ---- Hero title ---- */
.hero-title {
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
    line-height: 1.1;
}
.hero-sub {
    font-size: 1.1rem;
    color: rgba(220,220,255,0.65);
    margin-top: 6px;
    font-weight: 400;
}

/* ---- Metric pills ---- */
.metric-pill {
    display: inline-block;
    background: rgba(167,139,250,0.18);
    border: 1px solid rgba(167,139,250,0.35);
    border-radius: 999px;
    padding: 4px 18px;
    font-size: 0.82rem;
    color: #c4b5fd;
    font-weight: 600;
    margin-right: 8px;
    margin-bottom: 6px;
}

/* ---- Prediction box ---- */
.rain-box {
    background: linear-gradient(135deg, #1e3a5f 0%, #1a2a4a 100%);
    border: 2px solid #60a5fa;
    border-radius: 22px;
    padding: 36px;
    text-align: center;
    box-shadow: 0 0 40px rgba(96,165,250,0.3);
}
.no-rain-box {
    background: linear-gradient(135deg, #1a3a2f 0%, #143327 100%);
    border: 2px solid #34d399;
    border-radius: 22px;
    padding: 36px;
    text-align: center;
    box-shadow: 0 0 40px rgba(52,211,153,0.3);
}
.pred-emoji { font-size: 4.5rem; }
.pred-label {
    font-size: 2.2rem;
    font-weight: 800;
    margin: 10px 0;
    color: #f0f4ff;
}
.pred-prob {
    font-size: 1rem;
    color: rgba(200,220,255,0.7);
}

/* ---- Section heading ---- */
.section-heading {
    font-size: 1.15rem;
    font-weight: 700;
    color: #a78bfa;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 14px;
    padding-bottom: 6px;
    border-bottom: 1px solid rgba(167,139,250,0.25);
}

/* ---- Streamlit widget overrides ---- */
.stSlider > div[data-baseweb="slider"] { color: #a78bfa; }
label { color: #c8c8ef !important; font-weight: 500 !important; }
.stSelectbox > div { border-color: rgba(167,139,250,0.3) !important; }
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    color: white !important;
    border: none;
    border-radius: 14px;
    padding: 14px 36px;
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    width: 100%;
    transition: opacity 0.2s, transform 0.15s;
}
.stButton > button:hover {
    opacity: 0.88;
    transform: translateY(-2px);
}

/* ---- Developer credit ---- */
.dev-credit {
    color: rgba(200,200,240,0.4);
    font-size: 0.78rem;
    text-align: center;
    margin-top: 30px;
}

div[data-testid="stMetricValue"] { font-size: 1.6rem !important; font-weight: 700 !important; color: #a78bfa !important; }
div[data-testid="stMetricLabel"] { color: rgba(200,200,240,0.75) !important; }
</style>
""", unsafe_allow_html=True)

# ── Load Artifacts ────────────────────────────────────────────────────────────
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")

@st.cache_resource(show_spinner=True)
def load_artifacts():
    model    = joblib.load(os.path.join(MODEL_DIR, "model.pkl"))
    scaler   = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
    les      = joblib.load(os.path.join(MODEL_DIR, "label_encoders.pkl"))
    tgt_le   = joblib.load(os.path.join(MODEL_DIR, "target_encoder.pkl"))
    meta     = joblib.load(os.path.join(MODEL_DIR, "metadata.pkl"))
    return model, scaler, les, tgt_le, meta

# ── Wind direction options ────────────────────────────────────────────────────
WIND_DIRS = ['E','ENE','ESE','N','NE','NNE','NNW','NW','S','SE','SSE','SSW','SW','W','WNW','WSW','W','NA']
WIND_DIRS = sorted(set(WIND_DIRS))

LOCATIONS = [
    'Adelaide','Albany','Albury','AliceSprings','BadgerysCreek','Ballarat',
    'Bendigo','Brisbane','Cairns','Canberra','Cobar','CoffsHarbour',
    'Dartmoor','Darwin','GoldCoast','Hobart','Katherine','Launceston',
    'Melbourne','MelbourneAirport','Mildura','Moree','MountGambier',
    'MountGinini','Newcastle','Nhil','NorahHead','NorfolkIsland','Nuriootpa',
    'PearceRAAF','Penrith','Perth','PerthAirport','Portland','Richmond',
    'Sale','SalmonGums','Sydney','SydneyAirport','Townsville','Tuggeranong',
    'Uluru','WaggaWagga','Walpole','Watsonia','Williamtown',
    'Witchcliffe','Wollongong','Woomera'
]

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:20px 0 10px 0;'>
        <div style='font-size:3rem;'>🌦️</div>
        <div style='font-size:1.2rem; font-weight:700; background: linear-gradient(90deg,#a78bfa,#60a5fa);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>Rain Tomorrow</div>
        <div style='font-size:0.75rem; color:rgba(200,200,255,0.5); margin-top:4px;'>Australia Weather Predictor</div>
    </div>
    <hr style='border-color:rgba(255,255,255,0.1); margin:10px 0 20px 0;'>
    """, unsafe_allow_html=True)

    # Check if model is trained
    model_ready = os.path.exists(os.path.join(MODEL_DIR, "model.pkl"))

    if model_ready:
        model, scaler, les, tgt_le, meta = load_artifacts()
        metrics = meta.get("metrics", {})

        st.markdown("**📊 Model Performance**")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Accuracy", f"{metrics.get('accuracy',0)*100:.1f}%")
            st.metric("F1 Score", f"{metrics.get('f1_score',0)*100:.1f}%")
        with col2:
            st.metric("ROC-AUC", f"{metrics.get('roc_auc',0)*100:.1f}%")
            st.metric("Algorithm", "RF")

        st.markdown("""
        <div style='margin-top:16px; padding:14px; background:rgba(52,211,153,0.1);
                    border:1px solid rgba(52,211,153,0.3); border-radius:12px;'>
            <span style='color:#34d399; font-size:0.85rem; font-weight:600;'>✓ Model Ready</span><br>
            <span style='color:rgba(200,240,200,0.6); font-size:0.75rem;'>Random Forest · 200 estimators</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Model not trained yet!")
        st.info("Run `python training.py` first to train and save the model.")

    st.markdown("---")
    st.markdown("""
    <div style='color:rgba(200,200,255,0.5); font-size:0.78rem; line-height:1.6;'>
    <b style='color:rgba(200,200,255,0.8);'>Dataset:</b> weatherAUS.csv<br>
    <b style='color:rgba(200,200,255,0.8);'>Records:</b> ~145,000<br>
    <b style='color:rgba(200,200,255,0.8);'>Features:</b> 22 weather variables<br>
    <b style='color:rgba(200,200,255,0.8);'>Locations:</b> 49 Australian cities
    </div>
    """, unsafe_allow_html=True)

# ── Main Layout ───────────────────────────────────────────────────────────────
# Hero
st.markdown("""
<div class='glass-card'>
    <div class='hero-title'>🌧️ Will It Rain Tomorrow?</div>
    <div class='hero-sub'>Enter today's weather observations for any Australian city and get an instant AI-powered prediction.</div>
</div>
""", unsafe_allow_html=True)

if not model_ready:
    st.error("🚫 Model not found. Please run `python training.py` first, then refresh this page.")
    st.stop()

# ── Input Form ────────────────────────────────────────────────────────────────
st.markdown("<div class='section-heading'>📋 Today's Weather Observations</div>", unsafe_allow_html=True)

# Row 1 — Location & Date
col_loc, col_month, col_rain = st.columns([2, 1, 1])
with col_loc:
    location = st.selectbox("🏙️ Location", LOCATIONS, index=LOCATIONS.index("Sydney") if "Sydney" in LOCATIONS else 0)
with col_month:
    month = st.selectbox("📅 Month", list(range(1, 13)),
                         format_func=lambda m: date(2000, m, 1).strftime("%B"),
                         index=date.today().month - 1)
with col_rain:
    rain_today = st.selectbox("🌧️ Rain Today?", ["No", "Yes"])

st.markdown("---")

# Temperature
st.markdown("<div class='section-heading'>🌡️ Temperature & Rainfall</div>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
with c1: min_temp  = st.number_input("Min Temp (°C)",   -10.0, 50.0, 12.0, 0.1)
with c2: max_temp  = st.number_input("Max Temp (°C)",   -10.0, 55.0, 25.0, 0.1)
with c3: temp_9am  = st.number_input("Temp 9am (°C)",   -10.0, 50.0, 17.0, 0.1)
with c4: temp_3pm  = st.number_input("Temp 3pm (°C)",   -10.0, 50.0, 23.0, 0.1)

c5, c6, c7, c8 = st.columns(4)
with c5: rainfall    = st.number_input("Rainfall (mm)",    0.0, 400.0, 0.0, 0.1)
with c6: evaporation = st.number_input("Evaporation (mm)", 0.0,  150.0, 5.0, 0.1)
with c7: sunshine    = st.number_input("Sunshine (hrs)",   0.0,   15.0, 8.0, 0.1)

# Humidity & Cloud
st.markdown("<div class='section-heading'>💧 Humidity & Cloud Cover</div>", unsafe_allow_html=True)
c9, c10, c11, c12 = st.columns(4)
with c9:  hum9am  = st.slider("Humidity 9am (%)",  0, 100, 65)
with c10: hum3pm  = st.slider("Humidity 3pm (%)",  0, 100, 40)
with c11: cloud9am = st.slider("Cloud 9am (oktas)", 0, 9, 3)
with c12: cloud3pm = st.slider("Cloud 3pm (oktas)", 0, 9, 3)

# Pressure
st.markdown("<div class='section-heading'>🔵 Atmospheric Pressure</div>", unsafe_allow_html=True)
c13, c14 = st.columns(2)
with c13: pressure9am = st.number_input("Pressure 9am (hPa)", 970.0, 1045.0, 1015.0, 0.1)
with c14: pressure3pm = st.number_input("Pressure 3pm (hPa)", 970.0, 1045.0, 1013.0, 0.1)

# Wind
st.markdown("<div class='section-heading'>💨 Wind Conditions</div>", unsafe_allow_html=True)
cw1, cw2, cw3, cw4, cw5 = st.columns(5)
with cw1: wind_gust_dir  = st.selectbox("Gust Dir",     WIND_DIRS, index=WIND_DIRS.index("W") if "W" in WIND_DIRS else 0)
with cw2: wind_gust_spd  = st.number_input("Gust Speed (km/h)", 0, 150, 44, 1)
with cw3: wind_dir_9am   = st.selectbox("Dir 9am",      WIND_DIRS, index=WIND_DIRS.index("W") if "W" in WIND_DIRS else 0)
with cw4: wind_dir_3pm   = st.selectbox("Dir 3pm",      WIND_DIRS, index=WIND_DIRS.index("WNW") if "WNW" in WIND_DIRS else 0)
with cw5: wind_spd_9am   = st.number_input("Speed 9am (km/h)", 0, 130, 20, 1)
_, cw6, _ = st.columns([2, 1, 2])
with cw6: wind_spd_3pm = st.number_input("Speed 3pm (km/h)", 0, 130, 24, 1)

st.markdown("<br>", unsafe_allow_html=True)

# ── Predict Button ────────────────────────────────────────────────────────────
_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    predict_clicked = st.button("🔮 Predict Rain Tomorrow", use_container_width=True)

# ── Prediction Logic ──────────────────────────────────────────────────────────
if predict_clicked:
    feature_cols     = meta["feature_cols"]
    numerical_cols   = meta["numerical_cols"]
    categorical_cols = meta["categorical_cols"]

    raw_input = {
        "MinTemp":        min_temp,
        "MaxTemp":        max_temp,
        "Rainfall":       rainfall,
        "Evaporation":    evaporation,
        "Sunshine":       sunshine,
        "WindGustSpeed":  wind_gust_spd,
        "WindSpeed9am":   wind_spd_9am,
        "WindSpeed3pm":   wind_spd_3pm,
        "Humidity9am":    hum9am,
        "Humidity3pm":    hum3pm,
        "Pressure9am":    pressure9am,
        "Pressure3pm":    pressure3pm,
        "Cloud9am":       cloud9am,
        "Cloud3pm":       cloud3pm,
        "Temp9am":        temp_9am,
        "Temp3pm":        temp_3pm,
        "Month":          month,
        "Location":       location,
        "WindGustDir":    wind_gust_dir,
        "WindDir9am":     wind_dir_9am,
        "WindDir3pm":     wind_dir_3pm,
        "RainToday":      rain_today,
    }

    # Encode categoricals
    encoded = dict(raw_input)
    for col in categorical_cols:
        le = les[col]
        val = str(encoded[col])
        if val in le.classes_:
            encoded[col] = le.transform([val])[0]
        else:
            encoded[col] = 0  # fallback for unseen labels

    # Build feature vector in the correct order
    feature_vector = np.array([[encoded[col] for col in feature_cols]])
    feature_vector_sc = scaler.transform(feature_vector)

    # Predict
    prob    = model.predict_proba(feature_vector_sc)[0]
    pred_id = np.argmax(prob)
    pred_label = tgt_le.classes_[pred_id]
    rain_prob  = prob[tgt_le.transform(["Yes"])[0]]
    no_rain_prob = 1 - rain_prob

    # ── Result Display ─────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("<div class='section-heading'>🎯 Prediction Result</div>", unsafe_allow_html=True)

    res_col, gauge_col = st.columns([1, 1])

    with res_col:
        if pred_label == "Yes":
            st.markdown(f"""
            <div class='rain-box'>
                <div class='pred-emoji'>🌧️</div>
                <div class='pred-label'>Yes — It Will Rain!</div>
                <div class='pred-prob'>Rain Probability: <b style='color:#60a5fa;'>{rain_prob*100:.1f}%</b></div>
                <div style='margin-top:14px; padding: 10px; background:rgba(96,165,250,0.12);
                            border-radius:10px; color:rgba(200,220,255,0.8); font-size:0.9rem;'>
                    🧥 Don't forget your umbrella — there's a strong chance of rain in {location} tomorrow!
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='no-rain-box'>
                <div class='pred-emoji'>☀️</div>
                <div class='pred-label'>No — Skies Clear!</div>
                <div class='pred-prob'>No-Rain Probability: <b style='color:#34d399;'>{no_rain_prob*100:.1f}%</b></div>
                <div style='margin-top:14px; padding: 10px; background:rgba(52,211,153,0.12);
                            border-radius:10px; color:rgba(200,240,220,0.8); font-size:0.9rem;'>
                    🌞 Looking clear for {location} tomorrow. Enjoy the sunshine!
                </div>
            </div>
            """, unsafe_allow_html=True)

    with gauge_col:
        # Gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=rain_prob * 100,
            delta={"reference": 50, "suffix": "%"},
            title={"text": "Rain Probability (%)", "font": {"color": "#c4b5fd", "size": 16}},
            number={"suffix": "%", "font": {"color": "#f0f4ff", "size": 36}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#888"},
                "bar":  {"color": "#60a5fa" if rain_prob >= 0.5 else "#34d399"},
                "bgcolor": "rgba(255,255,255,0.05)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0,  30], "color": "rgba(52,211,153,0.2)"},
                    {"range": [30, 60], "color": "rgba(250,204,21,0.15)"},
                    {"range": [60,100], "color": "rgba(96,165,250,0.25)"},
                ],
                "threshold": {
                    "line": {"color": "#a78bfa", "width": 3},
                    "thickness": 0.75,
                    "value": 50,
                },
            }
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor ="rgba(0,0,0,0)",
            font_color   ="#c4b5fd",
            height=310,
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Key Inputs Summary ────────────────────────────────────────────────
    st.markdown("<br><div class='section-heading'>📌 Key Input Summary</div>", unsafe_allow_html=True)
    s1, s2, s3, s4, s5, s6 = st.columns(6)
    s1.metric("Min Temp",  f"{min_temp}°C")
    s2.metric("Max Temp",  f"{max_temp}°C")
    s3.metric("Humidity 3pm", f"{hum3pm}%")
    s4.metric("Rainfall",  f"{rainfall} mm")
    s5.metric("Pressure 3pm", f"{pressure3pm} hPa")
    s6.metric("Sunshine",  f"{sunshine} hrs")

    # ── Feature Contribution Bar Chart ────────────────────────────────────
    st.markdown("<br><div class='section-heading'>🔑 Top Feature Importances (Model-Level)</div>", unsafe_allow_html=True)
    feat_imp = meta.get("feature_importance", [])
    if feat_imp:
        fi_df = pd.DataFrame(feat_imp).head(12)
        fig2 = px.bar(
            fi_df[::-1],
            x="Importance", y="Feature",
            orientation="h",
            color="Importance",
            color_continuous_scale=["#34d399","#60a5fa","#a78bfa","#f472b6"],
            template="plotly_dark",
        )
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor ="rgba(0,0,0,0)",
            coloraxis_showscale=False,
            yaxis_title="",
            xaxis_title="Importance Score",
            height=380,
            margin=dict(l=10, r=10, t=10, b=20),
            font=dict(color="#c8c8ef", size=13),
        )
        fig2.update_traces(marker_line_width=0)
        st.plotly_chart(fig2, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='dev-credit'>
    Built with ❤️ using Random Forest · Streamlit · Plotly<br>
    Dataset: Bureau of Meteorology — Australia (weatherAUS)
</div>
""", unsafe_allow_html=True)
