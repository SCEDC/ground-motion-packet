---
layout: page
title: Event
nav_order: 3
parent: Specification
has_toc: false
---

## Event

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
          Event origin time UTC ISO 8601 time format <i>(string; required)</i>.
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

<i><b>NOTE</b>: "depth" in the events geometry coordinates array is defined as 
kilometers positive downward. This conforms with seismic metadata convention, 
but deviates from GeoJSON. Note, however, that "downward from what?" is a 
legitimate question. It may be the surface or it may be the WGS 84 ellipsoid or 
some other reference. This standard makes no attempt to define a reference. 
Users concerned with such matters should consult an authoritative reference for 
earthquake origin information.</i>

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
