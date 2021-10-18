---
layout: page
title: Terminology
nav_order: 2
---

## Terminology

<dl>
  <dt>JSON</dt>
    <dd>A standard file format, which stands for JavaScript Object Notation. 
    This standard is appealing because it is human readable, allows for 
    flexible data structures, and is supported by many programming languages.
</dd>
  <dt>GeoJSON</dt>
    <dd>A JSON specification that is designed for spatial data. This is a 
    format that can be read by most GIS software and is supported in many 
    programming languages. </dd>
  <dt>Feature</dt>
    <dd>GeoJSON term for specifying a spatial object (point, line, or polygon).
    Here all of our features will be points (denoting 
    latitude/longitude/elevation of a station and/or an event).</dd>
  <dt>Intensity Measure/Metric</dt>
    <dd>A parametric representation of a ground motion record. Examples include
    PGA or PGV, spectral acceleration, Arias Intensity, significant duration, 
    cumulative absolute velocity, and inelastic response spectra.</dd>
  <dt>Trace</dt>
    <dd>A reference to the time series used to compute the <b>Intensity 
    Measure/Metric</b>. This might be from a single seismic data channel (e.g., 
    HNE, HNN) or a derived combination of seismic channels such as the rotd50 
    or transverse time series. This is often referred to as “component” in 
    other contexts, especially when the station has only one sensor sampled at 
    one sample rate. We use the term “trace” to avoid confusion with the use of 
    the term “component” in the instrumentation context and therefore avoid 
    assumptions about sample rate and orientation. Note that these terms are 
    important for defining the hierarchy of the data structure, but this format 
    does not report the time series array itself.</dd>
  <dt>Stream</dt>
    <dd>A collection of traces. The terms “trace” and “stream” follow the
    terminology adopted by ObsPy.</dd>
  <dt>Provenance</dt>
    <dd>A <a href="http://seismicdata.github.io/SEIS-PROV/">SEIS-PROV</a>-compliant 
    provenance document.</dd>
</dl>