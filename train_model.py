import streamlit as st
import joblib
import numpy as np
import os
import datetime
import pandas as pd
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="AgroGuard AI", layout="wide", initial_sidebar_state="collapsed")

# =========================
# FINAL MODERN GLASSMORPHISM THEME
# =========================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #F0FDF4, #DCFCE7);
    }

    h1, h2, h3 {
        color: #166534 !important;
    }

    input, textarea, div[data-baseweb="select"] > div {
        background-color: white !important;
        border: 2px solid #166534 !important;
        border-radius: 12px !important;
        color: #1F2937 !important;
    }

    .premium-card {
        background: rgba(255, 255, 255, 0.78);
        padding: 28px 24px;
        border-radius: 20px;
        border: 1.5px solid rgba(22, 101, 52, 0.25);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        backdrop-filter: blur(12px);
        transition: all 0.35s ease;
        height: 100%;
    }

    .premium-card:hover {
        transform: translateY(-8px);
        border: 1.5px solid #4ADE80;
        box-shadow: 0 20px 45px rgba(22, 101, 52, 0.18);
    }

    .feature-card {
        border: 1.8px solid rgba(22, 101, 52, 0.35);
        background: rgba(255, 255, 255, 0.88);
    }

    .feature-card:hover {
        border: 2px solid #4ADE80;
        box-shadow: 0 25px 50px rgba(22, 101, 52, 0.20);
    }

    .output-card {
        background: rgba(255, 255, 255, 0.85);
        padding: 32px 28px;
        border-radius: 22px;
        border: 1.8px solid rgba(22, 101, 52, 0.30);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.10);
        backdrop-filter: blur(14px);
        margin-bottom: 25px;
        text-align: center;
    }

    .stButton > button {
        background: linear-gradient(90deg, #166534, #4ADE80);
        color: white;
        font-weight: 700;
        font-size: 18px;
        padding: 14px 32px;
        border-radius: 50px;
        border: none;
        box-shadow: 0 8px 25px rgba(22, 101, 52, 0.35);
    }
</style>
""", unsafe_allow_html=True)

# =========================
# LOAD MODELS & DATA
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, "models", "price_model.pkl"))
encoders = joblib.load(os.path.join(BASE_DIR, "models", "encoders.pkl"))
df = pd.read_csv(os.path.join(BASE_DIR, "data", "merged_cleaned_prices.csv"))
df['date'] = pd.to_datetime(df['date'])

# =========================
# SESSION STATE
# =========================
if "page" not in st.session_state:
    st.session_state.page = "welcome"

for k in ["crop", "state", "district", "market", "pred", "price", "date"]:
    if k not in st.session_state:
        st.session_state[k] = None

# =========================
# PAGE 1 - HOME
# =========================
if st.session_state.page == "welcome":

    st.markdown("""
    <div style='text-align:center;'>
        <h1>🌾 AgroGuard AI</h1>
        <h2>Smarter Decisions. Better Profits.</h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="premium-card feature-card"><h3>📊 Price Prediction</h3></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="premium-card feature-card"><h3>📈 Trend Analysis</h3></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="premium-card feature-card"><h3>💡 Smart Advice</h3></div>', unsafe_allow_html=True)

    if st.button("🚀 Start Predicting Now"):
        st.session_state.page = "input"
        st.rerun()

# =========================
# PAGE 2 - INPUT
# =========================
elif st.session_state.page == "input":

    if st.button("⬅️ Back"):
        st.session_state.page = "welcome"
        st.rerun()

    st.markdown("## 📥 Enter Crop Details")

    col1, col2 = st.columns(2)

    with col1:
        crop = st.selectbox("Crop", encoders['crop'].classes_)
        district = st.selectbox("District", encoders['district'].classes_)

    with col2:
        state = st.selectbox("State", encoders['state'].classes_)
        market = st.selectbox("Market", encoders['market'].classes_)

    date = st.date_input("Select Date", datetime.date.today())
    price = st.text_input("Current Price (₹)")

    # =========================
    # 🔥 FINAL PREDICTION BLOCK (FIXED)
    # =========================
    if st.button("🔮 Predict Price", use_container_width=True, type="primary"):

        if not price.strip():
            st.error("Please enter the current price")
        else:
            try:
                current_price = float(price)

                crop_e = encoders['crop'].transform([crop])[0]
                state_e = encoders['state'].transform([state])[0]
                district_e = encoders['district'].transform([district])[0]
                market_e = encoders['market'].transform([market])[0]

                features = np.array([[
                    crop_e,
                    state_e,
                    district_e,
                    market_e,
                    date.year,
                    date.month,
                    current_price,
                    current_price,
                    current_price
                ]])

                pred = model.predict(features)[0]

                st.session_state.crop = crop
                st.session_state.state = state
                st.session_state.district = district
                st.session_state.market = market
                st.session_state.date = date
                st.session_state.price = current_price
                st.session_state.pred = float(pred)

                st.session_state.page = "result"
                st.rerun()

            except Exception as e:
                st.error(f"Error: {str(e)}")

# =========================
# PAGE 3 - RESULT
# =========================
elif st.session_state.page == "result":

    pred = st.session_state.pred
    price = st.session_state.price

    diff = pred - price
    confidence = max(0, min(100, 100 - abs(diff) / max(price, 1) * 100))

    st.markdown(f"""
    <div class="output-card">
        <h3>💰 Predicted Price</h3>
        <h1>₹ {pred:.2f}</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="output-card">
        <h3>Confidence</h3>
        <h2>{confidence:.1f}%</h2>
    </div>
    """, unsafe_allow_html=True)

    decision = "HOLD"
    if diff < 0:
        decision = "SELL NOW"
    elif diff > 0:
        decision = "WAIT"

    st.markdown(f"""
    <div class="output-card">
        <h2>{decision}</h2>
    </div>
    """, unsafe_allow_html=True)

    filtered = df[
        (df['crop'].str.lower() == st.session_state.crop.lower()) &
        (df['state'].str.lower() == st.session_state.state.lower()) &
        (df['district'].str.lower() == st.session_state.district.lower())
    ]

    if not filtered.empty:
        fig = px.line(filtered, x="date", y="modal_price", markers=True)
        st.plotly_chart(fig, use_container_width=True)

    if st.button("🔁 Predict Again"):
        st.session_state.page = "input"
        st.rerun()