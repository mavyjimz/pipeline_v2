import pandas as pd
import logging
import os
import sys

# Ensure Python can find the src folder
sys.path.append(os.path.join(os.getcwd(), "src"))
from data_schema import CreditCardSchema

# ASCII Logging Only
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def ingest_data(file_path: str):
    logging.info(f"STARTING: Initializing ingestion for: {file_path}")
    
    if not os.path.exists(file_path):
        logging.error(f"CRITICAL: File not found at {file_path}")
        return None

    try:
        df = pd.read_csv(file_path)
        logging.info(f"SUCCESS: CSV Loaded. Found {len(df)} rows.")

        # Validate top 10 rows
        records = df.head(10).to_dict(orient='records')
        for record in records:
            CreditCardSchema(**record)
        
        logging.info("VERIFIED: Data Contract integrity check passed.")
        return df

    except Exception as e:
        logging.error(f"FAILURE: Data integrity check failed: {e}")
        raise

if __name__ == "__main__":
    RAW_DATA_PATH = "data/raw/creditcard.csv"
    ingest_data(RAW_DATA_PATH)