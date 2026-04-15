import os
import pandas as pd
df = pd.read_csv(os.path.join(os.path.dirname(__file__), "..", "data", "merged_cleaned_prices.csv"))
print(df.columns)
print(df.shape)
print(df.head())
print(df.info())
#df["date"] = pd.to_datetime(df["date"], errors="coerce")
#print(df.info())