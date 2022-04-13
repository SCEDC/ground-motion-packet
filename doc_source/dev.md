## Developer Notes

We welcome comments and contributions through github issues.

### Documentation

Never edit the contents of the `docs` directory, only edit files in the `doc_source`
directory.

To build this documentation, it is convenient to create a conda virtual environment
with [mamba](https://github.com/mamba-org/mamba) (note that mamba can be installed 
with [conda](https://docs.conda.io/en/latest/)).

```
cd doc_source
mamba create -n gmpdocs python=3.9 --file requirements.txt
conda activate gmpdocs
```

Then install the python packages as described  in the 
[Command Line Tools](cli) section. For the demo, we'll also need

```
pip install ipyleaflet
jupyter nbextension enable --py widgetsnbextension
```

```
./makedocs.sh
```

The above script builds the docs html in the `docs` subdirectory. It can be previewed
locally by opening `docs/index.html` in a browser.
