import pandas as pd
import logging
from sklearn.preprocessing import StandardScaler

# Standard logging - No emojis
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DataProcessor:
    def __init__(self):
        self.scaler = StandardScaler()

    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        logging.info("PROCESSOR: Checking for missing values...")
        null_count = df.isnull().sum().sum()
        if null_count > 0:
            logging.info(f"PROCESSOR: Dropping {null_count} missing values.")
            df = df.dropna()
        else:
            logging.info("PROCESSOR: No missing values found.")
        return df

    def scale_features(self, df: pd.DataFrame) -> pd.DataFrame:
        logging.info("PROCESSOR: Scaling 'Amount' and 'Time' features...")
        # We scale these because they have much larger ranges than the V1-V28 features
        df['Amount'] = self.scaler.fit_transform(df[['Amount']])
        df['Time'] = self.scaler.fit_transform(df[['Time']])
        return df

if __name__ == "__main__":
    # Test block to verify the logic
    from data_ingestion import ingest_data
    raw_df = ingest_data("data/raw/creditcard.csv")
    
    if raw_df is not None:
        processor = DataProcessor()
        clean_df = processor.handle_missing_values(raw_df)
        final_df = processor.scale_features(clean_df)
        logging.info(f"PROCESSOR: Transformation complete. Shape: {final_df.shape}")