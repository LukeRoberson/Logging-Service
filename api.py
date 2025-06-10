"""
Module: api.py

Adds API endpoints for the logging service.

Blueprints:
    - log_api: Handles API endpoints for logging and health checks.

Routes:
    - /api/health:
        Test endpoint for health checks. Used by Docker.

Dependencies:
    - Flask: For creating the API routes.
    - logging: For logging messages.

Custom Dependencies:
    - LogHandler: Custom handler for processing log messages.
"""


# Standard library imports
import logging
from flask import (
    Blueprint,
    jsonify,
    request,
)

# Custom imports
from log import LogHandler


# Create a Flask blueprint for the API
log_api = Blueprint(
    'log_api',
    __name__
)


@log_api.route(
    '/api/health',
    methods=['GET']
)
def health():
    """
    Health check endpoint.
    Returns a JSON response indicating the service is running.
    """

    return jsonify(
        {'status': 'ok'}
    ), 200


@log_api.route(
    '/api/log',
    methods=['POST']
)
def log():
    """
    Logging endpoint.
    Accepts a JSON payload with a log message and destination.

    The payload should contain the following fields:
        - source: The source of the log message (e.g., plugin name).
        - destination: The destination for the log message (eg, 'sql').
        - log: The actual log message to be processed.

    Returns a JSON response indicating success or failure.
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
