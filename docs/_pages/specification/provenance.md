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


Provenance 
==========

The provenance document is meant to inform the user about the provider, source, 
distributor, and processing of the data in this file. The provenance should 
meet the requirements of 
<a href="http://seismicdata.github.io/SEIS-PROV/index.html">SEIS-PROV</a>. 

```json
{
  "type": "FeatureCollection",
  "provenance": {
    ...
  },
  "features": [
    ...
  ]
}
```

The SEIS-PROV standard allows for a wide variety of information. SEIS-PROV 
categorizes entries into three main categories: "agents", "entities", and 
"activities". "Agents" entries can be either "software", "person", or 
"organization" agents.

The GMP format requires at least two entries:
  1. A "person" agent or an "organization" agent.
  2. A "software" agent.

The provenance JSON document is a dictionary with the following keys:
<dl>
  <dt>prefix</dt>
    <dd>A dictionary with a key "seis_prov" that defines the namespace.</dd>
  <dt>agent</dt>
    <dd>A dictionary for agent provenance information. </dd>
</dl>

```json
{
    ...
    "provenance": {
    	  "prefix": {
            "seis_prov": "http://seisprov.org/seis_prov/0.1/#"
        },
        "agent": {...}
    }
}
```

For "person" and "organization" agents, we define and require a specific 
attribute for the GMP format:
<dl>
  <dt>role</dt>
    <dd>Possible values are "data provider", "data processor", and "data 
    distributor".</dd>
</dl>

An example software agent is:
```json
{
    ...
    "provenance": {
    	...
        "agent": {
            "seis_prov:sp000_sa_0000000": {
                "prov:label": "gmprocess",
                "prov:type": {
                    "$": "prov:SoftwareAgent",
                    "type": "prov:QUALIFIED_NAME"
                },
                "seis_prov:software_name": "gmprocess",
                "seis_prov:software_version": "1.1",
                "seis_prov:website": {
                    "$": "http://dx.doi.org/10.5066/P9ANQXN3",
                    "type": "xsd:anyURI"
                }
            }
        }
    }
}
```

Note that the keys in the "agent" dictionary are the SEIS-PROV IDs for each 
provenance record, and must be unique. See the SEIS-PROV documentation for 
additional details. 

An example with an organization (the data distributor) and a person agents 
(the data processor) is:

```json
{
    ...
    "provenance": {
    	...
        "agent": {
            "seis_prov:sp000_pp_0000000": {
                "prov:label": "Mr. Processor",
                "prov:type": {
                    "$": "prov:Person",
                    "type": "prov:QUALIFIED_NAME"
                },
                "seis_prov:name": "Mr. Processor",
                "seis_prov:email": "mrprocessor@processing.org",
                "seis_prov:role": "data processor"
            },
            "seis_prov:sp000_og_0000000": {
                "prov:label": "IRIS DMC",
                "prov:type": {
                    "$": "prov:Organization",
                    "type": "prov:QUALIFIED_NAME"
                },
                "seis_prov:name": "IRIS DMC",
                "seis_prov:role": "data distributor",
                "seis_prov:website": {
                    "$": "https://www.iris.edu/",
                    "type": "xsd:anyURI"
                }
            }
        }
    }
}
```

An example with two organization agents (the data distributor and the data 
provider) is:

```json
{
    ...
    "provenance": {
    	...
        "agent": {
            "seis_prov:sp000_og_0000000": {
                "prov:label": "Mr. Processor",
                "prov:type": {
                    "$": "prov:Organization",
                    "type": "prov:QUALIFIED_NAME"
                },
                "seis_prov:name": "NCEDC",
                "seis_prov:website": {
                    "$": "https://ncedc.org/",
                    "type": "xsd:anyURI"
                },
                "seis_prov:role": "data provider"
            },
            "seis_prov:sp000_og_0000001": {
                "prov:label": "IRIS DMC",
                "prov:type": {
                    "$": "prov:Organization",
                    "type": "prov:QUALIFIED_NAME"
                },
                "seis_prov:name": "IRIS DMC",
                "seis_prov:role": "data distributor",
                "seis_prov:website": {
                    "$": "https://www.iris.edu/",
                    "type": "xsd:anyURI"
                }
            }
        }
    }
}
```
