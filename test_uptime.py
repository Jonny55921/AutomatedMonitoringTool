import requests
import json

# Define the URL and data
url = 'http://localhost:5000/check_uptime'
data = {'url': 'https://www.nonexistentwebsite12345.com'}

# Send POST request
response = requests.post(url, json=data)

# Print the response
print(f"Status Code: {response.status_code}")
print(f"Response JSON: {response.json()}")
