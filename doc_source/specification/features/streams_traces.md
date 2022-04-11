## Streams and Traces

For the purposes of the GMP format, we require that the traces be grouped into 
streams for which their corresponding properties (i.e., metadata) are 
consistent. Since a station may include traces from different locations or with 
different sample rates, a single station feature may contain multiple streams. 
The GMP format requires a "streams" key for each station dictionary. The 
streams key gives a list of dictionaries, and each dictionary represents a 
unique stream at that station.

Each stream dictionary contains the following keys:

**properties**
:  an element to store stream-level metadata that contains the following 
   keys <i>(dictionary; required)</i>:

   **band_code**
   :  The SEED band 
      [code](https://ds.iris.edu/ds/nodes/dmc/data/formats/seed-channel-naming/)
      <i>(string; required)</i>.

   **instrument_code**
   :  The SEED instrument 
      [code](https://ds.iris.edu/ds/nodes/dmc/data/formats/seed-channel-naming/) 
      <i>(string; required)</i>.

   **samples_per_second**
   :  The number of samples per second of the time series (Hz) 
      (float; required)</i>.

   **stream_housing**
   :  A dictionary with the following keys <i>(dictionary; required)</i>:

      **cosmos_code**
      :  The COSMOS station type
         [code](https://www.strongmotioncenter.org/vdc/tables/stationtype.table)
         <i>(integer; required)</i>.

      **description**
      :  The description associated with the cosmos_code 
         <i>(string; required)</i>.

      **stream_depth**
      :  Depth (in m) of the stream relative to the ground surface 
         <i>(float; required)</i>.

**traces**
:  A list of dictionaris in which each list element corresponds to a 
   different trace <i>(list; required)</i>.


It is important to note that since the "properties" element is a key within the
stream dictionary, all of these traces must share the specified metadata. 
Traces can be either “as recorded” or derived traces. "As recorded" traces are
the direct output of a data logger. 

Derived traces are a function of the "as recorded" traces. Examples of 
"as recorded" traces are `BHN.--` and `HNZ.01`. Examples of derived traces 
include: 
  - The "greater of two horizontal" traces, 
  - Transverse/radial traces, and 
  - "RotD50" (see Boore 2010 for the full definition of RotD50). 

An example stream dictionary structure is illustrated below.

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
                ...
                "streams": [
                    {
                        "properties": {
                            "band_code": "H",
                            "instrument_code": "N",
                            "samples_per_second": 100.0,
                            "stream_housing": {
                                "cosmos_code": 10,
                                "description": "Building",
                                "stream_depth": 0.0
                            }
                        },
                        "traces": [
                            {
                                ...
                            },
                            ...
                        ]
                    }
                ]
            }
        }
    ]
}
```

Each of the "traces" dictionaries must have the following
keys:

**properties**
:  A dictionary with the following keys <i>(dictionary, required)</i>:

   **channel_code:**
   :  [SEED](https://ds.iris.edu/ds/nodes/dmc/data/formats/seed-channel-naming/)
      channel code <i>(string, required)</i>.

   **location_code**
   :  [SEED](https://ds.iris.edu/ds/support/faq/54/what-is-a-seed-location-identifier-or-location-code/)
      location code <i>(string, required)</i>.

   **as_recorded**
   :  True if trace is a record from a data logger, False if trace is a 
      function of multiple traces <i>(bool; required)</i>.

   **azimuth**
   :  Degrees clockwise from north of the trace orientation 
      <i>(float; required)</i>.

   **dip**
   :  Degrees from horizontal of trace orientation <i>(float; required)</i>.

   **start_time**
   :  Trace start time; UTC ISO 8601 time format <i>(string; required).</i>

   **end_time**
   :  Trace end time; UTC ISO 8601 time format <i>(string; required).</i>

**metrics**
:  A list of dictionaries <i>(dictionary; required)</i>.


An example trace dictionary structure is illustrated below.

```{code-block} json
---
force: true
---
{
    ...
    "features": [
        {
            ...
            "properties": {
                ...
                "streams": [
                    {
                        ...
                        "traces": [
                            {
                                "properties": {
                                    "channel_code": "HNE",
                                    "location_code": "--",
                                    "as_recorded": true,
                                    "azimuth": 0,
                                    "dip": -90.0,
                                    "start_time": "2019-07-06T03:19:53Z",
                                    "end_time": "2019-07-06T04:59:53Z"
                                },
                                "metrics": [
                                    {
                                        ...
                                    },
                                    ...
                                ]
                            }
                        ]
                    }
                ]
            }
        }
    ]
}
```

