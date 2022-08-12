from ..services.auth import AuthService
from fastapi.testclient import TestClient
from ..models.auth import UserCreate
from sqlalchemy.orm import Session
import json


def user_authentication_headers(client: TestClient, email: str, username: str, password: str):
    data = {
  "email": email,
  "username": username,
  "password":  password
}
    response = client.post("/auth/sign-up/", json.dumps(data))
    auth_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def authentication_token_from_email(client: TestClient, email: str, db: Session):
    """
    Return a valid token for the user with given email.
    If the user doesn't exist it is created first.
    """
    password = "random-passW0rd"
    username = "random-username"
    #user = AuthService.get_user_by_email(email=email, db=db)
    #if not user:
       # user_in_create = UserCreate(email = email, username= username, password = password)
        #user = auth_service.register_new_user(user_data = user_in_create)
    return user_authentication_headers(client=client, email=email, username=username, password=password)