---
layout: page
title: Stations
nav_order: 2
parent: Features
grand_parent: Specification
has_toc: false
---

## Stations

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

<i><b>NOTE</b>: "depth" in the station geometry coordinates array is defined as 
meters positive downward from the surface. This conforms with seismic metadata 
convention, but deviates from GeoJSON.</i>

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