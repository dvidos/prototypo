import requests
from faker import Faker

API_URL = "http://localhost:8000/api/customers/"
NUM_CUSTOMERS = 500

fake = Faker()

for _ in range(NUM_CUSTOMERS):
    customer = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.unique.email(),
        "address": fake.address().replace("\n", ", ")
    }
    response = requests.post(API_URL, json=customer)
    if response.status_code > 299:
        print(f"Failed: {response.status_code} - {response.text}")
