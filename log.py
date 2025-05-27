'''
Class for logging messages
'''

import logging
import traceback


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

        print("Initializing LogHandler")
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

        print("Entering LogHandler context manager")
        print(f"Payload: {self.data}")

        self._validate_payload()

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
            logging.debug(
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
        Validates the payload to ensure it contains required fields.
        """

        print("Validating payload")

    def send_to_web(
        self,
    ) -> None:
        """
        Sends the log message to the web interface.
        This is simple real-time logs
        """

        print("Sending log to web interface")
        print("This has not been implemented yet")

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
