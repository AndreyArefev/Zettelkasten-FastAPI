import json

def test_create_user(client):
    data = {"email":"testuser@nofoobar.com","username":"testuser","password":"testing"}
    response = client.post("/auth/sign-up/",json.dumps(data))
    assert response.status_code == 201
    assert response.json()["access_token"] is not None
    assert response.json()["token_type"] == 'bearer'

def test_no_create_user(client):
    data = {"username":"testuser","password":"testing"}
    response = client.post("/auth/sign-up/",json.dumps(data))
    assert response.status_code == 422


def test_create_ideas_noAuth(client):
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

def test_create_ideas_Auth(client,normal_user_token_headers):
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
      "idea_name": "string22"
    }
  ],
  "data_create": "2022-08-10"
}
    response = client.post("/ideas/", json.dumps(data), headers=normal_user_token_headers)
    print(response.json())
    assert response.status_code == 201
    assert response.json()["idea_name"] == "string"
    assert response.json()["data_create"] == "2022-08-10"

def test_create_ideas_link_self(client,normal_user_token_headers):
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
    response = client.post("/ideas/", json.dumps(data), headers=normal_user_token_headers)
    print(response.json())
    assert response.status_code == 422
