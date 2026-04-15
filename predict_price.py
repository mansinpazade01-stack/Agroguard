import os
import calendar
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from hidden_loss import analyze_farmer_decision, generate_recommendation, optimal_selling_window

# ----------------- Load data and models -----------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
df = pd.read_csv(os.path.join(DATA_DIR, "merged_cleaned_prices.csv"))
model = joblib.load(os.path.join(MODELS_DIR, "price_model.pkl"))
encoders = joblib.load(os.path.join(MODELS_DIR, "encoders.pkl"))
crop_list = list(encoders['crop'].classes_)

# ----------------- Helper for selection -----------------
def select_from_list(name, options):
    print(f"\nSelect {name}:")
    for i, option in enumerate(options):
        print(f"{i+1}. {option}")
    while True:
        try:
            idx = int(input("Enter number: ")) - 1
            if 0 <= idx < len(options):
                return options[idx]
        except ValueError:
            pass
        print("Invalid input. Try again.")

# ----------------- User Inputs -----------------
crop = select_from_list("crop", crop_list)
districts = sorted(df[df['crop'] == crop]['district'].unique())
district = select_from_list("district", districts)
states = sorted(df[df['district'] == district]['state'].unique())
state = select_from_list("state", states)
markets = sorted(df[df['district'] == district]['market'].unique())
market = select_from_list("market", markets)

while True:
    try:
        month = int(input("Enter month (1-12): "))
        if 1 <= month <= 12:
            break
    except ValueError:
        pass
    print("Invalid month. Try again.")

while True:
    try:
        year = int(input("Enter year (e.g., 2026): "))
        if year > 2000:
            break
    except ValueError:
        pass
    print("Invalid year. Try again.")

# ----------------- Encode features -----------------
encoded = [
    encoders['crop'].transform([crop])[0],
    encoders['state'].transform([state])[0],
    encoders['district'].transform([district])[0],
    encoders['market'].transform([market])[0],
    year,
    month
]

features = pd.DataFrame([encoded], columns=['crop','state','district','market','year','month'])

# ----------------- Price Prediction -----------------
predicted_price = model.predict(features)[0]
features_array = features.values
tree_preds = [tree.predict(features_array)[0] for tree in model.estimators_]
min_pred, max_pred = min(tree_preds), max(tree_preds)

print("\n--- Price Prediction ---")
print(f"Predicted future price: ₹{predicted_price:.2f}")
print(f"Expected range: ₹{min_pred:.0f} – ₹{max_pred:.0f}")

# ----------------- Current Price Input -----------------
while True:
    try:
        current_price = float(input("\nEnter current mandi price (₹/quintal): "))
        if current_price > 0:
            break
    except ValueError:
        pass
    print("Invalid price. Try again.")

quantity = 1

# ----------------- Hidden Loss Detection -----------------
result = analyze_farmer_decision(
    current_price=current_price,
    predicted_price=predicted_price,
    min_pred=min_pred,
    max_pred=max_pred,
    quantity=quantity
)

print("\n--- Farmer Decision Analysis ---")
print(result["headline"])
print(result["explanation"])
print(f"Impact per quintal: ₹{result['impact_per_quintal']}")
print(f"Total impact: ₹{result['total_impact']}")
print("Advice:", result["advice"])

# ----------------- Risk Score -----------------
range_width = max_pred - min_pred
range_percent = (range_width / predicted_price) * 100
risk_score = min(round(range_percent * 10, 1), 100)

if risk_score < 30:
    risk_level = "LOW"
    risk_message = "Price is stable. Decision is relatively safe."
elif risk_score < 60:
    risk_level = "MEDIUM"
    risk_message = "Some price fluctuation expected. Decide carefully."
else:
    risk_level = "HIGH"
    risk_message = "High price uncertainty. Decision is risky."

print("\n--- Market Risk Assessment ---")
print(f"Risk Score: {risk_score}/100")
print(f"Risk Level: {risk_level}")
print(f"Note: {risk_message}")

# ----------------- Final Recommendation -----------------
final_sentence = generate_recommendation(result["status"], risk_level)
print("\n--- Final Recommendation ---")
print(final_sentence)

# ----------------- Optimal Selling Month(s) -----------------
best_months, fallback = optimal_selling_window(
    df=df,
    crop=crop,
    district=district,
    market=market,
    months_ahead=3,
    price_col="modal_price"
)

if best_months:
    month_names = [f"{calendar.month_name[m]} (Avg: ₹{p:.2f})" for m, p in best_months]
    print(f"\n--- Optimal Selling Month(s) [{fallback}] ---")
    print("Recommended months based on historical trends:", ", ".join(month_names))
else:
    print("\nCould not determine optimal selling month (insufficient data).")

# ----------------- Visualization -----------------
subset = df[
    (df['crop'].str.strip().str.lower() == crop.strip().lower()) &
    (df['district'].str.strip().str.lower() == district.strip().lower())
]

if not subset.empty:
    subset = subset.copy()
    subset['date'] = pd.to_datetime(subset['date'], errors='coerce')
    subset = subset.dropna(subset=['date'])
    subset = subset.sort_values('date')
    plt.figure(figsize=(8,4))
    plt.plot(subset['date'], subset['modal_price'], marker='o', label='Historical Price')
    plt.axhline(predicted_price, color='red', linestyle='--', label='Predicted Price')
    plt.title(f"{crop} Price Trend in {market}, {district}")
    plt.xlabel("Date")
    plt.ylabel("Modal Price (₹/quintal)")
    plt.legend()
    plt.tight_layout()
    plt.show()
