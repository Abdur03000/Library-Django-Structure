from fastapi import HTTPException, status

def not_found_exception(name: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{name} not found."
    )

def bad_request_exception(message: str):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=message
    )
