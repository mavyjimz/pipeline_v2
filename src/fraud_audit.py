import pandas as pd
import os

def initial_research():
    # Maasin Lab R&D Path
    raw_data_path = "input_data/raw/creditcard.csv"
    
    print("LOG: Initializing R&D Phase: Credit Card Fraud Detection...")
    
    # Check if file exists to prevent path errors
    if not os.path.exists(raw_data_path):
        print(f"ERROR: Target file not found at {raw_data_path}")
        return
    
    # 1. Loading the Big Data
    try:
        df = pd.read_csv(raw_data_path)
    except Exception as e:
        print(f"ERROR: Failed to load CSV. {str(e)}")
        return
    
    # 2. Extracting the Fraud Signal (Class 1 = Fraud)
    total_rows = len(df)
    fraud_count = df[df['Class'] == 1].shape[0]
    normal_count = df[df['Class'] == 0].shape[0]
    
    # 3. Research Summary
    print("\n--- R&D DATASET SUMMARY ---")
    print(f"Total Transactions: {total_rows}")
    print(f"Normal Activities:  {normal_count}")
    print(f"Fraudulent Flags:   {fraud_count}")
    print(f"Fraud Percentage:   {(fraud_count/total_rows)*100:.4f}%")
    print("---------------------------\n")

if __name__ == "__main__":
    initial_research()