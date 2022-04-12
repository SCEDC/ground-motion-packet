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
# Demo

Be sure to install the python packages as described 
in the [Command Line Tools](cli) section.

Also, for this demo specifically, also install ipyleaflet with
```shell
pip install ipyleaflet
jupyter nbextension enable --py widgetsnbextension
```

The following tutorial can be run in an ipython notebook or in 
an ipython shell.

We will start with the necessary imports 

```{code-cell} ipython3
import os
import json
import requests
import pkg_resources

from ipyleaflet import Map, GeoJSON
from gmpacket.scan import scan_gmp
```

Now we will read in the example data that is in the data directory
of the gmpacket package

```{code-cell} ipython3
datapath = os.path.join('data', 'examples', 'sps-100-200-example.json') # 
data_file = pkg_resources.resource_filename('gmpacket', datapath)
with open(data_file, 'r') as f:
    data = json.load(f)
geo_json = GeoJSON(data=data)
```

There is only one feature, so we will grab it to set the center of the map

```{code-cell} ipython3
lon, lat, depth = geo_json.data['features'][0]['geometry']['coordinates']
m = Map(center=(lat, lon), zoom=7)
m.add_layer(geo_json)
m
```

Now we can use the `scan_gmp` function to print a summary of the example data

```{code-cell} ipython3
scan_gmp(data_file, print_what='summary')
```

We can also change the `print_what` argument to also include the metrics

```{code-cell} ipython3
scan_gmp(data_file, print_what='all')
```

