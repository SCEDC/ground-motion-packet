import json
import pathlib


def get_jdict():
    datadir = pathlib.Path(__file__).parent / "data"
    jsonfile = datadir / "full_packet.json"
    with open(jsonfile, "rt") as f:
        jdict = json.load(f)
    return jdict
