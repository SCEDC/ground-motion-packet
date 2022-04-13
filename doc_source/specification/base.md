## Base Dictionary

For the base GeoJSON dictionary, the GMP specification adds four additional
keys:

**version**
:  The version of the ground motion packet *(string; required)*.

**creation_time**
:  File creation timestamp in UTC in ISO 8601 *extended* format 
   (i.e., with separators between the year, month, and day, and the hour, 
   minutes, and seconds, and with a "T" between the date and time). 
   Example: "2022-01-16T14:12:32.470Z" *(string; required)*.

**event**
:   An optional dictionary containing earthquake properties for the
    earthquake associatd with the metrics given in this file 
    *(dictionary; optional).*

**provenance**
:   A SEIS-PROV-compliant provenance document *(dictionary; required)*. 
    The contents of this dictionary will be discussed in more detail later, 
    but the full specification is given 
    [here](http://seismicdata.github.io/SEIS-PROV/).


Note that in this document, we will list the GMP elements as above, indicating
the element type and whether or not it is required in parentheses. The 
following example illustrates these top-level additions to the GeoJSON format. 

```{code-block} json
---
force: true
---
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

