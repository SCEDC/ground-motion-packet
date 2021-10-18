---
layout: page
title: Streams and Traces
nav_order: 3
parent: Features
grand_parent: Specification
has_toc: false
---

## Streams and Traces

For the purposes of the GMP format, we require that the traces be grouped into 
streams for which their corresponding properties (i.e., metadata) are 
consistent. Since a station may include traces from different locations or with 
different sample rates, a single station feature may contain multiple streams. 
The GMP format requires a "streams" key for each station dictionary. The 
streams key gives a list of dictionaries, and each dictionary represents a 
unique stream at that station.

Each stream dictionary contains the following keys:

<dl>
  <dt>properties</dt>
    <dd>an element to store stream-level metadata that contains the following 
    keys <i>(dictionary; required)</i>:
    <dl>
      <dt>band_code</dt>
        <dd>
          The SEED band
          <a href="https://ds.iris.edu/ds/nodes/dmc/data/formats/seed-channel-naming/">code</a> 
          <i>(string; required)</i>.
        </dd>
      <dt>instrument_code</dt>
        <dd>
          The SEED instrument
          <a href="https://ds.iris.edu/ds/nodes/dmc/data/formats/seed-channel-naming/">code</a> 
          <i>(string; required)</i>. </dd>
      <dt>samples_per_second</dt>
        <dd>
          The number of samples per second of the time series (Hz) 
          <i>(float; required)</i>.
        </dd>
      <dt>stream_housing</dt>
        <dd> 
          A dictionary with the following keys <i>(dictionary; required)</i>.:
        <dl>
          <dt>cosmos_code</dt>
            <dd>
              The COSMOS station type
              <a href="https://www.strongmotioncenter.org/vdc/tables/stationtype.table">code</a> 
              <i>(integer; required)</i>.
            </dd>
          <dt>description</dt>
            <dd>
              The description associated with the cosmos_code 
              <i>(string; required)</i>.
            </dd>
          <dt>stream_depth</dt>
            <dd>
              Depth (in m) of the stream relative to the ground surface 
              <i>(float; required)</i>.
            </dd>
        </dl>
        </dd>
    </dl>
    </dd>
  <dt>traces</dt>
    <dd>
      A list of dictionaris in which each list element corresponds to a 
      different trace <i>(list; required)</i>.
    </dd>
</dl>

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

```json
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

<dl>
  <dt>properties</dt>
    <dd>A dictionary with the following keys <i>(dictionary, required)</i>:
    <dl>
      <dt>channel_code</dt>
        <dd>
          <a href="https://ds.iris.edu/ds/nodes/dmc/data/formats/seed-channel-naming/">SEED</a> 
          channel code <i>(string, required)</i>.
        </dd>
      <dt>location_code</dt>
        <dd>
          <a href="https://ds.iris.edu/ds/support/faq/54/what-is-a-seed-location-identifier-or-location-code/">SEED</a> 
          location code <i>(string, required)</i>.
        </dd>
      <dt>as_recorded</dt>
        <dd>
          True if trace is a record from a data logger, False if trace is a 
          function of multiple traces <i>(bool; required)</i>.
        </dd>
      <dt>azimuth</dt>
        <dd>
          Degrees clockwise from north of the trace orientation <i>(float; required)</i>.
        </dd>
      <dt>dip</dt>
        <dd>
          Degrees from horizontal of trace orientation <i>(float; required)</i>.
        </dd>
      <dt>start_time</dt>
        <dd>
          Trace start time; UTC ISO 8601 time format <i>(string; required).</i>
        </dd>
      <dt>end_time</dt>
        <dd>
          Trace end time; UTC ISO 8601 time format <i>(string; required).</i>
        </dd>
    </dl>
    </dd>
  <dt>metrics</dt>
    <dd>A list of dictionaries <i>(dictionary; required)</i>.</dd>
</dl>

An example trace dictionary structure is illustrated below.

```json
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
