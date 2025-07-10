# Use the custom base image
FROM lukerobertson19/base-os:latest

# OCI labels for the image
LABEL org.opencontainers.image.title="AI Assistant Logging Service"
LABEL org.opencontainers.image.description="The logging service manages all alerts, whether from plugins or the system itself. It provides a unified interface for forwaring logs to locations such as SQL, Syslog, Teams, or live alerts in the web interface"
LABEL org.opencontainers.image.base.name="lukerobertson19/base-os:latest"
LABEL org.opencontainers.image.source="https://github.com/LukeRoberson/Logging-Service"
LABEL org.opencontainers.image.version="1.0.0"

# The health check URL for the service
LABEL net.networkdirection.healthz="http://localhost:5100/api/health"

# The name of the service, as it should appear in the compose file
LABEL net.networkdirection.service.name="logging"

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Start the application using uWSGI
CMD ["uwsgi", "--ini", "uwsgi.ini"]

# Set the version of the image in metadata
ARG VERSION
LABEL org.opencontainers.image.version="${VERSION}"
