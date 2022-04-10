Navigation
----------

 - [About](../index.md)
 - [GeoJSON Overview](../geojson.md)
 - [Terminology](../terms.md)
 - Specification
   - [Base Dictionary](base.md)
   - [Event Dictionary](event.md)
   - [Provenance](provenance.md)
   - [Guidelines for Data Providers](guidelines-provider.md)
   - Features
     - [Stations](features/station.md)
     - [Streams and Traces](features/streams_traces.md)
     - [Metrics Dictionary](features/metrics_dict.md)

Guidelines for Data Providers
=====

It is a common scenario where the data provider may only know the instrument 
response for seismic channels but may not be given information on sensor 
installation (housing, emplacement depth). The GMP format is designed to allow 
a provider to send GMP data even if this information is not known. How much 
detail is known to the provider will affect how the stream dictionary is 
organized. Table 2 gives guidance on how a provider should write a GMP file 
depending on how much information is known about site installation.

 Site Type | Is stream_housing and/or depth known to data provider? 
| Number of stream Elements; Number of traces per stream (“as_recorded” = True) 
| Comments 
 --- | --- | --- | --- 
 1 triaxial sensor digitized at 100 sps 
| Yes 
| streams []: 1  
| traces{} : 3 

 1 triaxial sensor digitized at 100 sps 
| No
| streams []: 1
| traces{}: 3


1 triaxial sensor digitized at 100 sps and 200 sps | Yes | streams []: 2 traces {}: 3 under each stream | stream is grouped by sample rate.
1 triaxial sensor digitized at 100 sps and 200 sps | No | streams []: 2 traces{}: 3 under each stream | We expect the data provider to know the sample rate

2 triaxial sensors digitized at 100 sps in a borehole. Borehole sensor at 100 m | Yes | streams []: 2 traces{}: 3 under each stream | 

2 triaxial sensors digitized at 100 sps in a borehole. Borehole sensor at 100 m | No | streams []: 1 traces{} : 6 | mark “stream_housing” and “depth” as Unknown.


3 sensors. 2 surface sensors, one vertical short period digitized at 100 sps, 1 triaxial strong motion at 100 sps. 1 triaxial borehole at 100 sps | Yes | streams []: 3 traces{}: short period vertical = 1, surface triaxial = 3, borehole triaxial = 3 | stream is also grouped by the band pass of the sensor (short period, broadband).  So the short period sensor traces should be in a different stream
3 sensors. 2 surface sensors, one vertical short period digitized at 100 sps, 1 triaxial strong motion at 100 sps. 1 triaxial borehole at 100 sps | No | streams []: 2 traces{}: short period vertical stream = 1, strong motion triaxial stream = 6 | Because the short period will have a different band code for its data channel, the data provider is able to put it in a separate stream element.


2 triaxial sensors on surface, but in different parts of a building or dam. Both measuring at 100 sps.
Yes
streams []: 2
traces{}: 3 under each stream
Sometimes even if “stream_housing” is not known, but if the channels have distinct lat/lon from station, the data provider should then group the channels by the same lat/lon pair
No
streams []: 1 
traces{} : 6
mark “stream_housing” and “depth” as Unknown. 



