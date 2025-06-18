# API
## Endpoints

There is an API in place so other services can send logs/events or request logs.

| Endpoint        | Methods | Description                                    |
| --------------- | ------- | ---------------------------------------------- |
| /api/health     | GET     | Check the health of the container              |
| /api/log        | POST    | Plugins/services send their events here        |
| /api/livealerts | GET     | Filter and retrieve live alert logs            |
</br></br>


## Responses

Unless otherwise specified, all endpoints have a standard JSON response, including a '200 OK' message if everything is successful.

A successful response:
```json
{
    'result': 'success'
}
```

An error:
```json
{
    "result": "error",
    "error": "A description of the error"
}
```
</br></br>


### Health

This is for checking that Flask is responding from the localhost, so Docker can see if this is up.

This just returns a '200 OK' response.
</br></br>


## Endpoint Details
### Logging

This endpoint receives alerts from other services and plugins. The body of the message is expected to be in this format:

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

Source, destination, and log areas are mandatory, while teams and sql are optional, depending on whether they're needed.

The API will create an instance of LogHandler to decide how to handle the event.
</br></br>


### Live Alerts

This endpoint returns a list of live alerts. These may be filtered, or it may include all alerts.

Several parameters can be provided to filter the results:
* search - A string to search for
* system_only - To filter out only system logs (no plugin logs)
* source - The source of an event (such as a service or plugin name)
* group - The alert group
* category - The alert category
* alert_type - The type of the alert
* severity - The alert severity, such as info, warning, etc

Additionally, there are parameters to control pagination:
* page_size - The number of alerts to include in a single page (200 by default)
* page_number - The offset into the log event to start with

There is currently no restriction on the number of alerts that can be returned per page.
</br></br>


A successful operation will return:
```json
{
    "result": "success",
    "alerts": "<a list of alerts>",
    "page_size": "<the number of alerts per page>",
    "total_pages": "<the total number of pages found>",
    "page_number": "<the page number being returned>",
    "total_logs": "<the total number of logs matching the query>",
}
```
</br></br>
