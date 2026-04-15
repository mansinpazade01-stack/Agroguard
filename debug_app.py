import pandas as pd
import os
import joblib

print("--- DIAGNOSTIC START ---")

# 1. Check Paths
base_dir = os.getcwd()
data_path = os.path.join(base_dir, "data", "merged_cleaned_prices.csv")
model_path = os.path.join(base_dir, "models", "price_model.pkl")

print(f"Checking Data Path: {data_path} -> Exists: {os.path.exists(data_path)}")
print(f"Checking Model Path: {model_path} -> Exists: {os.path.exists(model_path)}")

# 2. Load Data
if os.path.exists(data_path):
    try:
        df = pd.read_csv(data_path)
        print(f"Data Loaded. Shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        
        # Check Crop
        if 'crop' in df.columns:
            unique_crops = df['crop'].unique()
            print(f"Unique Crops ({len(unique_crops)}): {unique_crops[:5]}...")
        else:
            print("CRITICAL: 'crop' column missing!")

        # Check District
        if 'district' in df.columns:
            print("District column found.")
            # check logic
            test_crop = df['crop'].iloc[0]
            districts = df[df['crop'] == test_crop]['district'].unique()
            print(f"Districts for {test_crop}: {districts}")
        else:
            print("CRITICAL: 'district' column missing!")

        # Check Market
        if 'market' in df.columns:
             print("Market column found.")
        else:
             print("CRITICAL: 'market' column missing!")
             
    except Exception as e:
        print(f"Error reading CSV: {e}")
else:
    print("CSV File does not exist.")

print("--- DIAGNOSTIC END ---")
