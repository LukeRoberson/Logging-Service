'''
Module: log.py

Sends log messages to various destinations, including:
    - Web interface (live alerts)
    - Microsoft Teams
    - Syslog server
    - SQL database (for long-term storage)

Classes:
    LogHandler
        Handles log messages and sends them to specified destinations.
        Can be used as a context manager for resource management.

Dependencies:
    requests: For sending HTTP requests to web interface and Teams
    logging: For logging messages to the terminal
    traceback: For logging exceptions with full tracebacks
    flask.current_app: For accessing the Flask application context

Custom Imports:
    livealerts.LiveAlerts: For handling live alert logging
'''

# Standard library imports
import logging
import traceback
import requests
from flask import current_app
from typing import cast

# Custom imports
from livealerts import LiveAlerts


TEAMS_MESSAGE_URL = "http://teams:5100/api/message"


class LogHandler:
    """
    Handles log messages and sends them to specified destinations.
    It can send messages to different destinations like web
        interface, Teams, syslog, and SQL.

    args:
        data (dict): The payload containing log message and destination.
    """

    def __init__(
        self,
        data: dict
    ) -> None:
        """
        Initializes the LogHandler instance.
        Sets up the logging configuration.

        Args:
            data (dict): The payload containing log message and destination.
        """

        # Track the payload data
        self.data = data

    def __enter__(
        self,
    ) -> "LogHandler":
        '''
        Context manager setup for LogHandler.
        This allows the LogHandler to be used in a with statement,
            ensuring proper resource management.

        Returns:
            LogHandler: The instance of LogHandler.
        '''

        logging.info("Body data received: %s", self.data)

        # Validate the payload to ensure it contains required fields
        if not self._validate_payload():
            raise ValueError("Invalid log payload: missing required fields.")

        # Send messages to the appropriate destinations
        if "web" in self.data["destination"]:
            self.send_to_web()

        if "teams" in self.data["destination"]:
            self.send_to_teams()

        if "syslog" in self.data["destination"]:
            self.send_to_syslog()

        if "sql" in self.data["destination"]:
            self.send_to_sql()

        return self

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb
    ) -> None:
        """
        Context manager teardown for LogHandler.
        This ensures that any resources are cleaned up after use.

        Args:
            exc_type: The type of exception raised, if any.
            exc_val: The value of the exception raised, if any.
            exc_tb: The traceback object, if any.
        """

        # Log an error if an exception occurred
        if exc_type is not None:
            # Log error to terminal
            logging.error(
                f"A {exc_type} error occurred: {exc_val}"
            )

            # Log the full traceback to terminal
            logging.info(
                ''.join(traceback.format_exception(exc_type, exc_val, exc_tb))
            )

    def __str__(
        self
    ) -> str:
        """
        Returns a string representation of the LogHandler instance.
        This is used for debugging and logging purposes.

        Returns:
            str: A string representation of the LogHandler instance.
        """

        return "<LogHandler: handles web, teams, syslog, sql>"

    def __repr__(
        self
    ) -> str:
        """
        Returns a detailed string representation of the LogHandler instance.
        This is used for debugging and logging purposes.

        Returns:
            str: A detailed string representation of the LogHandler instance.
        """

        return f"<LogHandler(id={id(self)})>"

    def _validate_payload(
        self,
    ) -> bool:
        """
        Parses the payload and checks for necessary fields.

        Returns:
            bool: True if the payload is valid, False otherwise.
        """

        # Track the source and destination
        self.source = self.data["source"]
        self.destination = self.data["destination"]

        # Check if the payload contains log fields
        required_fields = [
            "category",
            "alert",
            "severity",
            "timestamp",
            "message",
        ]
        for field in required_fields:
            if field not in self.data["log"]:
                logging.error(f"Missing required log field: {field}")
                return False

        self.category = self.data["log"]["category"]
        self.severity = self.data["log"]["severity"]
        self.alert = self.data["log"]["alert"]
        self.timestamp = self.data["log"]["timestamp"]
        self.message = self.data["log"]["message"]

        if "group" in self.data["log"]:
            self.group = self.data["log"]["group"]
        else:
            self.group = ""

        # Check Teams fields
        if "teams" in self.data["destination"]:
            if "teams" not in self.data:
                logging.error("Missing 'teams' field in payload")
                return False

            required_teams_fields = ["destination", "message"]
            for field in required_teams_fields:
                if field not in self.data["teams"]:
                    logging.error(f"Missing required Teams field: {field}")
                    return False

            self.teams_destination = self.data["teams"]["destination"]
            self.teams_message = self.data["teams"]["message"]

        # Check sql fields
        if "sql" in self.data["destination"]:
            if "sql" not in self.data:
                logging.error("Missing 'sql' field in payload")
                return False

            required_sql_fields = ["destination"]
            for field in required_sql_fields:
                if field not in self.data["sql"]:
                    logging.error(f"Missing required SQL field: {field}")
                    return False

            self.sql_destination = self.data["sql"]["destination"]
            self.sql_fields = self.data["sql"]["fields"]

        return True

    def send_to_web(
        self,
    ) -> None:
        """
        Stores the log messages in the local database. These can be retrieved
            by the web interface for live alerts

        Args:
            None

        Returns:
            None
        """

        logging.info(
            "Saving log to local database: %s",
            self.data['log']['message']
        )

        # Get the LiveAlerts instance from the current Flask app context
        logger = cast(LiveAlerts, current_app.config.get('LOGGER'))

        logger.log_alert(
            timestamp=self.timestamp,
            source=self.source,
            group=self.group,
            category=self.category,
            alert=self.alert,
            severity=self.severity,
            message=self.message
        )

        logger.purge_old_alerts()

    def send_to_teams(
        self,
    ) -> None:
        """
        Sends the log message to Microsoft Teams.
            Uses the Teams service to send messages
        """

        # API call to the Teams service
        logging.info("LogHandler.sent_to_teams: Sending log to Teams")
        try:
            requests.post(
                TEAMS_MESSAGE_URL,
                json={
                    "chat-id": self.data["teams"]["destination"],
                    "message": self.data["teams"]["message"],
                },
                timeout=3
            )

        except Exception as e:
            logging.warning(
                "Failed to send log to Teams service. %s",
                e
            )

    def send_to_syslog(
        self,
    ) -> None:
        """
        Sends the log message to a syslog server.
        This goes straight to syslog server, not through anoter service
        """

        print("Sending log to syslog")
        print("This has not been implemented yet")

    def send_to_sql(
        self,
    ) -> None:
        """
        Sends the log message to a SQL database.
        This is for long-term storage of logs
        Uses the SQL service to send messages
        """

        print("Sending log to SQL database")
        print("This has not been implemented yet")
