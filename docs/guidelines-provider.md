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

Table: Stream/Trace Organization vs Site Installation Type 
=====

Site Type | Is stream_housing and/or depth known to data provider?
| Number of stream Elements; Number of traces per stream (“as_recorded” = True) 
| Comments 
 --- | --- | --- | ---
  1 triaxial sensor digitized at 100 sps
| Yes
| streams []: 1
| traces{} : 3
