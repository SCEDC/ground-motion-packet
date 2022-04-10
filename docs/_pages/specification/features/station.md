Navigation
----------

 - [About](../../index.md)
 - [GeoJSON Overview](../../geojson.md)
 - [Terminology](../../terms.md)
 - Specification
   - [Base Dictionary](../base.md)
   - [Event Dictionary](../event.md)
   - [Provenance](../provenance.md)
   - Features
     - [Stations](station.md)
     - [Streams and Traces](streams_traces.md)
     - [Metrics Dictionary](metrics_dict.md)


Stations
========

The GeoJSON features represent seismic stations in the GMP specification. 
Station metadata is included in the GeoJSON feature "properties" dictionary. 
Requited properties include:

<dl>
  <dt>network_code</dt>
    <dd>The <a href="https://www.fdsn.org/networks/">FSDN</a>
    network code <i>(string; required)</i>.</dd>
  <dt>station_code</dt>
    <dd>FDSN station code <i>(string; required)</i>.</dd>
  <dt>name</dt>
    <dd>Station name <i>(string; optional)</i>.</dd>
  <dt>streams</dt>
    <dd>A list of dictionaries, one for each stream at this station. 
    <i>(list; required)</i>.</dd>
</dl>

> NOTE: "depth" in the station geometry coordinates array is defined as 
> meters positive from the WGS84 datum. This conforms with GEOJSON
> standard, but defiates from metadata convention.

Example:

```json
{
    ...
    "features": [
        {
            "type": "Feature",
            "properties": {
                "network_code": "CI",
                "station_code": "CCC",
                "name": "Christmas Canyon China Lake",
                "streams": [
                    {
                        ...
                    },
                    ...
                ]
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    -117.3645,
                    35.5249,
                    670.0
                ]
            }
        }
    ]
}
```
