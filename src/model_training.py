import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Standard ASCII logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def train_fraud_model(df: pd.DataFrame):
    logging.info("TRAINER: Starting model training sequence...")
    
    # Target check
    if 'Class' not in df.columns:
        logging.error("TRAINER: Target column 'Class' missing!")
        return None

    X = df.drop('Class', axis=1)
    y = df['Class']
    
    logging.info("TRAINER: Splitting data (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    logging.info(f"TRAINER: Training Random Forest (10 Trees) on {len(X_train)} rows...")
    # Using n_jobs=-1 to use all your CPU cores for speed
    model = RandomForestClassifier(n_estimators=10, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    logging.info("TRAINER: Training complete. Evaluating...")
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred)
    
    print("\n--- FRAUD DETECTION REPORT ---")
    print(report)
    print("------------------------------\n")
    
    return model

if __name__ == "__main__":
    from data_ingestion import ingest_data
    from data_processor import DataProcessor
    
    # Full Chain Execution
    raw_df = ingest_data("data/raw/creditcard.csv")
    if raw_df is not None:
        processor = DataProcessor()
        # Clean and scale
        processed_df = processor.handle_missing_values(raw_df)
        final_df = processor.scale_features(processed_df)
        
        # Train
        train_fraud_model(final_df)