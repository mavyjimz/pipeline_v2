import pandas as pd
from sklearn.preprocessing import StandardScaler
import os

def clean_and_scale():
    raw_path = "input_data/raw/creditcard.csv"
    processed_dir = "input_data/processed"
    output_path = os.path.join(processed_dir, "cleaned_creditcard.csv")
    
    print("LOG: Initializing R&D Phase: Data Cleaning and Scaling...")
    
    if not os.path.exists(raw_path):
        print(f"ERROR: Raw data not found at {raw_path}")
        return

    # 1. Load Data
    df = pd.read_csv(raw_path)
    
    # 2. Scaling 'Amount' and 'Time'
    # These are the only features not yet scaled in the Kaggle dataset
    scaler = StandardScaler()
    
    print("LOG: Scaling 'Amount' and 'Time' features...")
    df['scaled_amount'] = scaler.fit_transform(df['Amount'].values.reshape(-1, 1))
    df['scaled_time'] = scaler.fit_transform(df['Time'].values.reshape(-1, 1))
    
    # 3. Drop original unscaled columns
    df.drop(['Time', 'Amount'], axis=1, inplace=True)
    
    # 4. Save Processed Data
    os.makedirs(processed_dir, exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print(f"LOG: Cleaned data saved to {output_path}")
    print(f"LOG: Processed shape: {df.shape}")
    print("LOG: Data cleaning complete.")

if __name__ == "__main__":
    clean_and_scale()