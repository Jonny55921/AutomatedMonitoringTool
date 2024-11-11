import requests
import json

# Define the URL for the security check endpoint and the data
url = 'http://localhost:5000/check_security'
data = {'url': 'https://www.example.com'}

# Send POST request to /check_security
response = requests.post(url, json=data)

# Print status code
print(f"Status Code: {response.status_code}")

# Try to print the response as JSON if possible
try:
    response_json = response.json()
    print("Response JSON:")
    print(json.dumps(response_json, indent=2))
except requests.exceptions.JSONDecodeError:
    # Print the raw response if JSON parsing fails
    print("Response is not in JSON format")
    print("Response Text:", response.text)
