import requests
from flask import Blueprint, jsonify, request
from datetime import datetime
from . import mongo

main = Blueprint('main', __name__)

# Uptime Monitoring Route with error handling and saving to MongoDB
@main.route('/check_uptime', methods=['POST'])
def check_uptime():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        # Send a request to the URL
        response = requests.get(url, timeout=5)
        status_code = response.status_code
        response_time = response.elapsed.total_seconds()  # Measure response time in seconds

        # Store the successful result in MongoDB
        result = {
            "url": url,
            "status_code": status_code,
            "response_time": response_time,
            "status": "up" if status_code == 200 else "down",
            "timestamp": datetime.now()  # Record the time of the check
        }
        mongo.db.uptime_results.insert_one(result)

        return jsonify({
            "url": url,
            "status": "up" if status_code == 200 else "down",
            "status_code": status_code,
            "response_time": response_time
        })

    except requests.exceptions.Timeout:
        # Handle timeout error and save to MongoDB
        result = {
            "url": url,
            "status": "down",
            "error": "Timeout: The request took too long to complete.",
            "timestamp": datetime.now()
        }
        mongo.db.uptime_results.insert_one(result)

        return jsonify(result), 504  # 504 Gateway Timeout

    except requests.exceptions.ConnectionError:
        # Handle connection errors and save to MongoDB
        result = {
            "url": url,
            "status": "down",
            "error": "Connection Error: Unable to reach the server.",
            "timestamp": datetime.now()
        }
        mongo.db.uptime_results.insert_one(result)

        return jsonify(result), 503  # 503 Service Unavailable

    except requests.exceptions.InvalidURL:
        # Handle invalid URL error and save to MongoDB
        result = {
            "url": url,
            "status": "down",
            "error": "Invalid URL: The provided URL is not valid.",
            "timestamp": datetime.now()
        }
        mongo.db.uptime_results.insert_one(result)

        return jsonify(result), 400  # 400 Bad Request

    except requests.exceptions.RequestException as e:
        # Catch all other request-related errors and save to MongoDB
        result = {
            "url": url,
            "status": "down",
            "error": f"An error occurred: {str(e)}",
            "timestamp": datetime.now()
        }
        mongo.db.uptime_results.insert_one(result)

        return jsonify(result), 500  # 500 Internal Server Error
