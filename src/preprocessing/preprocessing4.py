import pandas as pd
import os

def bin_annual_income(df):
    """
    Categorizes the 'annual_rate_usd' into 4 specific ranges:
    1. < 50k
    2. 50k - 80k
    3. 80k - 125k
    4. 125k+
    """
    target_col = 'annual_income_usd'
    new_col = 'annual_income_range'
    
    if target_col in df.columns:
        # Convert string to Numeric values
        df[target_col] = df[target_col].astype(str)
        df[target_col] = df[target_col].str.replace(r'[$,]', '', regex=True)
        df[target_col] = pd.to_numeric(df[target_col], errors='coerce')
        
        df = df.dropna(subset=[target_col])
        # Define the bin edges
        # float('inf') represents the upper limit for the last category
        bins = [0, 50000, 80000, 125000, float('inf')]
        
        # Define the labels for these bins
        labels = [
            '< $50k', 
            '$50k - $80k', 
            '$80k - $125k', 
            '$125k+'
        ]
        
        # Create the new column
        # right=False means the left edge is inclusive [50000, 80000)
        df[new_col] = pd.cut(df[target_col], bins=bins, labels=labels, right=False)
        
        print(f"Successfully created '{new_col}' column.")
    else:
        print(f"Error: {target_col} not found in dataset.")
        
    return df

# --- Execution for dataset.csv ---
if __name__ == "__main__":
    file_path = os.path.join('..','..', 'data', 'dataset.csv')
    
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        
        # Apply the binning
        df = bin_annual_income(df)
        
        # Preview the results
        print("\n--- Income Binning Preview ---")
        print(df[['annual_income_usd', 'annual_income_range']].head(10))
    else:
        print("Dataset file not found.")