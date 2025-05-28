'''
Class for logging messages
'''

import logging
import traceback
import requests


# Logging level can be set to DEBUG, INFO, WARNING, ERROR, or CRITICAL
LOGGING_LEVEL = "INFO"
logging.basicConfig(level=logging.INFO)


class LogHandler:
    """
    Class for handling log messages.
    It can send messages to different destinations like web
        interface, Teams, syslog, and SQL.

    Methods:
        __init__: Initializes the LogHandler instance.
        __enter__: Context manager setup for LogHandler.
        __exit__: Context manager teardown for LogHandler.
        __str__: Returns a string representation of the LogHandler instance.
        __repr__: Returns a detailed string representation.
        _validate_payload: Validates the payload.
        send_to_web: Sends the log message to the web interface.
        send_to_teams: Sends the log message to Microsoft Teams.
        send_to_syslog: Sends the log message to a syslog server.
        send_to_sql: Sends the log message to a SQL database.
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
            self.group = None

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
        Sends the log message to the web interface.
            This is simple real-time logs

        Uses an API endpoint to send messages
        """

        logging.info(
            "Sending log to web interface: %s",
            self.data['log']['message']
        )

        # Send a log as a webhook to the web interface
        try:
            requests.post(
                "http://web-interface:5100/api/webhook",
                json={
                    "source": self.source,
                    "group": self.group,
                    "category": self.category,
                    "alert": self.alert,
                    "severity": self.severity,
                    "timestamp": self.timestamp,
                    "message": self.message,
                },
                timeout=3
            )

        except Exception as e:
            logging.warning(
                "Failed to send startup webhook to web interface. %s",
                e
            )

    def send_to_teams(
        self,
    ) -> None:
        """
        Sends the log message to Microsoft Teams.
        Uses the Teams service to send messages
        """

        print("Sending log to Teams")
        print("This has not been implemented yet")

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
