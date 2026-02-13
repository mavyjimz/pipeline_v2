import pandas as pd
import logging
import os
import sys

# Ensure Python can find our 'src' folder for the schema import
sys.path.append(os.path.join(os.getcwd(), "src"))
from data_schema import CreditCardSchema

# Senior-grade logging setup - No emojis for terminal compatibility
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def ingest_data(file_path: str):
    logging.info(f"STARTING: Initializing ingestion for: {file_path}")
    
    # 1. Safety Check: Does the file exist?
    if not os.path.exists(file_path):
        logging.error(f"CRITICAL: File not found at {file_path}")
        return None

    try:
        # 2. Load the data
        df = pd.read_csv(file_path)
        logging.info(f"SUCCESS: CSV Loaded. Found {len(df)} rows.")

        # 3. Integrity Check (The Pydantic Gate)
        # We validate the top 10 rows to ensure the 'Contract' is valid
        records = df.head(10).to_dict(orient='records')
        for i, record in enumerate(records):
            CreditCardSchema(**record)
        
        logging.info("VERIFIED: Data Contract integrity check passed.")
        return df

    except Exception as e:
        logging.error(f"FAILURE: Data integrity check failed: {e}")
        raise

if __name__ == "__main__":
    # Pointing to the location we established in Phase 1
    # NOTE: Ensure creditcard.csv is in pipeline_v2/data/raw/
    RAW_DATA_PATH = "data/raw/creditcard.csv"
    ingest_data(RAW_DATA_PATH)