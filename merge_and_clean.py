import pandas as pd
import glob
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "merged_cleaned_prices.csv")

all_dfs = []

print("\n🔄 STARTING MERGE & CLEAN PROCESS\n")

for file_path in glob.glob(os.path.join(DATA_DIR, "*.csv")):
    crop_name = os.path.basename(file_path).split("_")[0].capitalize()

    print(f"Reading: {file_path}")
    df = pd.read_csv(file_path)

    print(f"Initial rows: {len(df)}")

    # ---------- STANDARDIZE COLUMN NAMES ----------
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # ---------- FIND DATE COLUMN ----------
    date_col = None
    for col in df.columns:
        if "date" in col:
            date_col = col
            break

    if date_col is None:
        print("❌ No date column found, skipping file\n")
        continue

    # ---------- PARSE DATE SAFELY ----------
    df["date"] = pd.to_datetime(
        df[date_col],
        errors="coerce",
        dayfirst=True
    )

    # ---------- CLEAN PRICE COLUMNS ----------
    price_cols = [col for col in df.columns if "price" in col]

    for col in price_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(r"[^\d.]", "", regex=True)
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # ---------- ADD CROP COLUMN ----------
    df["crop"] = crop_name

    # ---------- KEEP ONLY IMPORTANT COLUMNS ----------
    keep_cols = ["date", "crop"]

    for col in ["state", "district", "market"]:
        if col in df.columns:
            keep_cols.append(col)

    for col in ["min_price", "max_price", "modal_price"]:
        if col in df.columns:
            keep_cols.append(col)

    df = df[keep_cols]

    # ---------- DROP ONLY ESSENTIAL NaNs ----------
    df = df.dropna(subset=["date", "modal_price"])

    print(f"Rows after cleaning: {len(df)}\n")

    if len(df) > 0:
        all_dfs.append(df)

# ---------- MERGE ALL ----------
if not all_dfs:
    print("❌ No valid data found!")
    exit()

final_df = pd.concat(all_dfs, ignore_index=True)

# ---------- SORT ----------
final_df = final_df.sort_values(by=["crop", "date"])

# ---------- SAVE ----------
final_df.to_csv(OUTPUT_FILE, index=False)

print("✅ MERGE COMPLETE")
print(f"Total rows: {len(final_df)}")
print("Crop-wise count:")
print(final_df["crop"].value_counts())
print(f"\n📁 Saved as: {OUTPUT_FILE}")
