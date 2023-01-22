# stdlib imports
import json
import pathlib

# third party imports
from deepdiff import DeepDiff

# local imports
from gmpacket.packet import Event, GroundMotionPacket
from test_utils import get_jdict


def test_event():
    jdict = get_jdict()
    data = jdict["event"]
    event = Event(**data)
    assert event.dict(by_alias=True) == data

    event = Event.from_parameters(
        "ci38457511", "2019-07-06T03:19:53Z", 7.1, -117.599, 35.77, -8.0
    )
    cmp_dict = {
        "type": "Feature",
        "properties": {
            "id": "ci38457511",
            "time": "2019-07-06T03:19:53Z",
            "magnitude": 7.1,
        },
        "geometry": {"type": "Point", "coordinates": [35.77, -117.599, -8000.0]},
    }
    assert event.dict(by_alias=True) == cmp_dict


def test_packet():
    data = get_jdict()
    packet = GroundMotionPacket(**data)
    pdict = json.loads(packet.json(by_alias=True))
    cmp_dict = json.loads(json.dumps(data))
    assert DeepDiff(cmp_dict, pdict) == {}

    jsonfile = (
        pathlib.Path(__file__).parent
        / ".."
        / ".."
        / "gmpacket"
        / "data"
        / "examples"
        / "multichannel_example.json"
    )
    columns = [
        "id",
        "time",
        "magnitude",
        "event_longitude",
        "event_latitude",
        "event_depth",
        "network",
        "station",
        "station_name",
        "station_longitude",
        "station_latitude",
        "station_elevation",
        "channel",
        "location",
        "PGA(g)",
        "PGV(cm/s)",
        "SA(g)_critical_damping_5.0%_period_0.3s",
        "SA(g)_critical_damping_5.0%_period_1.0s",
        "SA(g)_critical_damping_5.0%_period_3.0s",
    ]
    with open(jsonfile, "rt") as f:
        data = json.load(f)
        packet = GroundMotionPacket(**data)
        dataframe = packet.to_dataframe()
        assert dataframe.columns.to_list() == columns


def test_loader():
    datadir = (
        pathlib.Path(__file__).parent / ".." / ".." / "gmpacket" / "data" / "examples"
    )
    jsonfiles = datadir.glob("*.json")
    for jsonfile in jsonfiles:
        with open(jsonfile, "rt") as f:
            data = json.load(f)
            packet = GroundMotionPacket(**data)
            print(f"Successfully read in {jsonfile}. to {packet.version}")


if __name__ == "__main__":
    test_event()
    test_packet()
    test_loader()
