import pandas as pd
import os

def load_and_clean_data(file_path):
    # Load the dataset
    df = pd.read_csv(file_path)
    
    # Drop the freelancer id column
    if 'freelancer_id' in df.columns:
        df = df.drop(columns=['freelancer_id'])
        print("Freelancer Id coloumn droped")
    
    if 'hourly_rate_usd' in df.columns:
        df = df.drop(columns=['hourly_rate_usd'])
        print("Hourly rate coloumn droped")

    if 'primary_platform' in df.columns:
        df = df.drop(columns=['primary_platform'])
        print("primary_platform coloumn droped")
    
    # Drop Region and Country
    cols_to_drop = ['region', 'country']
    df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])
    print("Region and Country coloumn droped")

    # Round off Work Experience 
    target_col = 'years_experience'
    if target_col in df.columns:
        # Fill missing values with 0 before rounding to avoid errors
        df[target_col] = df[target_col].fillna(0)
        
        # Round to nearest whole number and convert to integer
        df[target_col] = df[target_col].round().astype(int)
        print(f"Rounded '{target_col}' to whole numbers.")
    
    # Dividing Annual_Income_USD into ranges
    # Adding new Rnge Column
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
    
    # Converting primary_skills String to Array of string
    if 'primary_skills' in df.columns:
        df['primary_skills'] = df['primary_skills'].apply(
            lambda x: [skill.strip() for skill in x.split(',')] if pd.notna(x) else []
        )
    
    # Basic cleanup: Remove rows with missing essential values
    # (Category and Primary Skills are the backbone of our KG)
    df = df.dropna(subset=['category', 'primary_skills',])
    
    return df

if __name__ == "__main__":
    # Path to your data
    DATA_PATH = os.path.join('..','..', 'data', 'dataset.csv')
    OUTPUT_PATH = os.path.join('..', '..', 'data', 'processed', 'cleaned_dataset.csv')

    # Create folder if it doesn't exist
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    if os.path.exists(DATA_PATH):
        raw_df = load_and_clean_data(DATA_PATH)
        print("Initial Cleanup Complete.")
        print(f"Columns remaining: {list(raw_df.columns)}")
        print(raw_df.head(10))
        # Save the DataFrame
        raw_df.to_csv(OUTPUT_PATH, index=False)
        print(f"Cleaned dataset saved at: {OUTPUT_PATH}")
    else:
        print(f"Error: Could not find file at {DATA_PATH}. Please check your data folder.")