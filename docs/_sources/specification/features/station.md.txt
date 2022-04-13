## Stations

The GeoJSON features represent seismic stations in the GMP specification. 
Station metadata is included in the GeoJSON feature "properties" dictionary. 
Requited properties include:

**type**
:  Must be "Feature" *(string; required)*.

**geometry**
:  A dictionary with the following keys *(dictionary; required)*.

   **type**
   :  Must be "Point" *(string; required)*.

   **coordinates**
   :  List of coordinates as floats *(list; required)*.

**properties**
:  A dictionary to store station-level metadata that contains the following 
   keys *(dictionary; required)*:

   **network_code**
   :  The [FSDN](https://www.fdsn.org/networks/) network code *(string; required)*.

   **station_code**
   :  FDSN station code *(string; required)*.

   **name**
   :  Station name *(string; optional)*.

   **streams**
   :  A list of dictionaries, one for each stream at this station. 
      *(list; required)*.

   **structure_reference_orientation**
   :  Reference for the structural coordinate system with respect to geographic north. 
      Equivalent to COSMOS integer 21 *(int; optional)*


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

