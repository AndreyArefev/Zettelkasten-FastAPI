import json

def test_create_user(client):
    data = {"email":"testuser@nofoobar.com","username":"testuser","password":"testing"}
    response = client.post("/auth/sign-up/",json.dumps(data))
    assert response.status_code == 201
    assert response.json()["access_token"] is not None
    assert response.json()["token_type"] == 'bearer'

def test_create_jobs_noAuth(client):
    data = {
  "idea_name": "string",
  "idea_text": "string",
  "tags": [
    {
      "tag_name": "string"
    }
  ],
  "children": [
    {
      "idea_name": "string"
    }
  ],
  "data_create": "2022-08-10"
}
    response = client.post("/ideas/",json.dumps(data))
    assert response.status_code == 401

def test_create_jobs_Auth(client):
    data = {
  "idea_name": "string",
  "idea_text": "string",
  "tags": [
    {
      "tag_name": "string"
    }
  ],
  "children": [
    {
      "idea_name": "string"
    }
  ],
  "data_create": "2022-08-10"
}
    response = client.post("/ideas/",json.dumps(data))
    assert response.status_code == 401
    assert response.json()["idea_name"] == "string"
    assert response.json()["data_create"] == "2022-08-10"
