from fastapi import APIRouter, HTTPException
from app.services.cognito_service import CognitoService

router = APIRouter()
cognito_service = CognitoService()

@router.post("/login")
def login(username: str, password: str):
    """
    Login endpoint to authenticate users and return a JWT token.
    """
    try:
        tokens = cognito_service.authenticate_user(username, password)
        return {"message": "Login successful", "tokens": tokens}
    except HTTPException as e:
        raise e
