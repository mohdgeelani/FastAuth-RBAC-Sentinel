import requests
import time
import random

BASE_URL = "http://localhost:8000"

USERS = [
    {"username": "newadmin@example.com", "password": "new123"},
    {"username": "user1234@example.com", "password": "string1234"}
]

# Login and get token
def get_token(username, password):
    r = requests.post(f"{BASE_URL}/login", data={
        "username": username,
        "password": password
    })
    if r.status_code == 200:
        return r.json()["access_token"]
    else:
        print(f"Login failed for {username}: {r.text}")
        return None

# Call protected endpoint
def get_me(token):
    r = requests.get(f"{BASE_URL}/users/me", headers={
        "Authorization": f"Bearer {token}"
    })
    print(f"/users/me -> {r.status_code}")

# Create new user (admin only)
def create_user(token):
    new_email = f"user{random.randint(1000,9999)}@example.com"
    r = requests.post(f"{BASE_URL}/users/", json={
        "email": new_email,
        "password": "testpass",
        "role": "user"
    }, headers={
        "Authorization": f"Bearer {token}"
    })
    print(f"POST /users -> {r.status_code}")

if __name__ == "__main__":
    # Get tokens
    tokens = {}
    for user in USERS:
        token = get_token(user["username"], user["password"])
        if token:
            tokens[user["username"]] = token

    # Run traffic for ~1 minute
    start = time.time()
    while time.time() - start < 180:
        for username, token in tokens.items():
            get_me(token)
            if "admin" in username:  # Only admin creates users
                create_user(token)
        # time.sleep(0.2)  # Half a second between requests
