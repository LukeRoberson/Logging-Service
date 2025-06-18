"""
Module: api.py

Adds API endpoints for the logging service.

Blueprints:
    - log_api: Handles API endpoints for logging and health checks.

Routes:
    - /api/health:
        Test endpoint for health checks. Used by Docker.
    - /api/log:
        Endpoint for receiving log messages from plugins and services.
    - /api/livealerts:
        Endpoint for retrieving live alerts from the web interface.

Dependencies:
    - Flask: For creating the API routes.
    - logging: For logging messages.

Custom Dependencies:
    - LogHandler: Custom handler for processing log messages.
    - LiveAlerts: For handling live alerts in the web interface.
"""


# Standard library imports
import logging
from typing import cast
from flask import (
    Blueprint,
    Response,
    jsonify,
    make_response,
    request,
    current_app,
)

# Custom imports
from log import LogHandler
from livealerts import LiveAlerts


# Create a Flask blueprint for the API
log_api = Blueprint(
    'log_api',
    __name__
)


@log_api.route(
    '/api/health',
    methods=['GET']
)
def health() -> Response:
    """
    Health check endpoint.
    Returns a JSON response indicating the service is running.
    """

    return make_response(
        jsonify(
            {'status': 'ok'}
        ),
        200
    )


@log_api.route(
    '/api/log',
    methods=['POST']
)
def log() -> Response:
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
        return make_response(
            jsonify(
                {
                    "result": "error",
                    "error": "Missing required fields"
                }
            ),
            400
        )

    # Create an instance of LogHandler
    with LogHandler(data) as log_handler:
        logging.debug("Log handler: %s", log_handler.data)

    return make_response(
        jsonify(
            {
                'result': 'success'
            }
        ),
        200
    )


@log_api.route(
    '/api/livealerts',
    methods=['GET']
)
def livealerts() -> Response:
    """
    Endpoint to retrieve live alerts.
    Returns a JSON response with the current live alerts.

    Parameters:
        search (optional):
            A search term to filter live alerts.
        system_only (optional):
            If set to 'true', only system alerts are returned.
        source (optional):
            Filter alerts by source (e.g., plugin name).
        group (optional):
            Filter alerts by group.
        category (optional):
            Filter alerts by category.
        alert_type (optional):
            Filter alerts by type (e.g., 'error', 'warning').
        severity (optional):
            Filter alerts by severity level.
        page_size (optional):
            The number of alerts to return per page (default is 200).
        page_number (optional):
                The page number to retrieve (default is 1).

    Returns:
        Response: A JSON response containing the live alerts.
            Result - 'success' or 'error'
            alerts - List of live alerts
            page_size - Number of alerts per page
            total_pages - Total number of pages available
            page_number - Current page number
    """

    # Get a list of parameters, used for filtering live alerts
    search = request.args.get("search", default='', type=str)
    system_only = request.args.get("system_only", default='', type=str)
    source = request.args.get("source", default='', type=str)
    group = request.args.get("group", default='', type=str)
    category = request.args.get("category", default='', type=str)
    alert_type = request.args.get("alert_type", default='', type=str)
    severity = request.args.get("severity", default='', type=str)
    page_size = request.args.get("page_size", 200, type=int)
    page_number = request.args.get("page", 1, type=int)

    # If system_only is set and group is not, set group to 'service'
    if not group and system_only:
        group = 'service'

    # Get the LiveAlerts instance from the current Flask app context
    logger = cast(LiveAlerts, current_app.config.get('LOGGER'))

    # Manage pagination for alerts
    total_logs = logger.count_alerts(
        search=search,
        source=source,
        group=group,
        category=category,
        alert=alert_type,
        severity=severity,
    )
    total_pages = (total_logs + page_size - 1) // page_size

    # Collect a list of alerts
    alerts = logger.get_recent_alerts(
        offset=(page_number - 1) * page_size,
        limit=page_size,
        search=search,
        source=source,
        group=group,
        category=category,
        alert=alert_type,
        severity=severity,
    )

    logging.info(
        "Returning %d alerts for page %d/%d",
        len(alerts),
        page_number,
        total_pages
    )

    return make_response(
        jsonify(
            {
                "result": "success",
                "alerts": alerts,
                "page_size": page_size,
                "total_pages": total_pages,
                "page_number": page_number,
                "total_logs": total_logs,
            }
        ),
        200
    )
