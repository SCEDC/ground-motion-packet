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

Base Dictionary
===============

For the base GeoJSON dictionary, the GMP specification adds three additional
keys:

<dl>
  <dt>version</dt>
    <dd>
      The version of the ground motion packet 
      <i>(string; required)</i>.
    </dd>
 <dt>creation_time</dt>
    <dd>
     File creation timestamp in UTC in ISO 8601 *extended* format (i.e., with separators between the year, month, and day, and the hour, minutes, and seconds, and with a “T” between the date and time) ex “2022-01-16T14:12:32.470Z” 
      <i>(string; required)</i>.
    </dd>
  <dt>event</dt>
    <dd> 
      An optional dictionary containing earthquake properties for the
      earthquake associatd with the metrics given in this file 
      <i>(dictionary; optional).</i>
    </dd>
  <dt>provenance</dt>
    <dd>
      A SEIS-PROV-compliant provenance document <i>(dictionary; required)</i>. 
      The contents of this dictionary will be discussed in more detail later, 
      but the full specification is given 
      <a href="http://seismicdata.github.io/SEIS-PROV/">here</a>.
    </dd>
</dl>

Note that in this document, we will list the GMP elements as above, indicating
the element type and whether or not it is required in parentheses. The 
following example illustrates these top-level additions to the GeoJSON format. 

```json
{
  "type": "FeatureCollection",
  "event": {
    ...
  },
  "features": [
    ...
  ],
  "version": "0.1dev",
  "provenance": {
    ...
  }
}
```
