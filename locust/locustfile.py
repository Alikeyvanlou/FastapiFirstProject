from locust import HttpUser, task, between
from faker import Faker

fake = Faker()

class ApiUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.authenticated = False
        self.username = f"loadtest-{fake.uuid4()}"
        register_resp = self.client.post("/users/register", json={
            "username": self.username,
            "email": f"{self.username}@gmail.com",
            "password": "123456",
            "password_repeat": "123456",
            "is_fake": True
        })
        if register_resp.status_code not in (200, 201):
            print(f"Register failed: {register_resp.status_code} - {register_resp.text}")
            return

        login_resp = self.client.post("/users/login", data={
            "username": self.username,
            "password": "123456"
        })
        if login_resp.status_code != 200:
            print(f"Login failed: {login_resp.status_code} - {login_resp.text}")
            return

        self.token = login_resp.json()["access_token"]
        self.authenticated = True

    @task(2)
    def about_me(self):
        if not self.authenticated:
            return
        self.client.get("/users/me", headers=self.head())

    @task(3)
    def create_cost(self):
        if not self.authenticated:
            return
        resp = self.client.post("/costs/", headers=self.head(), json={
            "title": "shop",
            "amount": 2.1
        })
        if resp.status_code == 200 or resp.status_code == 201:
            self.last_cost_id = resp.json()["id"]

    @task(1)
    def edit_cost(self):
        if not self.authenticated:
            return
        if hasattr(self, "last_cost_id"):
            self.client.put(f"/costs/{self.last_cost_id}", headers=self.head(), json={
                "title": "fun",
                "amount": 2.1
            })

    @task(1)
    def delete_cost(self):
        if not self.authenticated:
            return
        if hasattr(self, "last_cost_id"):
            self.client.delete(f"/costs/{self.last_cost_id}", headers=self.head())
            del self.last_cost_id

    def head(self):
        return {"Authorization": f"Bearer {self.token}"}
    
        