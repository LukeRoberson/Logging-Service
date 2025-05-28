"""
Main module for handling log messages and alerts
    Send messages to:
        - Web interface
        - Teams
        - Syslog
        - SQL
"""

from flask import (
    Flask,
    jsonify,
    request
)

import logging
import requests

from log import LogHandler


# Get global config
global_config = None
try:
    response = requests.get("http://web-interface:5100/api/config", timeout=3)
    response.raise_for_status()  # Raise an error for bad responses
    global_config = response.json()

except Exception as e:
    logging.critical(
        "Failed to fetch global config from web interface."
        f" Error: {e}"
    )

if global_config is None:
    raise RuntimeError("Could not load global config from web interface")

# Set up logging
log_level_str = global_config['config']['web']['logging-level'].upper()
log_level = getattr(logging, log_level_str, logging.INFO)
logging.basicConfig(level=log_level)
logging.info("Logging level set to: %s", log_level_str)


# Create the Flask application
app = Flask(__name__)


@app.route(
    '/api/health',
    methods=['GET']
)
def health():
    """
    Health check endpoint.
    Returns a JSON response indicating the service is running.
    """

    return jsonify({'status': 'ok'})


@app.route(
    '/api/log',
    methods=['POST']
)
def log():
    """
    Logging endpoint.
    Accepts a JSON payload with a log message and destination.
    """

    data = request.get_json()
    logging.info("Received payload: %s", data)

    # Simple validation to check main fields in the payload
    if not all(field in data for field in ("source", "destination", "log")):
        logging.error("Missing required fields in payload")
        return jsonify(
            {
                "result": "error",
                "error": "Missing required fields"
            }
        ), 400

    # Create an instance of LogHandler
    with LogHandler(data) as log_handler:
        logging.debug("Log handler: %s", log_handler.data)

    return jsonify(
        {'result': 'success'}
    )


'''
NOTE: When running in a container, the host and port are set in the
    uWSGI config. uWSGI starts the process, which means the
    Flask app is not run directly.
    This can be uncommented for local testing.
'''
# if __name__ == "__main__":
#     # Run the application
#     app.run(
#         debug=True,
#         host='0.0.0.0',
#         port=5000,
#     )
