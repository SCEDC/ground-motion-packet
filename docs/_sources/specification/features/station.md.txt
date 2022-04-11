## Stations

The GeoJSON features represent seismic stations in the GMP specification. 
Station metadata is included in the GeoJSON feature "properties" dictionary. 
Requited properties include:

**network_code**
:  The [FSDN](https://www.fdsn.org/networks/) network code <i>(string; required)</i>.

**station_code**
:  FDSN station code <i>(string; required)</i>.

**name**
:  Station name <i>(string; optional)</i>.

**streams**
:  A list of dictionaries, one for each stream at this station. 
    <i>(list; required)</i>.


```{note} "depth" in the station geometry coordinates array is defined as 
meters positive from the WGS84 datum. This conforms with GEOJSON
standard, but defiates from metadata convention.
```

Example:

```{code-block} json
---
force: true
---
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

