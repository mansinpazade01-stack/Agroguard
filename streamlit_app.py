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
    
    /* INPUT STYLING */
    input, textarea, div[data-baseweb="select"] > div {
        background-color: white !important;
        border: 2px solid #166534 !important;
        border-radius: 12px !important;
        color: #1F2937 !important;
    }
    
    /* ==================== HOMEPAGE CARDS ==================== */
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
    
    /* Feature Cards (Top 3) - More Prominent */
    .feature-card {
        border: 1.8px solid rgba(22, 101, 52, 0.35);
        background: rgba(255, 255, 255, 0.88);
    }
    
    .feature-card:hover {
        border: 2px solid #4ADE80;
        box-shadow: 0 25px 50px rgba(22, 101, 52, 0.20);
    }
    
    /* ==================== OUTPUT CARDS ==================== */
    .output-card {
        background: rgba(255, 255, 255, 0.85);
        padding: 32px 28px;
        border-radius: 22px;
        border: 1.8px solid rgba(22, 101, 52, 0.30);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.10);
        backdrop-filter: blur(14px);
        margin-bottom: 25px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .output-card:hover {
        border: 1.8px solid #4ADE80;
        box-shadow: 0 20px 50px rgba(22, 101, 52, 0.18);
        transform: translateY(-4px);
    }
    
    /* BUTTONS */
    .stButton > button {
        background: linear-gradient(90deg, #166534, #4ADE80);
        color: white;
        font-weight: 700;
        font-size: 18px;
        padding: 14px 32px;
        border-radius: 50px;
        border: none;
        box-shadow: 0 8px 25px rgba(22, 101, 52, 0.35);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(22, 101, 52, 0.45);
        background: linear-gradient(90deg, #14532D, #22C55E);
    }
    
    .feature-title {
        font-size: 23px;
        font-weight: 700;
        color: #166534;
        margin-bottom: 12px;
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

defaults = {"crop": None, "state": None, "district": None, "market": None, 
            "pred": None, "price": None, "date": None}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =========================
# PAGE 1: HOME
# =========================
if st.session_state.page == "welcome":

    st.markdown("""
    <div style='text-align:center; margin-bottom: 30px;'>
        <h1 style='font-size: 54px; margin-bottom: 10px;'>🌾 AgroGuard AI</h1>
        <h2 style='color: #166534; font-weight: 600;'>Smarter Decisions. Better Profits.</h2>
        <p style='font-size: 18.5px; color: #14532D; max-width: 720px; margin: 15px auto 0;'>
            Empowering farmers and traders with AI-driven insights for better selling decisions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Main Feature Cards
    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        st.markdown("""
        <div class="premium-card feature-card">
            <h3 class="feature-title">📊 Price Prediction</h3>
            <p>Get accurate future price forecasts for your specific market and date.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="premium-card feature-card">
            <h3 class="feature-title">📈 Trend Analysis</h3>
            <p>Visualize historical trends and future price movements clearly.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="premium-card feature-card">
            <h3 class="feature-title">💡 Smart Advice</h3>
            <p>Receive clear Sell Now or Wait recommendations with reasoning.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Info Cards
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("""
        <div class="premium-card">
            <h4>🤔 What does this app do?</h4>
            <p>Predicts crop prices using real market data to help you make profitable selling decisions.</p>
        </div>
        <div class="premium-card">
            <h4>💡 How can this help me?</h4>
            <p>Shows whether prices are likely to rise or fall in the coming days.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="premium-card">
            <h4>📊 Is this reliable?</h4>
            <p>Yes. Trained on real government APMC market data from Maharashtra.</p>
        </div>
        <div class="premium-card">
            <h4>🧑‍🌾 Need technical knowledge?</h4>
            <p>No. Simple and easy to use for every farmer.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div class="premium-card" style='text-align:center;'>
        <p style='font-size:18px; color:#166534; margin-bottom:8px;'>
            Data-driven • AI-powered • Built for Maharashtra farmers
        </p>
        <p style='font-style:italic; font-size:17px; color:#14532D;'>
            "Better data leads to better decisions and higher profits."
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Start Predicting Now", use_container_width=True):
        st.session_state.page = "input"
        st.rerun()

# =========================
# PAGE 2: INPUT
# =========================
elif st.session_state.page == "input":

    col_back, _ = st.columns([1, 6])
    with col_back:
        if st.button("⬅️ Back to Home"):
            st.session_state.page = "welcome"
            st.rerun()

    st.markdown("<h2 style='color:#166534; margin-bottom:20px;'>📥 Enter Crop Details</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        crop = st.selectbox("Crop", encoders['crop'].classes_, key="crop_input")
        district = st.selectbox("District", encoders['district'].classes_, key="district_input")

    with col2:
        state = st.selectbox("State", encoders['state'].classes_, key="state_input")
        market = st.selectbox("Market", encoders['market'].classes_, key="market_input")

    st.markdown("---")

    date = st.date_input("Select Date", datetime.date.today(), key="date_input")
    price = st.text_input("Current Price (₹)", placeholder="e.g. 1200", key="price_input")

    if st.button("🔮 Predict Price", use_container_width=True, type="primary"):
     if not price.strip():
        st.error("Please enter the current price")
     else:
        try:
            current_price = float(price)

            st.session_state.crop = crop
            st.session_state.state = state
            st.session_state.district = district
            st.session_state.market = market
            st.session_state.date = date
            st.session_state.price = current_price

            # Encoding
            crop_e = encoders['crop'].transform([crop])[0]
            state_e = encoders['state'].transform([state])[0]
            district_e = encoders['district'].transform([district])[0]
            market_e = encoders['market'].transform([market])[0]

            # 9 features (MATCH BACKEND)
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

            st.session_state.pred = float(pred)
            st.session_state.page = "result"
            st.rerun()

        except ValueError:
            st.error("Please enter a valid numeric price")
        except Exception as e:
            st.error(f"Prediction error: {str(e)}")
            
# =========================
# PAGE 3: RESULT
# =========================
elif st.session_state.page == "result":

    pred = st.session_state.pred
    price = st.session_state.price

    # SAFETY CHECK
    if pred is None or price is None:
        st.error("Missing prediction data. Please try again.")
        st.stop()

    diff = pred - price
    confidence = max(0, min(100, 100 - abs(diff) / max(price, 1) * 100))

    # Output Cards
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="output-card">
            <h3 style='margin:0; color:#166534;'>💰 Predicted Price</h3>
            <h1 style='margin:12px 0 0; color:#15803D; font-size:46px;'>₹ {pred:.2f}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="output-card">
            <h3 style='margin-bottom:8px;'>Confidence Level</h3>
            <h2 style='color:#166534; margin:0;'>{confidence:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)

    # =========================
    # DECISION ENGINE
    # =========================

    if diff < -15:
        decision = "SELL NOW"
        color = "#B91C1C"
        trend = "⬇️ Downtrend"
        explanation = "Price may drop. Selling now can secure profit."
        quote = "Don’t wait for the market to fall — smart farmers act early."

    elif diff > 25:
        decision = "WAIT & WATCH"
        color = "#166534"
        trend = "⬆️ Uptrend"
        explanation = "Price may increase. Waiting could give better returns."
        quote = "Patience today can turn into profit tomorrow."

    else:
        decision = "HOLD"
        color = "#854D0E"
        trend = "➡️ Stable Market"
        explanation = "Market is stable. Monitor price changes."
        quote = "Stay alert — stable markets can shift anytime."

    # Decision Card
    st.markdown(f"""
    <div class="output-card">
        <h2 style='color:{color}; font-size:38px; margin:0;'>{decision}</h2>
        <p style='font-size:18px; margin-top:12px; color:#374151;'>{quote}</p>
    </div>
    """, unsafe_allow_html=True)

    # Insight Card
    st.markdown(f"""
    <div class="output-card" style="text-align:left;">
        <h3 style="color:#166534;">📊 Market Insight</h3>
        <p><b>Trend:</b> {trend}</p>
        <p><b>Why this prediction?</b><br>{explanation}</p>
    </div>
    """, unsafe_allow_html=True)

    # Summary
    st.markdown(f"""
    <div style='background:#F1F5F9; padding:18px; border-radius:14px; margin:25px 0; font-size:15.5px;'>
        <strong>Prediction Details:</strong> {st.session_state.crop} • 
        {st.session_state.district}, {st.session_state.state} • 
        Market: {st.session_state.market} • Date: {st.session_state.date}
    </div>
    """, unsafe_allow_html=True)

    # SAFE FILTER
    filtered = pd.DataFrame()

    if all([
        st.session_state.crop,
        st.session_state.state,
        st.session_state.district
    ]):
        filtered = df[
            (df['crop'].str.lower() == str(st.session_state.crop).lower()) &
            (df['state'].str.lower() == str(st.session_state.state).lower()) &
            (df['district'].str.lower() == str(st.session_state.district).lower())
        ]

    # Chart
    if not filtered.empty:
        fig = px.line(
            filtered,
            x="date",
            y="modal_price",
            markers=True,
            title=f"Historical Price Trend - {st.session_state.crop} ({st.session_state.district})"
        )

        fig.update_layout(
            yaxis_title="Price (₹)",
            xaxis_title="Date",
            height=520,
            template="plotly_white",
            title_font_size=18
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("No historical data found for this crop-district combination.")

    # Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔁 Predict Another Crop", use_container_width=True):
            st.session_state.page = "input"
            st.rerun()