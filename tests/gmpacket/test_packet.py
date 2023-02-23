# stdlib imports
import json
import pathlib
import sys
from datetime import datetime, timedelta

# third party imports
from deepdiff import DeepDiff

# local imports
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
from gmpacket.provenance import (
    OrganizationAgent,
    PersonAgent,
    Provenance,
    SoftwareAgent,
    Website,
)
from test_utils import get_jdict


def test_event():
    jdict = get_jdict()
    data = jdict["event"]
    event = Event(**data)
    assert event.dict(by_alias=True) == data

    event = Event.from_params(
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
        "epicentral_distance_km",
        "component",
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


def dataframe_test(jsonfile=None, save_file=False):
    with open(jsonfile, "rt") as f:
        data = json.load(f)
        packet = GroundMotionPacket(**data)
        dataframe = packet.to_dataframe()

        if save_file:
            outfile = pathlib.Path.home() / pathlib.Path(jsonfile).with_suffix(".xlsx")
            print(f"Writing file {outfile}...")
            dataframe.to_excel(outfile, index=False)


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


def test_from_objects():
    person = PersonAgent.from_params(
        "Alex Processor", "aprocessor@datagenerator.org", "Data Processor"
    )
    website = Website(
        url="https://code.usgs.gov/ghsc/esi/groundmotion-processing/#introduction"
    )
    software = SoftwareAgent.from_params("gmprocess", "1.2.0", website)
    org_website = Website(url="https://www.datagenerator.org")
    organization = OrganizationAgent.from_params(
        "Data Generator", "Data Provider", org_website
    )
    agents = {"person": person, "software": software, "organization": organization}
    provenance = Provenance(agent=agents)
    pga_props = MetricProperties(
        description="Peak Ground Accleration",
        name="PGA",
        units="g",
        provenance_ids=provenance.getAgents(),
    )
    pga_metric = Metric(properties=pga_props, values=1.5)
    sa_props = MetricProperties(
        description="Spectral Acceleration",
        name="SA",
        units="g",
        provenance_ids=provenance.getAgents(),
    )
    sa_dims = MetricDimensions(
        number=2,
        names=["critical damping", "period"],
        units=["%", "s"],
        axis_values=[[5.0], [0.3, 1.0, 3.0]],
    )
    sa_metric = Metric(
        properties=sa_props,
        dimensions=sa_dims,
        values=[[1.23435678, 1.456789, 1.678901]],
    )
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(seconds=30)
    sa_trace_props = TraceProperties(
        channel_code="HNE",
        location_code="10",
        as_recorded=True,
        azimuth=90,
        dip=0,
        start_time=start_time,
        end_time=end_time,
    )
    metrics = [pga_metric, sa_metric]
    hne_trace = Trace(properties=sa_trace_props, metrics=metrics)
    stream_housing = StreamHousing(
        cosmos_code=10, description="A building", stream_depth=0.0
    )
    stream_props = StreamProperties(
        band_code="H",
        instrument_code="N",
        samples_per_second=100.0,
        stream_housing=stream_housing,
    )
    stream = Stream(properties=stream_props, traces=[hne_trace])
    feature_geom = FeatureGeometry(coordinates=[-124.1, 32.0, 1.1])
    feature_props = FeatureProperties(
        network_code="NC",
        station_code="ABCD",
        name="A nice place for picnics",
        streams=[stream],
    )
    feature = Feature(geometry=feature_geom, properties=feature_props)
    event = Event.from_params("us2023abcd", datetime.utcnow(), 7.3, 32.1, -120.0, 35.3)
    gm_packet = GroundMotionPacket(
        version="0.1dev", event=event, provenance=provenance, features=[feature]
    )
    feature = gm_packet.features[0]
    cmp_json = (
        '{"geometry": {"coordinates": [-124.1, 32, 1.1], "type": "Point"}, '
        '"properties": {"network_code": "NC", "station_code": "ABCD", "name": '
        '"A nice place for picnics", "streams": [{"properties": {"band_code": '
        '"H", "instrument_code": "N", "samples_per_second": 100, "stream_housing": '
        '{"cosmos_code": 10, "description": "A building", "stream_depth": 0, '
        '"stream_location": null}}, "traces": [{"properties": {"channel_code": '
        '"HNE", "location_code": "10", "as_recorded": true, "azimuth": 90, "dip": 0, '
        '"start_time": "2023-01-31T19:18:40Z", "end_time": "2023-01-31T19:19:10Z"}, '
        '"metrics": [{"properties": {"description": "Peak Ground Accleration", "name": '
        '"PGA", "units": "g", "provenance_ids": ["person", "software", "organization"], '
        '"time_of_peak": null}, "dimensions": null, "values": 1.5}, {"properties": '
        '{"description": "Spectral Acceleration", "name": "SA", "units": "g", '
        '"provenance_ids": ["person", "software", "organization"], "time_of_peak": '
        'null}, "dimensions": {"number": 2, "names": ["critical damping", "period"], '
        '"units": ["%", "s"], "axis_values": [[5], [0.3, 1, 3]]}, "values": '
        '[[1.2344, 1.4568, 1.6789]]}]}]}], "structure_reference_orientation": null}, '
        '"type": "Feature"}'
    )
    feature_json = feature.json(by_alias=True)
    cmp_dict = json.loads(cmp_json)
    feature_dict = json.loads(feature_json)
    res = DeepDiff(feature_dict, cmp_dict)
    cmp_changed_keys = [
        "root['properties']['streams'][0]['traces'][0]['properties']['start_time']",
        "root['properties']['streams'][0]['traces'][0]['properties']['end_time']",
    ]

    changed_keys = list(res["values_changed"].keys())
    assert changed_keys == cmp_changed_keys


if __name__ == "__main__":
    input_file = None
    save_file = False
    if len(sys.argv) > 1:
        input_file = pathlib.Path(sys.argv[1])
        save_file = bool(int(sys.argv[2]))
        dataframe_test(jsonfile=input_file, save_file=save_file)
    test_event()
    test_packet()
    test_loader()
    test_from_objects()
