from locust import HttpUser, task, between
import random

# Normal user simulation
class WebsiteUser(HttpUser):
    wait_time = between(0.2, 1)  # short gaps for heavier load

    def on_start(self):
        # Register user
        self.username = f"user{random.randint(1000, 99999)}"
        self.email = f"{self.username}@example.com"
        self.password = "testpass"
        reg_payload = {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "role": "user"
        }
        self.client.post("/register", json=reg_payload)

        # Login
        self.login()

    def login(self):
        login_payload = {
            "username": self.email,
            "password": self.password
        }
        r = self.client.post("/login", data=login_payload)
        if r.status_code == 200:
            self.token = r.json()["access_token"]
        else:
            self.token = None

    @task(3)
    def users_me(self):
        if self.token:
            self.client.get("/users/me", headers={"Authorization": f"Bearer {self.token}"})

    @task(1)
    def register_more(self):
        username = f"user{random.randint(1000, 99999)}"
        email = f"{username}@example.com"
        payload = {
            "username": username,
            "email": email,
            "password": "testpass",
            "role": "user"
        }
        self.client.post("/register", json=payload)

    @task(1)
    def relogin(self):
        # Keeps login endpoint active in traffic stats
        self.login()

# Admin user simulation
class AdminUser(HttpUser):
    wait_time = between(0.2, 1)

    def on_start(self):
        self.admin_email = "admintoday@example.com"
        self.admin_password = "string"
        self.login_admin()

    def login_admin(self):
        login_payload = {
            "username": self.admin_email,
            "password": self.admin_password
        }
        r = self.client.post("/login", data=login_payload)
        if r.status_code == 200:
            self.token = r.json()["access_token"]
        else:
            self.token = None

    @task
    def call_admin_endpoint(self):
        if self.token:
            self.client.get(
                "/admin-only",
                headers={"Authorization": f"Bearer {self.token}"}
            )

