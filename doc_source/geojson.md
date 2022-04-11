# GeoJSON Overview


The GMP ground motion format is an extension of the GeoJSON "FeatureCollection"
format for points. For example, a simple collection of two points in GeoJSON
would look like this:

```{code-block} json
---
force: true
---
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "name": "Example Point 1"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [-117.3, 35.5, 10.0]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "name": "Example Point 2"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [-120.1, 37.2, 2.0]
      }
    }
  ]
}
```

There are a few key aspects of the JSON format that users should be familiar
with:

  - Dictionaries consist of key-value pairs and begin with an open brace `{` 
    and end with a closed brace `}`. In the example above, the base structure 
    of the format is a dictionary, with keys of "type" and "features". Note 
    that the order of the entries in a dictionary does not matter and is
    ignored. 
  - A list is an array of values separated by commas and begins with an open 
    bracket `[` and ends with a closed bracket `]`. The values can be anything,
    such as a number, string, another list, or a dictionary. The "features" key
    in the base dictionary is itself a list of dictionaries, each of which
    corresponds to one point.

