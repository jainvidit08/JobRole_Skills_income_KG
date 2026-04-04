import pandas as pd
import os

def load_and_clean_data(file_path):
    # Load the dataset
    df = pd.read_csv("../../data/dataset.csv")
    
    if 'primary_skills' in df.columns:
        df['primary_skills'] = df['primary_skills'].apply(
            lambda x: [skill.strip() for skill in x.split(',')] if pd.notna(x) else []
        )
    
    return df

if __name__ == "__main__":
    # Path to your data
    DATA_PATH = os.path.join('..','..', 'data', 'dataset.csv')
    
    if os.path.exists(DATA_PATH):
        raw_df = load_and_clean_data(DATA_PATH)
        print("Initial Cleanup Complete.")
        print(raw_df.head())
        skills_list = raw_df['primary_skills'].iloc[1]

        if len(skills_list) > 1:
            print(skills_list[0])
        else:
            print("Not enough skills in this row")
    else:
        print(f"Error: Could not find file at {DATA_PATH}. Please check your data folder.")