import pandas as pd
import os
import numpy as np

def process_dataset():
    # Define the file path
    # dataset.csv is in the 'data' folder
    file_path = os.path.join('..','..', 'data', 'dataset.csv')
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return None

    # Load the data
    df = pd.read_csv(file_path)
    print(f"Successfully loaded {file_path}")
    
    # Rounding Experience ---
    target_col = 'years_experience'
    if target_col in df.columns:
        # Fill missing values with 0 before rounding to avoid errors
        df[target_col] = df[target_col].fillna(0)
        
        # Round to nearest whole number and convert to integer
        df[target_col] = df[target_col].round().astype(int)
        print(f"Rounded '{target_col}' to whole numbers.")
    
    # Display results for verification
    print("\n--- Processed Data Preview ---")
    print(df[target_col].head())
    
    return df

if __name__ == "__main__":
    processed_df = process_dataset()