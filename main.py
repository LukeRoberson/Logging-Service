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

from log import LogHandler


# Logging level can be set to DEBUG, INFO, WARNING, ERROR, or CRITICAL
LOGGING_LEVEL = "INFO"
logging.basicConfig(level=logging.INFO)

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
        print(log_handler.data)

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
