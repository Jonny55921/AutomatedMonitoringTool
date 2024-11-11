import requests
from flask import Blueprint, jsonify, request
from datetime import datetime
from . import mongo
import ssl
import socket

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

def check_ssl_cert(url):
    try:
        hostname = url.replace("https://", "").replace("http://", "").split("/")[0]

        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443),timeout=5) as sock:
            with context.wrap_socket(sock,server_hostname=hostname) as ssock:
                cert=ssock.getpeercert()
        
        expire_date_str = cert['notAfter']
        expire_date = datetime.strptime(expire_date_str,'%b %d %H:%M:%S %Y %Z' )
        current_date = datetime.utcnow()

        is_valid = current_date < expire_date

        return{
            "url": url,
            "ssl_valid": is_valid,
            "expiry_date": expire_date_str,
            "issuer": cert.get('issuer')
        }
    except Exception as e:
        return{
            "url": url,
            "ssl_valid": False,
            "error": str(e)
        }
    
def check_version(url):
    try:
        response = requests.get(url,timeout=5)
        headers = response.headers
        server_info = headers.get("Server", "Unknown")
        x_powered_by = headers.get("X-Powered-By", "Unknown")

        return{
            "url": url,
            "server_info": server_info,
            "x_powered_by": x_powered_by
        }

    except requests.exceptions.RequestException as e:
        return{
            "url": url,
            "server_info": "Error",
            "error": str(e)
        }

@main.route('/check_security', methods=['POST'])
def check_security():
    data = request.json()
    url = data.get('url')

    if not url:
<<<<<<< HEAD
        return jsonify({"error": "URL is required"}), 400
    
    ssl_check_result = check_ssl_cert(url)
    software_check_result = check_version(url)

    security_results = {
        "url": url,
        "ssl_check": ssl_check_result,
        "software_check": software_check_result
    }

    mongo.db.security_checks.insert_one(security_results)

    return jsonify(security_results)
=======
        return jsonify({"error": "URL is required"}), 400
>>>>>>> backup-branch
