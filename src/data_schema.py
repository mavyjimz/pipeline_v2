from pydantic import BaseModel, Field, field_validator
from typing import List

class CreditCardSchema(BaseModel):
    """
    The 'Data Contract' for Credit Card Transactions.
    Ensures strict validation at the pipeline entrance.
    """
    Time: float
    V1: float
    V2: float
    Amount: float = Field(..., description="The transaction value")
    Class: int = Field(..., ge=0, le=1, description="0=Safe, 1=Fraud")

    @field_validator('Amount')
    @classmethod
    def amount_must_be_positive(cls, v: float) -> float:
        if v < 0:
            raise ValueError(f"VALIDATION FAILED: Negative amount detected: {v}")
        return v

class TransactionBatch(BaseModel):
    transactions: List[CreditCardSchema]

# --- SELF-TEST BLOCK ---
if __name__ == "__main__":
    print("--- RUNNING SCHEMA SELF-TEST ---")
    try:
        # Test 1: Valid Data
        valid_data = {"Time": 0.0, "V1": 1.1, "V2": -1.1, "Amount": 100.0, "Class": 0}
        CreditCardSchema(**valid_data)
        print("TEST 1 PASSED: Valid data accepted.")

        # Test 2: Invalid Data (Negative Amount)
        print("TEST 2: Testing Negative Amount (Should fail)...")
        invalid_data = {"Time": 0.0, "V1": 1.1, "V2": -1.1, "Amount": -50.0, "Class": 0}
        CreditCardSchema(**invalid_data)
    except ValueError as e:
        print(f"TEST 2 PASSED: Caught expected error: {e}")
    
    print("--- SCHEMA VERIFIED ---")