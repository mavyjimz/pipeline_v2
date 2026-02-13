import pandas as pd
import logging
import os
import sys
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))
from data_ingestion import ingest_data

# ASCII Logging Only
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DataProcessor:
    def __init__(self):
        self.scaler = StandardScaler()

    def clean_and_scale(self, df: pd.DataFrame) -> pd.DataFrame:
        logging.info("PROCESSOR: Cleaning missing values and scaling features...")
        df = df.dropna()
        df['Amount'] = self.scaler.fit_transform(df[['Amount']])
        df['Time'] = self.scaler.fit_transform(df[['Time']])
        return df

def train_and_save(df: pd.DataFrame, processor: DataProcessor):
    logging.info("TRAINER: Starting training sequence...")
    
    X = df.drop('Class', axis=1)
    y = df['Class']
    
    # Stratified split for imbalanced fraud data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Use n_jobs=-1 for multi-core CPU speed
    model = RandomForestClassifier(n_estimators=10, random_state=42, n_jobs=-1)
    logging.info("TRAINER: Fitting Random Forest model...")
    model.fit(X_train, y_train)
    
    # Evaluation
    y_pred = model.predict(X_test)
    print("\n--- PERFORMANCE REPORT ---")
    print(classification_report(y_test, y_pred))
    
    # Persistence
    if not os.path.exists("model"):
        os.makedirs("model")
    
    joblib.dump(model, "model/fraud_model.pkl")
    joblib.dump(processor.scaler, "model/scaler.pkl")
    logging.info("SUCCESS: Model and Scaler saved to model/ directory.")

if __name__ == "__main__":
    raw_df = ingest_data("data/raw/creditcard.csv")
    if raw_df is not None:
        proc = DataProcessor()
        clean_df = proc.clean_and_scale(raw_df)
        train_and_save(clean_df, proc)