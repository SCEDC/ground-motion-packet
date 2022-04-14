## Command Line Tools

This respository contains some command line tools that are meant to assist in reading,
parsing, and validating the ground motion data packet format. This is a python package
that can be imported and the functions can be called directly in new scripts, jupyter
notebooks, or interactive python sessions. An example session is given in the 
[Demo](demo) section.

### Installation

The basic dependencies are `pip` and `git`.

The main python dependency is the 
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

### Usage

The installed program is called `gmpformat`:
```
$ gmpformat -h
usage: gmpformat [-h] {print,csv,validate} ...

This is a program for describing, validating, and converting Ground Motion Packet (GMP) formatted data.

optional arguments:
  -h, --help            show this help message and exit

subcommands:
  {print,csv,validate}
    print               Print GMP file contents.
    csv                 Convert GMP file contents to a CSV flatfile.
    validate            Validate a GMP file; will print encountered error messages.
```
