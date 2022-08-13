from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import json


def user_authentication_headers(client: TestClient, email: str):
    data = {
  "email": email,
  "username": "random-passW0rd",
  "password":  "random-username"
}
    response = client.post("/auth/sign-up/", json.dumps(data))
    auth_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers
