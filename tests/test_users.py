def test_read_users_200(client):
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# register user test:
def test_register_user_201(register_user):
    data = register_user.json()
    assert register_user.status_code == 201
    assert data["username"] == "ali"
    assert data["email"] == "ali@example.com"


def test_register_user_pass_not_match_422(client):
    payload = {
        "username": "ali",
        "email": "ali@example.com",
        "password": "string",
        "password_repeat": "srindddg",
    }
    response = client.post("/users/register", json=payload)
    data = response.json()
    assert response.status_code == 422, data


def test_register_username_exist_400(client, register_user):
    new_payload = {
        "username": "ali",
        "email": "newali@example.com",
        "password": "1234567",
        "password_repeat": "1234567",
    }
    response = client.post("/users/register", json=new_payload)
    data = response.json()
    assert response.status_code == 400
    assert not data["success"]
    assert data["error"]["message"] == "The username already exists."


def test_register_email_exist_400(client, register_user):
    new_payload = {
        "username": "ali1",
        "email": "ali@example.com",
        "password": "1234567",
        "password_repeat": "1234567",
    }
    response = client.post("/users/register", json=new_payload)
    data = response.json()
    assert response.status_code == 400
    assert not data["success"]
    assert data["error"]["message"] == "The email already registered."


# login user test:
def test_login_user_200(login_user):
    data = login_user.json()
    assert isinstance(data, dict)
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_user_username_403(client, register_user):
    response = client.post("/users/login", data={"username": "ali1", "password": "string"})
    data = response.json()
    assert response.status_code == 403
    assert not data["success"]
    assert data["error"]["message"] == "username or password is incorrect."


def test_login_user_pass_403(client, register_user):
    response = client.post("/users/login", data={"username": "ali", "password": "string1"})
    data = response.json()
    assert response.status_code == 403
    assert not data["success"]
    assert data["error"]["message"] == "username or password is incorrect."


# user edit test:
def test_edit_user_200(client, auth_user):
    edit_payload = {
        "username": "alikey",
        "email": "alikey@example.com",
        "password": "1234567",
    }
    response = client.put("/users/", headers=auth_user, json=edit_payload)
    data = response.json()
    assert response.status_code == 200
    assert data["username"] == "alikey"
    assert data["email"] == "alikey@example.com"


def test_edit_user_401(client, login_user):
    edit_payload = {
        "username": "alikey",
        "email": "alikey@example.com",
        "password": "1234567",
    }
    response = client.put("/users/", json=edit_payload)
    data = response.json()
    assert response.status_code == 401
    assert not data["success"]
    assert data["error"]["message"] == "Not authenticated"


# delete user tests:
def test_delete_user_401(client, login_user):
    response = client.delete("/users/")
    data = response.json()
    assert response.status_code == 401
    assert not data["success"]
    assert data["error"]["message"] == "Not authenticated"


def test_delete_user_204(client, auth_user):
    response = client.delete("/users/", headers=auth_user)
    assert response.status_code == 204


# user info test:


def test_get_user_info_200(client, auth_user):
    response_user = client.get("/users/me", headers=auth_user)
    data = response_user.json()
    assert isinstance(data, dict)
    assert response_user.status_code == 200
    assert data["username"] == "ali"
    assert data["email"] == "ali@example.com"
    assert isinstance(data["costs"], list)
    assert data["id"] == 1


def test_get_user_info_401(client, login_user):
    response_user = client.get("/users/me")
    data = response_user.json()
    assert response_user.status_code == 401
    assert not data["success"]
    assert data["error"]["message"] == "Not authenticated"


# user refresh token:
def test_user_refresh_token_200(client, auth_user):
    response = client.post("/users/refresh")
    data = response.json()
    assert response.status_code == 200
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_user_refresh_token_401(client):
    response = client.post("/users/refresh")
    data = response.json()
    assert response.status_code == 401
    assert not data["success"]
    assert data["error"]["message"] == "Refresh token missing"
