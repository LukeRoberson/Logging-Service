# Logging Service

The logging service. Manages logs and messages from multiple sources, and handles them appropriately.

This includes logging to live alerts, SQL, or sending messages to Teams.
</br></br>

> [!NOTE]  
> Additional documentation can be found in the **docs** folder
</br></br>



----
# Project Organization
## Python Files

| File          | Provided Function                                             |
| ------------- | ------------------------------------------------------------- |
| main.py       | Entry point to the service, load configuration, set up routes |
| api.py        | API endpoints for this service                                |
| log.py        | Forwards logs and messages to their destinations              |
</br></br>



---
# Incoming Events

Plugins and services will send alerts to the logging service through the API. In the back end, these are handled by the _LogHandler_ class in _log.py_.

The purpose of this class is to:
1. Validate the contents of the event
2. Decide which locations to send to
3. Forward events or handle them locally as needed.
</br></br>


## Data format

The format of data that this class handles is:
```json
{
  "source": "Plugin or service name",
  "destination": [
    "dest-1",
    "dest-n"
  ],
  "log": {
    "group": "major category",
    "category": "minor category",
    "alert": "event alert",
    "severity": "info",
    "timestamp": "date and time",
    "message": "Log message"
  },
  "teams": {
    "destination": "chat destination",
    "message": "chat message"
  },
  "sql": {
    "destination": "table",
    "fields": {
      "field-1": "data",
      "field-n": "data"
    }
  }
}
```

The source, destination, and log fields are mandatory. The teams and sql fields are optional, depending on whether they are needed.
</br></br>


## Destinations

Events can have these locations:

| Destination | Description                                                      |
| ----------- | ---------------------------------------------------------------- |
| web         | Live alerts, that will be shown in the /alerts page on the WebUI |
| teams       | A message sent to a Chat ID                                      |
| sql         | Store entries in an SQL database                                 |
| syslog      | Send events to an external syslog server                         |
</br></br>


### Web / Live Alerts

The /alerts page displays live alerts. The logging service collects these alerts and stores them in an SQLite database locally.

When the WebUI requires alerts, it will make an API call to the logging service to collect the alerts it needs to display. This includes filtering based on various criteria.
</br></br>


### Teams

Messages are sent to Teams through the Teams Service. Interaction is through the service's API.
</br></br>

