---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: '0.8'
    jupytext_version: '1.4.1'
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---
# Pydantic Demo

We will start with the necessary imports 

```{code-cell} ipython3
from datetime import datetime, timedelta
from gmpacket.provenance import SoftwareAgent, PersonAgent, OrganizationAgent, Website, Provenance
from gmpacket.feature import (
    Feature,
    FeatureGeometry,
    FeatureProperties,
    Metric,
    MetricDimensions,
    MetricProperties,
    Stream,
    StreamHousing,
    StreamProperties,
    Trace,
    TraceProperties,
)
from gmpacket.packet import Event, GroundMotionPacket
```

## Dealing with Provenance

```{code-cell} ipython3
person = PersonAgent.from_params("Alex Processor", 
                                 "aprocessor@datagenerator.org", 
                                 "Data Processor")
print(person)

website = Website(url="https://code.usgs.gov/ghsc/esi/groundmotion-processing/#introduction")
software = SoftwareAgent.from_params("gmprocess", "1.2.0", website)
print(software)

org_website = Website(url="https://www.datagenerator.org")
organization = OrganizationAgent.from_params("Data Generator", "Data Provider", org_website)
print(organization)

# the names of the keys are not important, but the values must be valid Person,Software, or 
# OrganizationAgent objects.
agents = {"person": person, "software": software, "organization":organization}
provenance = Provenance(agent=agents)
print(provenance)
```

## Creating Simple Metrics

```{code-cell} ipython3
pga_props = MetricProperties(description="Peak Ground Accleration",
                           name="PGA",
                           units= "g",
                           provenance_ids= provenance.getAgents())
print(pga_props)

# for scalar values like PGA, MetricDimensions are not necessary
pga_metric = Metric(properties=pga_props, values=1.5)
print(pga_metric)
```

## Creating Complex Metrics

```{code-cell} ipython3
sa_props = MetricProperties(description="Spectral Accleration",
                             name="SA",
                             units= "g",
                             provenance_ids= provenance.getAgents())
print(sa_props)

sa_dims = MetricDimensions(number=2,
                           names=["critical damping", "period"],
                           units=["%","s"],
                           axis_values=[[5.0],[0.3, 1.0, 3.0]])
print(sa_dims)

sa_metric = Metric(properties=sa_props, dimensions=sa_dims, values=[[1.2, 1.4, 1.6]])
print(sa_metric)
```

## Creating Traces

```{code-cell} ipython3
end_time = datetime.utcnow()
start_time = end_time - timedelta(seconds=30)
sa_trace_props = TraceProperties(channel_code="HNE", 
                                 location_code="10", 
                                 as_recorded=True, 
                                 azimuth=90, 
                                 dip=0,
                                 start_time=start_time, 
                                 end_time=end_time)
print(sa_trace_props)

metrics = [pga_metric, sa_metric]
hne_trace = Trace(properties=sa_trace_props, metrics=metrics)
print(hne_trace)
```

## Creating a Stream

```{code-cell} ipython3
stream_housing = StreamHousing(cosmos_code=10, description="A building", stream_depth=0.0)
print(stream_housing)

stream_props = StreamProperties(band_code="H", 
                                instrument_code="N", 
                                samples_per_second=100.0, 
                                stream_housing=stream_housing)
print(stream_props)

stream = Stream(properties=stream_props, traces=[hne_trace])
print(stream)
```

## Creating a Feature (station)

```{code-cell} ipython3
feature_geom = FeatureGeometry(coordinates=[-124.1, 32.0, 1.1])
print(feature_geom)

feature_props = FeatureProperties(network_code="NC", 
                                  station_code="ABCD", 
                                  name="A nice place for picnics", 
                                  streams=[stream])
print(feature_props)

feature = Feature(geometry=feature_geom, properties=feature_props)
print(feature)
```

## Creating a Ground Motion Packet

```{code-cell} ipython3
event = Event.from_params("us2023abcd", datetime.utcnow(), 7.3, 32.1, -120.0, 35.3)
print(event)

gm_packet = GroundMotionPacket(version="0.1dev", 
                               event=event, 
                               provenance=provenance, 
                               features=[feature]
                              )
print(gm_packet)
```

## Exporting GroundMotion Packets

```{code-cell} ipython3
print(gm_packet.as_json())

df = gm_packet.to_dataframe()
df
```


