import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os

def train_detection_engine():
    # R&D Paths
    input_dir = "input_data/processed"
    model_dir = "model"
    
    print("LOG: Initializing R&D Phase: Model Training (Random Forest)...")
    
    # 1. Load the Stratified Splits
    try:
        X_train = pd.read_csv(os.path.join(input_dir, "X_train.csv"))
        y_train = pd.read_csv(os.path.join(input_dir, "y_train.csv")).values.ravel()
        X_test = pd.read_csv(os.path.join(input_dir, "X_test.csv"))
        y_test = pd.read_csv(os.path.join(input_dir, "y_test.csv")).values.ravel()
    except Exception as e:
        print(f"ERROR: Could not load split data. {str(e)}")
        return

    # 2. Configure the Engine
    # n_jobs=-1 uses all CPU cores for faster training on 227k rows
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    
    # 3. Training
    print("LOG: Training engine on 227,845 records. This may take a moment...")
    model.fit(X_train, y_train)
    
    # 4. Immediate R&D Validation
    print("LOG: Running validation on 56,962 unseen transactions...")
    y_pred = model.predict(X_test)
    
    print("\n--- R&D MODEL PERFORMANCE ---")
    print(classification_report(y_test, y_pred))
    print("-----------------------------\n")
    
    # 5. Save the Asset
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(model, os.path.join(model_dir, "fraud_model.pkl"))
    print(f"LOG: Model asset saved to {model_dir}/fraud_model.pkl")

if __name__ == "__main__":
    train_detection_engine()