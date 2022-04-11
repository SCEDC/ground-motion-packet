## Command Line Tools

This respository contains some command line tools that are meant to assist in reading,
parsing, and validating the ground motion data packet format.

### Installation

The basic dependencies are pip and git. 
The primary python package that is necessary is the 
[SEIS-PROV validator](http://seismicdata.github.io/SEIS-PROV/validation.html#official-validator). 
To install:
```shell
git clone https://github.com/SeismicData/SEIS-PROV.git
cd SEIS-PROV/validator
pip install -e .
```

Then, to install this package:
```
git clone https://github.com/SCEDC/ground-motion-packet.git
cd ground-motion-packet
pip install -e .
```

### Usage

The installed program is called `gmpformat`:
```shell
$ gmpformat -h
usage: gmpformat [-h] {print,csv,validate} ...

This is a program for describing, validating, and converting Ground Motion
Packet (GMP) formatted data.

optional arguments:
  -h, --help            show this help message and exit

subcommands:
  {print,csv,validate}
    print               Print GMP file contents.
    csv                 Convert GMP file contents to a CSV flatfile.
    validate            Validate a GMP file.
```
