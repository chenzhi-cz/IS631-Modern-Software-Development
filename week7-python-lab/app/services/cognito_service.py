import os
from jose import jwt
from jose.exceptions import JWTError
import boto3
import hmac
import hashlib
import base64
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests
from dotenv import load_dotenv

load_dotenv()


CognitoUserRole = os.getenv("COGNITO_USER_ROLE", "Users")
CognitoAdminRole = os.getenv("COGNITO_ADMIN_ROLE", "Admins")
bearer_scheme = HTTPBearer()

class CognitoService:
    def __init__(self):
        self.region = os.getenv("COGNITO_REGION")
        self.user_pool_id = os.getenv("COGNITO_USER_POOL_ID")
        self.client_id = os.getenv("COGNITO_CLIENT_ID")
        self.client_secret = os.getenv("COGNITO_CLIENT_SECRET")
        self.jwks_url = f"https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}/.well-known/jwks.json"
        self.jwks_keys = self._get_cognito_jwks()
        self.bearer = HTTPBearer()

        # Initialize Boto3 Cognito client
        self.client = boto3.client("cognito-idp", region_name=self.region)

    def _get_cognito_jwks(self):
        """
        Retrieve JWKS (JSON Web Key Set) for token validation from AWS Cognito.
        """
        response = requests.get(self.jwks_url)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Unable to fetch JWKS for token validation.")
        return response.json()["keys"]

    def validate_token(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        """
        Validate and decode a JWT token issued by AWS Cognito.

        :param credentials: HTTPAuthorizationCredentials (token from the Authorization header).
        :return: The decoded token payload.
        """
        token = credentials.credentials
        try:
            # Decode token using Cognito's JWKS
            headers = jwt.get_unverified_header(token)
            kid = headers.get("kid")
            key = next((k for k in self.jwks_keys if k["kid"] == kid), None)
            if not key:
                raise HTTPException(status_code=401, detail="Invalid token signature.")

            payload = jwt.decode(
                token,
                key=key,
                algorithms=["RS256"],
                audience=self.client_id,
                issuer=f"https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}",
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired.")
        except jwt.JWTError as e:
            raise HTTPException(status_code=401, detail=f"Token validation error: {str(e)}")

    def calculate_secret_hash(self, username):
        """
        Calculate the Cognito SECRET_HASH for the given username.
        """
        message = username + self.client_id
        dig = hmac.new(
            self.client_secret.encode("utf-8"),
            message.encode("utf-8"),
            hashlib.sha256
        ).digest()
        return base64.b64encode(dig).decode()

    def authenticate_user(self, username: str, password: str):
        """
        Authenticate a user with Cognito using their username and password.

        :param username: Username of the user.
        :param password: Password of the user.
        :return: Dictionary containing tokens if authentication is successful.
        """
        try:
            # Calculate the SECRET_HASH
            secret_hash = self.calculate_secret_hash(username)

            # Initiate the authentication
            response = self.client.initiate_auth(
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={
                    "USERNAME": username,
                    "PASSWORD": password,
                    "SECRET_HASH": secret_hash
                },
                ClientId=self.client_id
            )

            return {
                "id_token": response["AuthenticationResult"]["IdToken"],
                "access_token": response["AuthenticationResult"]["AccessToken"],
                "refresh_token": response["AuthenticationResult"]["RefreshToken"]
            }

        except self.client.exceptions.NotAuthorizedException:
            raise HTTPException(status_code=401, detail="Invalid username or password.")
        except self.client.exceptions.UserNotConfirmedException:
            raise HTTPException(status_code=403, detail="User account not confirmed.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")
        
    def decode_token(self, token: str):
        """
        Decode and validate a JWT token.
        """
        try:
            # Decode token without verification to read claims
            claims = jwt.decode(
                token,
                key=None,  # No key needed for decoding; this doesn't verify
                options={"verify_signature": False}
            )
            return claims
        except JWTError as e:
            raise HTTPException(status_code=401, detail=f"Token validation failed: {str(e)}")

    def check_user_role(self, claims, required_role: str):
        """
        Check if the token contains the required role.
        """
        try:
            groups = claims.get("cognito:groups", [])
            if required_role in groups:
                return True
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        except Exception as e:
            raise HTTPException(status_code=403, detail=f"Invalid token or permissions: {str(e)}")
