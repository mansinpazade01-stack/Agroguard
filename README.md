🌾 AgroGuard
Intelligence that Secures Every Harvest

AgroGuard is an AI-powered web application built using Streamlit that helps farmers and stakeholders make informed decisions by predicting crop prices, analyzing market trends, and suggesting optimal selling strategies.

🚀 Features
💰 Price Prediction
Predict future crop prices based on selected date, crop, district, and market.
📊 Market Trend Analysis
Visualize monthly price trends for a selected year.
⚠️ Risk Analysis
Calculates risk score based on price difference.
🌾 Smart Recommendation
Suggests whether to sell now or wait using AI insights.
📅 Optimal Selling Months
Identifies best months to sell crops based on historical data.
🎨 Modern UI Dashboard
Eco-friendly design with interactive panels and animations.
🧠 How It Works
User selects:
Crop 🌱
District 📍
Market 🏪
State 🏙️
Date 📅
Current Price 💰
The system:
Encodes inputs using trained encoders
Uses a Machine Learning model to predict price
Compares predicted vs current price
Output:
Predicted price
Risk level
Profit/Loss impact
Recommendation (Sell/Wait)
📊 Graph Explanation
The graph shows monthly average prices for a selected year
Helps identify:
📈 High price months
📉 Low price periods
Used for better selling decisions
🛠️ Tech Stack
Frontend: Streamlit
Backend: Python
Libraries:
Pandas
Joblib
Scikit-learn
Visualization: Streamlit Charts
📁 Project Structure
SmartAgroGuard/
│── streamlit_app.py
│── background.jpg
│
├── models/
│   ├── price_model.pkl
│   └── encoders.pkl
│
├── data/
│   └── merged_cleaned_prices.csv
│
└── README.md
▶️ How to Run
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py
🎯 Use Case
Helps farmers decide:
When to sell crops
Which market is profitable
Reduces losses due to price fluctuations
Supports data-driven agriculture
📌 Future Enhancements
🌦️ Weather integration
📈 Future price forecasting graph
🤖 AI chatbot assistant
📱 Mobile-friendly UI
👩‍💻 Author

Mansi Pazade Yashfeen Mansuri Pranali Dalvi Niyati Raval

⭐ Acknowledgement

This project aims to empower farmers using AI and data-driven decision-making for better agricultural outcomes.
