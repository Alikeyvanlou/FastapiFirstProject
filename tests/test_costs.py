# cost reading tests:
def test_get_cost_200(client, auth_user):
    response = client.get("/costs/", headers=auth_user)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_cost_401(client):
    response = client.get("/costs/")
    assert response.status_code == 401


# cost reading by id tests:
def test_get_cost_by_id_200(client, create_cost, auth_user):
    cost_id = create_cost.json()["id"]
    response = client.get(f"/costs/{cost_id}", headers=auth_user)
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, dict)
    assert data["title"] == "gym"
    assert data["amount"] == 2.1


def test_get_cost_by_id_401(client, create_cost):
    cost_id = create_cost.json()["id"]
    response = client.get(f"/costs/{cost_id}")
    assert response.status_code == 401


def test_get_cost_by_id_404(client, create_cost, auth_user):
    cost_id = create_cost.json()["id"] + 1
    response = client.get(f"/costs/{cost_id}", headers=auth_user)
    data = response.json()
    assert response.status_code == 404
    assert not data["success"]
    assert data["error"]["message"] == f"No cost with id {cost_id} was found."


# cost create tests:
def test_create_cost_201(create_cost):
    data = create_cost.json()
    assert isinstance(data, dict)
    assert data["title"] == "gym"
    assert data["amount"] == 2.1


def test_create_cost_bad_title_422(client, auth_user):
    response = client.post("/costs/", json={"title": "", "amount": 2.1}, headers=auth_user)
    data = response.json()
    assert response.status_code == 422
    assert not data["success"]
    assert data["error"][0]["filed"] == "title"
    assert data["error"][0]["message"] == "String should have at least 2 characters"


def test_create_cost_bad_amount_422(client, auth_user):
    response = client.post("/costs/", json={"title": "gym", "amount": ""}, headers=auth_user)
    data = response.json()
    assert response.status_code == 422
    assert not data["success"]
    assert data["error"][0]["filed"] == "amount"
    assert (
        data["error"][0]["message"]
        == "Input should be a valid number, unable to parse string as a number"
    )


# cost edit tests:
def test_edit_cost_200(client, create_cost, auth_user):
    cost_id = create_cost.json()["id"]
    response = client.put(
        f"/costs/{cost_id}", headers=auth_user, json={"title": "gym", "amount": 3.4}
    )
    data = response.json()
    assert response.status_code == 200
    assert data["title"] == "gym"
    assert data["amount"] == 3.4


def test_edit_cost_401(client, create_cost):
    cost_id = create_cost.json()["id"]
    response = client.put(f"/costs/{cost_id}", json={"title": "gym", "amount": 3.4})
    data = response.json()
    assert response.status_code == 401
    assert not data["success"]
    assert data["error"]["message"] == "Not authenticated"


def test_edit_cost_404(client, create_cost, auth_user):
    cost_id = create_cost.json()["id"] + 1
    response = client.put(
        f"/costs/{cost_id}", headers=auth_user, json={"title": "gym", "amount": 3.4}
    )
    data = response.json()
    assert response.status_code == 404
    assert not data["success"]
    assert data["error"]["message"] == f"No cost with id {cost_id} was found."


# cost delete tests:
def test_delete_cost_204(client, create_cost, auth_user):
    cost_id = create_cost.json()["id"]
    response = client.delete(f"/costs/{cost_id}", headers=auth_user)
    assert response.status_code == 204


def test_delete_cost_404(client, create_cost, auth_user):
    cost_id = create_cost.json()["id"] + 1
    response = client.delete(f"/costs/{cost_id}", headers=auth_user)
    data = response.json()
    assert response.status_code == 404
    assert not data["success"]
    assert data["error"]["message"] == f"No cost with id {cost_id} was found."
