Navigation
----------

 - [About](../index.md)
 - [GeoJSON Overview](../geojson.md)
 - [Terminology](../terms.md)
 - Specification
   - [Base Dictionary](base.md)
   - [Event Dictionary](event.md)
   - [Provenance](provenance.md)
   - [Guidelines for Data Providers on Incomplete Data](guidelines-provider.md)
   - Features
     - [Stations](features/station.md)
     - [Streams and Traces](features/streams_traces.md)
     - [Metrics Dictionary](features/metrics_dict.md)

Guidelines for Data Providers on Incomplete Data
=====

It is a common scenario where the data provider may only know the instrument
response for seismic channels but may not be given information on sensor
installation (housing, emplacement depth).  How much detail is known to the 
provider will affect how the stream dictionary is organized. **If the provider 
does not have enough information to separate 2 time series they should be put into the same stream.**

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

Table: Stream/Trace Organization vs Site Installation Type 
=====

Site Installation Type | Is stream_housing and/or depth known to data provider? | Number of stream Elements; Number of traces per stream (“as_recorded” = True) | Comments 
 --- | --- | --- | ---
 1 triaxial sensor digitized at 100 sps | Yes | streams []: 1 traces{}: 3
 1 triaxial sensor digitized at 100 sps | No | streams []: 1 traces{}: 3
 1 triaxial sensor digitized at 100 sps and 200 sps | Yes | streams []: 2 traces{}: 3 under each stream | stream is grouped by sample rate.
 1 triaxial sensor digitized at 100 sps and 200 sps | No | streams []: 2 traces{}: 3 under each stream | stream is grouped by sample rate
 2 triaxial sensors digitized at 100 sps in a borehole. Borehole sensor at 100 m | Yes | streams []: 2 traces{}: 3 under each stream | 
 2 triaxial sensors digitized at 100 sps in a borehole. Borehole sensor at 100 m | No | streams []: 1 traces{} : 6 | mark “stream_housing” and “depth” as Unknown.
 3 sensors. 2 surface sensors, one vertical short period digitized at 100 sps, 1 triaxial strong motion at 100 sps. 1 triaxial borehole at 100 sps | Yes | streams []: 3 traces{}: short period vertical = 1, surface triaxial = 3, borehole triaxial = 3 | stream is also grouped by the band pass of the sensor (short period, broadband).  So the short period sensor traces should be in a different stream
3 sensors. 2 surface sensors, one vertical short period digitized at 100 sps, 1 triaxial strong motion at 100 sps. 1 triaxial borehole at 100 sps | No | streams []: 2 traces{}: short period vertical stream = 1, strong motion triaxial stream = 6 | Because the short period will have a different band code for its data channel, the data provider is able to put it in a separate stream element. 
2 triaxial sensors on surface, but in different parts of a building or dam. Both measuring at 100 sps. | Yes | streams []: 2 traces{}: 3 under each stream | Sometimes even if “stream_housing” is not known, but if the channels have distinct lat/lon from station, the data provider should then group the channels by the same lat/lon pair
2 triaxial sensors on surface, but in different parts of a building or dam. Both measuring at 100 sps. | No | streams []: 1 traces{} : 6 | mark “stream_housing” and “depth” as Unknown. 


