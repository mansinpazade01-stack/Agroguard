import streamlit as st
import pandas as pd
import joblib

# =========================
# PAGE SETTINGS
# =========================
st.set_page_config(page_title="AgroGuard", layout="centered")

# =========================
# LOAD MODEL + ENCODERS
# =========================
@st.cache_resource
def load_model():
    try:
        model = joblib.load("models/price_model.pkl")
        encoders = joblib.load("models/encoders.pkl")
        return model, encoders
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        return None, None

model, encoders = load_model()

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/merged_cleaned_prices.csv")
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        return df
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

# =========================
# UI HEADER
# =========================
st.title("🌾 AgroGuard - Crop Price Predictor")
st.markdown("### 📊 Predict prices & detect hidden loss")
st.markdown("---")

# =========================
# INPUT SECTION
# =========================
st.subheader("📥 Enter Crop Details")

if df.empty:
    st.error("Dataset not loaded properly")
    st.stop()

col1, col2 = st.columns(2)

with col1:
    crop = st.selectbox("🌱 Select Crop", sorted(df['crop'].dropna().unique()))
    state = st.selectbox("🏙️ Select State", sorted(df['state'].dropna().unique()))

with col2:
    district = st.selectbox("📍 Select District", sorted(df['district'].dropna().unique()))
    market = st.selectbox("🏪 Select Market", sorted(df['market'].dropna().unique()))

date = st.date_input("📅 Select Date")

year = date.year
month = date.month

# =========================
# PREDICTION FUNCTION
# =========================
def predict_price(crop, state, district, market, year, month):
    try:
        crop_enc = encoders['crop'].transform([crop])[0]
        state_enc = encoders['state'].transform([state])[0]
        district_enc = encoders['district'].transform([district])[0]
        market_enc = encoders['market'].transform([market])[0]

        input_data = pd.DataFrame([{
            'crop': crop_enc,
            'state': state_enc,
            'district': district_enc,
            'market': market_enc,
            'year': year,
            'month': month
        }])

        prediction = model.predict(input_data)[0]
        return round(prediction, 2)

    except Exception as e:
        st.error(f"❌ Prediction error: {e}")
        return None

# =========================
# LOSS FUNCTION
# =========================
def calculate_loss(predicted_price, market_avg):
    return round(market_avg - predicted_price, 2)

# =========================
# BUTTON ACTION
# =========================
if st.button("🚀 Predict Price"):

    if model is None or encoders is None:
        st.error("❌ Model not loaded properly")
    else:
        predicted_price = predict_price(crop, state, district, market, year, month)

        if predicted_price is not None:

            st.success(f"💰 Predicted Price: ₹ {predicted_price}")

            # MARKET COMPARISON
            try:
                market_avg = df[
                    (df['crop'] == crop) &
                    (df['state'] == state) &
                    (df['district'] == district) &
                    (df['market'] == market)
                ]['modal_price'].mean()

                if pd.notnull(market_avg):

                    st.write(f"📊 Market Average Price: ₹ {round(market_avg, 2)}")

                    loss = calculate_loss(predicted_price, market_avg)

                    if loss > 0:
                        st.warning(f"⚠️ Hidden Loss: ₹ {loss} (You may be underpricing!)")
                    else:
                        st.info("✅ No loss detected. Good pricing!")

                else:
                    st.info("ℹ️ No market data available")

            except Exception as e:
                st.error(f"❌ Error calculating market comparison: {e}")

# =========================
# VISUALIZATION
# =========================
st.markdown("---")
st.subheader("📈 Price Trend")

if st.checkbox("Show Crop Trend"):

    crop_data = df[df['crop'] == crop]

    if not crop_data.empty:
        trend = crop_data.groupby('year')['modal_price'].mean()
        st.line_chart(trend)
    else:
        st.info("No data available for selected crop")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("💡 AgroGuard helps farmers make better pricing decisions using AI.")