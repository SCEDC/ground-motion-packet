Navigation
----------

 - [About](../index.md)
 - [GeoJSON Overview](../geojson.md)
 - [Terminology](../terms.md)
 - Specification
   - [Base Dictionary](base.md)
   - [Event Dictionary](event.md)
   - [Provenance](provenance.md)
   - [Guidelines for Data Providers](guidelines-provider.md)
   - Features
     - [Stations](features/station.md)
     - [Streams and Traces](features/streams_traces.md)
     - [Metrics Dictionary](features/metrics_dict.md)

Event
=====

The event dictionary contains the following keys:

<dl>
  <dt>type</dt>
    <dd>
      The value is always "Feature" <i>(string; required)</i>.
    </dd>
  <dt>properties</dt>
    <dd>A dictionary with the following keys <i>(dictionary; required)</i>:
    <dl>
      <dt>id</dt>
        <dd>
          A unique event id <i>(string; required)</i>.
        </dd>
      <dt>time</dt>
        <dd>
          Event origin time in UTC ISO 8601 *extended* format (i.e., with separators between the year, month, and day, and the hour, minutes, and seconds, and with a “T” between the date and time)<i>(string; required)</i>.
        </dd>
      <dt>magnitude</dt>
        <dd>
          Earthquake magnitude <i>(float; required)</i>.
        </dd>
    </dl>
    </dd>
  <dt>geometry</dt>
    <dd>
      A dictionary with the following keys <i>(dictionary; required)</i>;
    <dl>
      <dt>type</dt>
        <dd>
          The value is always "Point" <i>(string; required)</i>.
        </dd>
      <dt>coordinates</dt>
        <dd>
          A list of three floats: longitude, latitude, and depth.
        </dd>
    </dl>
    </dd>
</dl>


Including the "event" dictionary is not required, but if it is present then the 
above elements are required.

> NOTE: "depth" in the events geometry coordinates array conforms with the
> GeoJSON standard (meters above WGS datum). This is different from
> seismic metadata convention, which is kilometers positive downward.

The following example illustrates the "event" dictionary:

```json
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
