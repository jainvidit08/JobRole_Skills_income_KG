import pandas as pd
import os

def load_and_clean_data(file_path):
    # Load the dataset
    df = pd.read_csv("../../data/dataset.csv")
    
    # Drop the freelancer id column
    if 'freelancer_id' in df.columns:
        df = df.drop(columns=['freelancer_id'])
    
    if 'primary_platform' in df.columns:
        df = df.drop(columns=['primary_platform'])
    
    # Drop Region and Country
    cols_to_drop = ['region', 'country']
    df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])
    
    # Basic cleanup: Remove rows with missing essential values
    # (Category and Primary Skills are the backbone of our KG)
    df = df.dropna(subset=['category', 'primary_skills'])
    
    return df

if __name__ == "__main__":
    # Path to your data
    DATA_PATH = os.path.join('..','..', 'data', 'dataset.csv')
    
    if os.path.exists(DATA_PATH):
        raw_df = load_and_clean_data(DATA_PATH)
        print("Initial Cleanup Complete.")
        print(f"Columns remaining: {list(raw_df.columns)}")
        print(raw_df.head())
    else:
        print(f"Error: Could not find file at {DATA_PATH}. Please check your data folder.")