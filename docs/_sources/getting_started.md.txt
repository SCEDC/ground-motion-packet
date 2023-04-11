# Getting Started
This is a python package that can be imported and the functions can be called directly in new scripts, jupyter
notebooks, or interactive python sessions. Examples using different aspects of the GMP format can be foun in the
[Pydantic Demo](pydantic_demo) section.

## Installation

The basic dependencies are `pip` and `git`.

The main python dependency  for the `validate` and `scan` modules is the 
[SEIS-PROV validator](http://seismicdata.github.io/SEIS-PROV/validation.html#official-validator). 
To install:
```shell
git clone https://github.com/SeismicData/SEIS-PROV.git
cd SEIS-PROV/validator
pip install -e .
```

We also need the "schema" package:

```
pip install schema
```

Then, to install this package:
```
git clone https://github.com/SCEDC/ground-motion-packet.git
cd ground-motion-packet
pip install -e .
```

For developers or other interested users, there are optional dependencies for development (`dev`), running tests (`test`), making documentation (`doc`), and building distributions (`build`), that can instead be installed using:
```
pip install -e .[dev,test,doc,build]
```

Alternatively, you can install a pre-built wheel distribution directly from PyPi:
```
pip install gmpacket
```
