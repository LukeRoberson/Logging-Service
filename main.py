"""
Module: main.py

Main module for handling log messages and alerts from services and plugins.
Manages sending messages to:
    - Web interface
    - Teams
    - Syslog
    - SQL

Module Tasks:
    1. Fetch global configuration from the web interface.
    2. Set up logging based on the global configuration.
    3. Create a Flask application instance and register API endpoints.

Usage:
    This is a Flask application that should run behind a WSGI server inside
        a Docker container.
    Build the Docker image and run it with the provided Dockerfile.

Functions:
    - fetch_global_config:
        Fetches the global configuration from the web interface.
    - logging_setup:
        Sets up the root logger (for terminal logging within the service).

Blueprints:
    - log_api: Handles API endpoints for logging and health checks.

Dependencies:
    - Flask: For creating the web application.
    - logging: For logging messages to the terminal.
    - requests: For making HTTP requests to the web interface.

Custom Dependencies:
    - api.log_api: Contains API endpoints for logging and health checks.
"""


# Standard library imports
from flask import Flask
import logging
import requests

# Custom imports
from api import log_api


CONFIG_URL = "http://web-interface:5100/api/config"


def fetch_global_config(
    url: str = CONFIG_URL,
) -> dict:
    """
    Fetch the global configuration from the web interface.

    Args:
        None

    Returns:
        dict: The global configuration loaded from the web interface.

    Raises:
        RuntimeError: If the global configuration cannot be loaded.
    """

    global_config = None
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        global_config = response.json()

    except Exception as e:
        logging.critical(
            "Failed to fetch global config from web interface."
            f" Error: {e}"
        )

    if global_config is None:
        raise RuntimeError("Could not load global config from web interface")

    return global_config


def logging_setup(
    config: dict,
) -> None:
    """
    Set up the root logger for the web service.

    Args:
        config (dict): The global configuration dictionary

    Returns:
        None
    """

    # Get the logging level from the configuration (eg, "INFO")
    log_level_str = config['config']['web']['logging-level'].upper()
    log_level = getattr(logging, log_level_str, logging.INFO)

    # Set up the logging configuration
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logging.info("Logging setup complete with level: %s", log_level)


# Get the global configuration for the app
global_config = fetch_global_config(CONFIG_URL)

# Set up logging
logging_setup(global_config)

# Create the Flask application
app = Flask(__name__)
app.register_blueprint(log_api)
