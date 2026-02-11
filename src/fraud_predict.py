import pandas as pd
import joblib
import os

def run_prediction_test():
    model_path = "model/fraud_model.pkl"
    test_data_path = "input_data/processed/X_test.csv"
    
    print("LOG: Initializing R&D Phase: Live Prediction Testing...")
    
    if not os.path.exists(model_path):
        print(f"ERROR: Model asset not found at {model_path}")
        return

    # 1. Load the Brain and Sample Data
    model = joblib.load(model_path)
    X_test = pd.read_csv(test_data_path)
    
    # 2. Select a sample (Row 0) for testing
    sample_transaction = X_test.iloc[[0]]
    
    # 3. Execute Prediction
    print("LOG: Analyzing transaction signature...")
    prediction = model.predict(sample_transaction)
    probability = model.predict_proba(sample_transaction)
    
    # 4. Final Verdict
    result = "FRAUD DETECTED" if prediction[0] == 1 else "NORMAL TRANSACTION"
    confidence = probability[0][prediction[0]] * 100
    
    print("\n--- R&D PREDICTION VERDICT ---")
    print(f"VERDICT:    {result}")
    print(f"CONFIDENCE: {confidence:.2f}%")
    print("------------------------------\n")

if __name__ == "__main__":
    run_prediction_test()