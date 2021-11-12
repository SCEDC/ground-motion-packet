Navigation
----------

 - [About](index.md)
 - [GeoJSON Overview](geojson.md)
 - [Terminology](terms.md)
 - Specification
   - [Base Dictionary](specification/base.md)
   - [Event Dictionary](specification/event.md)
   - [Provenance](specification/provenance.md)
   - [Guidelines for Data Providers on Incomplete Data](guidelines-provider.md)
   - Features
     - [Stations](specification/features/station.md)
     - [Streams and Traces](specification/features/streams_traces.md)
     - [Metrics Dictionary](specification/features/metrics_dict.md)

Guidelines for Data Providers on Incomplete Data  (Work in Progress)
=====

It is a common scenario where the data provider may only know the instrument
response for seismic channels but may not be given information on sensor
installation (housing, emplacement depth).  How much detail is known to the 
provider will affect how the stream dictionary is organized. 

**If the provider has sufficient knowledge of the site installation, a stream should contain traces from a single sensor at a single sample rate.**

**If the provider does not have enough information to determine if multiple time series with the same sample rate came from one or more sensors they should be put into the same stream. The data provider should the set the values to the appropriate keys in the "stream_housing" dictionary to "unknown" to mark this ambiguity.**

Example
====
Consider two time series with the SEED channel codes:
```
net code: CI
station code: PASC
channel code: HNZ
location code: 00
```
and 
```
net code: CI
station code: PASC
channel code: HNZ
location code: 10
```

If both channels have a sample rate 100 sps and nothing else is known about the site installation,
then both traces should be put into one stream.

```
...
                "streams": [
                    {
                        "properties": {
                            "band_code": "H",
                            "instrument_code": "N",
                            "samples_per_second": 100.0,
                            "stream_housing": {
                                "cosmos_code": "unknown",
                                description": "",
                                "stream_depth": "unknown"
                            }
                        },
                        "traces": [
                            {
                                "properties": {
                                    "channel_code": "HNZ",
                                    "location_code": "00",
                                    "as_recorded": true,
                                    "azimuth": 0,
                                    "dip": -90.0,
                                    "start_time":"2019-07-06T03:19:53Z",
                                    "end_time":"2019-07-06T04:59:53Z"
                                },
                                ...   
                                "properties": {
                                    "channel_code": "HNZ",
                                    "location_code": "10",
                                    "as_recorded": true,
                                    "azimuth": 0,
                                    "dip": -90.0,
                                    "start_time":"2019-07-06T03:19:53Z",
                                    "end_time":"2019-07-06T04:59:53Z"
                                },
                                ...
                               }
                             ]
...
```
On the other hand, if the provider knew this was a borehole station, with one channel belonging to the surface sensor at 0.3 m depth,
and the other channel belonging to the borehole sensor at 20.0 m depth, then these traces should belong to separate streams.

```
...
                "streams": [
                    {
                        "properties": {
                            "band_code": "H",
                            "instrument_code": "N",
                            "samples_per_second": 100.0,
                            "stream_housing": {
                                "cosmos_code": "6",
                                "description": "Free field",
                                "stream_depth": "0.3"
                            }
                        },
                        "traces": [
                            {
                                "properties": {
                                    "channel_code": "HNZ",
                                    "location_code": "00",
                                    "as_recorded": true,
                                    "azimuth": 0,
                                    "dip": -90.0,
                                    "start_time":"2019-07-06T03:19:53Z",
                                    "end_time":"2019-07-06T04:59:53Z"
                                },
                                ...   
                              }
                              ]
                         },
                        "properties": {
                            "band_code": "H",
                            "instrument_code": "N",
                            "samples_per_second": 100.0,
                            "stream_housing": {
                                "cosmos_code": "50",
                                "description": "Borehole",
                                "stream_depth": "20.0"
                            }
                        },
                        "traces": [                         
                                {
                                    "channel_code": "HNZ",
                                    "location_code": "10",
                                    "as_recorded": true,
                                    "azimuth": 0,
                                    "dip": -90.0,
                                    "start_time":"2019-07-06T03:19:53Z",
                                    "end_time":"2019-07-06T04:59:53Z"
                                },   
...
```

The following table gives guidance on how a provider should write a GMP file depending on how much information is known about site installation.

Table: Stream/Trace Organization vs Site Installation Type (Version 2)
=====

Sensor Type | Is sample rate uniform? | Is housing known? | # surface sensors | # borehole sensors | Number of Streams | Number of Traces | Comments
--- | --- | --- | --- | --- | --- | --- | ---
triaxial | Yes | Yes | 1 | 0 | 1 | 3 | 3 traces because it is a triaxial sensor; in the "stream_housing" dictionary, the "cosmos_code" and "stream_depth" are known.
triaxial | Yes | No | 1 | 0 | 1 | 3 | 3 traces because it is a triaxial sensor; in the "stream_housing" dictionary, mark "cosmos_code" and "stream_depth" as "unknown"
triaxial | No | Yes | 1 | 0 | 2+ | 3,3... | N 3-trace streams; stream is grouped by sample rate (e.g., 100 sps and 200 sps); housing is indicated in stream properties.
triaxial | No | No | 1 | 0 | 2+ | 3,3... | N 3-trace streams; stream is grouped by sample rate (e.g., 100 sps and 200 sps); housing is unknown is stream properties.
triaxial | Yes | Yes | 1 | 1 | 2 | 3,3 | The depth of the sensors is given in "stream_depth" under "stream_housing" for each stream; the "cosmos_code" is also given.
triaxial | Yes | No | 1 | 1 | 1 | 6 | In the "stream_housing" dictionary, mark "cosmos_code" and "stream_depth" as "unknown"; the sensors are differentiated by location code
mixed | Yes | Yes | 2 | 1 | 3 | 1,3,3 | First stream is a vertical surface sensor, second is a surface triaxial, third is a borehole triaxial with known depth(i.e. known housing).
mixed | Yes | No | 2 | 1 | 2 | 1,6 | First stream is a vertical surface sensor, second is a pair of triaxial sensors with distinct location codes but unknown housing.



