import pandas as pd
from sklearn.model_selection import train_test_split
import os

def split_data():
    input_path = "input_data/processed/cleaned_creditcard.csv"
    output_dir = "input_data/processed"
    
    print("LOG: Initializing R&D Phase: Train-Test Splitting...")
    
    if not os.path.exists(input_path):
        print(f"ERROR: Processed data not found at {input_path}")
        return

    # 1. Load Cleaned Data
    df = pd.read_csv(input_path)
    
    # 2. Separate Features and Target
    X = df.drop('Class', axis=1)
    y = df['Class']
    
    # 3. Stratified Split (Crucial for 0.17% fraud ratio)
    # 80% Train, 20% Test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 4. Save Splits for R&D Reproducibility
    X_train.to_csv(os.path.join(output_dir, "X_train.csv"), index=False)
    X_test.to_csv(os.path.join(output_dir, "X_test.csv"), index=False)
    y_train.to_csv(os.path.join(output_dir, "y_train.csv"), index=False)
    y_test.to_csv(os.path.join(output_dir, "y_test.csv"), index=False)
    
    print("LOG: Stratified splitting complete.")
    print(f"LOG: Training set size: {len(X_train)}")
    print(f"LOG: Testing set size: {len(X_test)}")
    print(f"LOG: Fraud cases in Test set: {sum(y_test)}")
    print("----------------------------------\n")

if __name__ == "__main__":
    split_data()