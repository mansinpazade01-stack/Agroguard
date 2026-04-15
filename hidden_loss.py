# hidden_loss.py

import pandas as pd
import calendar

def analyze_farmer_decision(current_price, predicted_price, min_pred, max_pred, quantity=1):
    """
    Detect hidden profit or loss.
    Returns a dict with status, headline, explanation, impact per quintal, total impact, advice
    """
    impact_per_quintal = round(predicted_price - current_price, 2)
    total_impact = round(impact_per_quintal * quantity, 2)

    if impact_per_quintal > 0:
        status = "HIDDEN_LOSS"
        headline = "Hidden loss detected ⚠️ Selling now may cause loss."
        explanation = "If sold now, you may miss profit."
        advice = "Waiting may give better profit, if storage is possible."
    elif impact_per_quintal < 0:
        status = "SELL_NOW"
        headline = "Current loss detected ⚠️ Selling now may minimize loss."
        explanation = "Future prices may drop further."
        advice = "Sell now to avoid bigger losses."
    else:
        status = "NEUTRAL"
        headline = "No significant change expected."
        explanation = "Selling now or later will have minimal impact."
        advice = "Either option is acceptable."

    return {
        "status": status,
        "headline": headline,
        "explanation": explanation,
        "impact_per_quintal": impact_per_quintal,
        "total_impact": total_impact,
        "advice": advice
    }

def generate_recommendation(status, risk_level):
    """Generates farmer-friendly recommendation sentence."""
    status = status.upper()
    risk_level = risk_level.upper()

    if status == "HIDDEN_LOSS":
        if risk_level == "LOW":
            return "Waiting may give better profit, and market risk is LOW."
        elif risk_level == "MEDIUM":
            return "Waiting may increase profit, but market risk is MEDIUM."
        else:
            return "Higher profit possible if you wait, but market risk is HIGH."
    elif status == "SELL_NOW":
        return f"Sell now — future prices are expected to fall. Risk Level: {risk_level}."
    elif status == "NEUTRAL":
        return f"Either option is reasonable; price difference is minimal. Risk Level: {risk_level}."
    else:
        return "Decision unclear. Check market conditions."

def optimal_selling_window(df, crop, district, market, months_ahead=3, price_col="modal_price"):
    """
    Suggests optimal selling month(s) based on historical modal_price averages.
    Fallback: market -> district -> crop
    Returns best_months list and fallback level used.
    """
    df = df.copy()
    # Clean strings (on copy to avoid mutating caller's dataframe)
    df['crop'] = df['crop'].astype(str).str.strip().str.lower()
    df['district'] = df['district'].astype(str).str.strip().str.lower()
    df['market'] = df['market'].astype(str).str.strip().str.lower()
    crop = crop.strip().lower()
    district = district.strip().lower()
    market = market.strip().lower()

    # Ensure date column is datetime
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])

    # Extract month
    df['month'] = df['date'].dt.month

    fallback = "Exact market"
    data = df[(df['crop'] == crop) & (df['district'] == district) & (df['market'] == market)]
    if data.empty:
        data = df[(df['crop'] == crop) & (df['district'] == district)]
        fallback = "District-level average"
    if data.empty:
        data = df[df['crop'] == crop]
        fallback = "Crop-level average"
    if data.empty:
        return [], "No data"

    monthly_avg = data.groupby('month')[price_col].mean()
    if monthly_avg.empty:
        return [], "No data"

    top_months = monthly_avg.sort_values(ascending=False).head(months_ahead)
    best_months = [(m, p) for m, p in zip(top_months.index, top_months.values)]
    return best_months, fallback
