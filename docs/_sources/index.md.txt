---
hide-toc: true
---

## Earthquake Ground Motion Data Packet 

Here we present a specification for a [GeoJSON](https://geojson.org/) format 
for unassociated and event-associated ground motion metrics—that is, quantities
derived from ground motion records (e.g., accelerograms, velocity recordings).
We refer to this specification as a Ground Motion Packet (GMP). Common example
metrics include peak ground acceleration (PGA), peak ground velocity (PGV), and
spectral acceleration (SA). This format is designed so that it can also include
metrics that are gaining popularity for many engineering use cases, such as
significant duration, Arias intensity, and inelastic response spectra. This
format should be able to be used by any application that uses ground motion
metrics including, but not limited to, ShakeMap. The GMP format is not meant to
describe station metadata or site installation. The purpose of the metadata
included in the GMP format is to provide high-level information regarding the
suitability of the data for common engineering/seismological applications.

Note that this ground motion packet is for ground motion metrics and not the
waveforms themselves. Some metrics are associated with a single waveform, and 
others are associated with a group a waveforms. We apply
[ObsPy](https://docs.obspy.org/)'s nomenclature of 
"[trace](https://docs.obspy.org/packages/autogen/obspy.core.trace.Trace.html)" 
to refer to a single cotinuous time series, and 
"[stream](https://docs.obspy.org/packages/autogen/obspy.core.stream.Stream.html)" 
to refer to a group of traces.

```{attention}
Although the use of the terms "trace" and "stream" is convenient for use in organizing
waveform metrics, there is the potential for confusion since we are referring to the
trace or streams from which the metrics are derived, and the waveforms themselves are
not stored in the format presented here. 
```



```{toctree}
:hidden:

geojson
terms
specification/index
examples
cli
demo
pydantic_demo
dev
```