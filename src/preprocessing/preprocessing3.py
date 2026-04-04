import pandas as pd
import os

def analyze_annual_income():
    # Path to your standardized dataset
    file_path = os.path.join('..','..', 'data', 'dataset.csv')
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    # Load the data
    df = pd.read_csv(file_path)
    
    target_col = 'annual_income_usd'
    
    if target_col in df.columns:
        # Clean income column
        df[target_col] = df[target_col].astype(str)
        df[target_col] = df[target_col].str.replace(r'[$,]', '', regex=True)
        df[target_col] = pd.to_numeric(df[target_col], errors='coerce')
        
        df = df.dropna(subset=[target_col])

        # 1. Basic Stats
        min_income = df[target_col].min()
        max_income = df[target_col].max()
        avg_income = df[target_col].mean()
        median_income = df[target_col].median()
        
        # 2. Percentiles (Helpful for breaking into ranges)
        # This shows what 25%, 50%, and 75% of people earn
        quantiles_3 = df[target_col].quantile([0.25, 0.5, 0.75])
        quantiles_5 = df[target_col].quantile([0.20, 0.40, 0.60,0.80,0.90])
        
        print(f"--- Income Analysis for {target_col} ---")
        print(f"Minimum Annual Income: ${min_income:,.2f}")
        print(f"Maximum Annual Income: ${max_income:,.2f}")
        print(f"Average Annual Income: ${avg_income:,.2f}")
        print(f"Median Annual Income:  ${median_income:,.2f}")
        print("\n--- Distribution (Quantiles 4) ---")
        print(f"25th Percentile: ${quantiles_3[0.25]:,.2f}")
        print(f"50th Percentile: ${quantiles_3[0.50]:,.2f} (Median)")
        print(f"75th Percentile: ${quantiles_3[0.75]:,.2f}")

        print("\n--- Distribution (Quantiles 5) ---")
        print(f"20th Percentile: ${quantiles_5[0.20]:,.2f}")
        print(f"40th Percentile: ${quantiles_5[0.40]:,.2f}")
        print(f"60th Percentile: ${quantiles_5[0.60]:,.2f}")
        print(f"80th Percentile: ${quantiles_5[0.80]:,.2f}")
        print(f"90th Percentile: ${quantiles_5[0.90]:,.2f}")
        
    else:
        print(f"Error: Column '{target_col}' not found in dataset.csv")
        print(f"Available columns: {list(df.columns)}")

if __name__ == "__main__":
    analyze_annual_income()