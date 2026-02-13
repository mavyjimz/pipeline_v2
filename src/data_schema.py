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
    # Business critical fields: Field(...) means it is REQUIRED
    Amount: float = Field(..., description="The transaction value")
    Class: int = Field(..., ge=0, le=1, description="0=Safe, 1=Fraud")

    # Integrity Check: Financial data must have positive amounts
    @field_validator('Amount')
    @classmethod
    def amount_must_be_positive(cls, v: float) -> float:
        if v < 0:
            raise ValueError(f"VALIDATION FAILED: Negative amount detected: {v}")
        return v

class TransactionBatch(BaseModel):
    """Handles bulk validation of multiple rows from the CSV"""
    transactions: List[CreditCardSchema]