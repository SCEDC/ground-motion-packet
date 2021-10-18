---
layout: page
title: About
nav_order: 1
---

## About

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
