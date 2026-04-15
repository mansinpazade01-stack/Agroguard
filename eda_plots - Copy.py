import os
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(os.path.join(os.path.dirname(__file__), "..", "data", "merged_cleaned_prices.csv"))
print(df.shape)
print(df.columns)
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')
print(df['crop'].value_counts())
crop_name = "Wheat" 
df_crop = df[df['crop'] == crop_name]
df_crop_2025 = df_crop[df_crop['date'].dt.year == 2025]
df_daily = df_crop_2025.groupby('date')['modal_price'].mean().reset_index()
plt.figure(figsize=(12, 6))
plt.plot(df_daily['date'], df_daily['modal_price'], color='blue', label=f'{crop_name} Avg Modal Price 2025')
plt.title(f'{crop_name} Average Modal Price Trend in 2025')
plt.xlabel('Date')
plt.ylabel('Average Modal Price')
plt.legend()
plt.tight_layout()
_plots_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", "plots")
os.makedirs(_plots_dir, exist_ok=True)
plt.savefig(os.path.join(_plots_dir, f"{crop_name.lower()}_avg_price_trend_2025.png"))
plt.close()

print(f"✅ Saved: {_plots_dir}/{crop_name.lower()}_avg_price_trend_2025.png")



# Group by district and calculate average modal price
df_district = (
    df_crop_2025
    .groupby('district', as_index=False)['modal_price']
    .mean()
)

# Sort districts by average price (high → low)
df_district = df_district.sort_values(by='modal_price', ascending=False)

# Take top 10 districts (optional but recommended)
df_district_top10 = df_district.head(10)
plt.figure(figsize=(10, 6))
plt.barh(df_district_top10['district'], df_district_top10['modal_price'])
plt.xlabel('Average Modal Price')
plt.ylabel('District')
plt.title(f'Top 10 Districts by Average {crop_name} Price in 2025')
plt.gca().invert_yaxis()
plt.tight_layout()

plt.savefig(os.path.join(_plots_dir, f"{crop_name.lower()}_district_avg_price_2025.png"))
plt.close()

print("✅ District-wise plot saved")
# Volatility = standard deviation of modal price
df_volatility = (
    df_crop_2025
    .groupby('district', as_index=False)['modal_price']
    .std()
)

# Rename column for clarity
df_volatility.rename(columns={'modal_price': 'price_volatility'}, inplace=True)

# Sort by volatility (high risk first)
df_volatility = df_volatility.sort_values(by='price_volatility', ascending=False)

# Take top 10 most volatile districts
df_volatility_top10 = df_volatility.head(10)
plt.figure(figsize=(10, 6))
plt.barh(df_volatility_top10['district'], df_volatility_top10['price_volatility'])
plt.xlabel('Price Volatility (Std Dev)')
plt.ylabel('District')
plt.title(f'Top 10 Most Volatile Districts for {crop_name} Prices in 2025')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.barh(
    df_volatility_top10['district'],
    df_volatility_top10['price_volatility'],
    color='crimson'
)


plt.savefig(os.path.join(_plots_dir, f"{crop_name.lower()}_district_volatility_2025.png"))
plt.close()

print("✅ Volatility plot saved")



df_crop_2025.loc[:, 'month_num'] = df_crop_2025['date'].dt.month
df_crop_2025.loc[:, 'month_name'] = df_crop_2025['date'].dt.month_name()

df_monthly = (
    df_crop_2025
    .groupby(['month_num', 'month_name'], as_index=False)['modal_price']
    .mean()
    .sort_values('month_num')
)

plt.figure(figsize=(10, 6))
plt.plot(df_monthly['month_name'], df_monthly['modal_price'], marker='o')
plt.xlabel('Month')
plt.ylabel('Average Modal Price')
plt.title(f'{crop_name} Monthly Price Seasonality (2025)')
plt.xticks(rotation=45)
plt.tight_layout()
os.makedirs(os.path.join(os.path.dirname(__file__), "..", "outputs", "plots"), exist_ok=True)
plt.savefig(os.path.join(os.path.dirname(__file__), "..", "outputs", "plots", f"{crop_name.lower()}_monthly_seasonality_2025.png"))
plt.close()

print("✅ ALL EDA PLOTS GENERATED SUCCESSFULLY")