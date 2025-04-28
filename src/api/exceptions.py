from fastapi import HTTPException, status

InvalidTransactionSignature = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid transaction signature.",
)
