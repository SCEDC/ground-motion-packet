## Event

The event dictionary contains the following keys. Note that the event parameters listed
here can become outdated as new information becomes available. For anyone using these
data we strongly encourage you to retrieve updated event information from the USGS
[Comcat](https://earthquake.usgs.gov/earthquakes/search/) database 
([Comcat API documentation](https://earthquake.usgs.gov/fdsnws/event/1/)).

**type**
:  The value is always "Feature" *(string; required)*.

**properties**
:  A dictionary with the following keys *(dictionary; required)*:

   **id**
   :  A unique event id *(string; required)*.

   **time**
   :  Event origin time in UTC ISO 8601 *extended* format (i.e., with 
      separators between the year, month, and day, and the hour, minutes,
      and seconds, and with a “T” between the date and time)*(string; 
      required)*.

   **magnitude**
   :   Earthquake magnitude *(float; required)*.

**geometry**
:  A dictionary with the following keys *(dictionary; required)*;

   **type**
   :  The value is always "Point" *(string; required)*.

   **coordinates**
   :  A list of three floats: longitude, latitude, and depth.


Including the "event" dictionary is not required, but if it is present then the 
above elements are required.

```{note} 
"depth" in the events geometry coordinates array conforms with the
GeoJSON standard (meters above WGS datum). This is different from
seismic metadata convention, which is kilometers positive downward.
```

The following example illustrates the "event" dictionary:

```{code-block} json
---
force: true
---
{
    ...
    "event": {
        "type": "Feature",
        "properties": {
            "id": "ci38457511",
            "time": "2019-07-06T03:19:53Z",
            "magnitude": 7.1
        },
        "geometry": {
            "type": "Point",
            "coordinates": [
                -117.599,
                35.77,
                8.0
            ]
        }
    }
}
```
