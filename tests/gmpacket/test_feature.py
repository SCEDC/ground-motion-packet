# stdlib imports
import json
import pathlib
from datetime import datetime, timedelta

# third party imports
from deepdiff import DeepDiff

# local imports
from gmpacket.feature import (
    CosmosCode,
    Feature,
    Metric,
    MetricDimensions,
    MetricProperties,
    Stream,
    StreamHousing,
    StreamProperties,
    Trace,
    TraceProperties,
)
from test_utils import get_jdict


def test_metric_properties():
    jdict = get_jdict()
    data = jdict["features"][0]["properties"]["streams"][0]["traces"][0]["metrics"][0][
        "properties"
    ]
    metprops = MetricProperties(**data)
    assert metprops.dict(by_alias=True) == data


def test_metric_dimensions():
    jdict = get_jdict()
    data = jdict["features"][0]["properties"]["streams"][0]["traces"][0]["metrics"][0][
        "dimensions"
    ]
    metdims = MetricDimensions(**data)
    assert metdims.dict(by_alias=True) == data


def test_metric():
    jdict = get_jdict()
    data = jdict["features"][0]["properties"]["streams"][0]["traces"][0]["metrics"][0]
    metric = Metric(**data)
    mdict = json.loads(metric.json(by_alias=True))
    cmp_dict = json.loads(json.dumps(data))
    assert DeepDiff(cmp_dict, mdict) == {}


def test_trace_properties():
    jdict = get_jdict()
    data = jdict["features"][0]["properties"]["streams"][0]["traces"][0]["properties"]
    traceprops = TraceProperties(**data)
    pdict = json.loads(traceprops.json(by_alias=True))
    cmp_dict = json.loads(json.dumps(data))
    assert DeepDiff(cmp_dict, pdict) == {}


def test_trace():
    jdict = get_jdict()
    data = jdict["features"][0]["properties"]["streams"][0]["traces"][0]
    trace = Trace(**data)
    tdict = json.loads(trace.json(by_alias=True))
    cmp_dict = json.loads(json.dumps(data))
    assert DeepDiff(cmp_dict, tdict) == {}


def test_stream_housing():
    jdict = get_jdict()
    data = jdict["features"][0]["properties"]["streams"][0]["properties"][
        "stream_housing"
    ]
    housing = StreamHousing(**data)
    assert housing.dict(by_alias=True) == data

    # test class constructors
    # from_enum(cls, code: CosmosCode, depth: float, location: str = ""):
    housing = StreamHousing.from_enum(CosmosCode.BUILDING, 33.0, "in a building")
    cmp_dict = {
        "cosmos_code": 10,
        "description": "Building",
        "stream_depth": 33.0,
        "stream_location": "in a building",
    }
    assert housing.dict(by_alias=True) == cmp_dict

    # from_int(cls, code: int, depth: float, location: str = ""):
    housing = StreamHousing.from_int(10, 33.0, "in a building")
    assert housing.dict(by_alias=True) == cmp_dict


def test_stream_properties():
    jdict = get_jdict()
    data = jdict["features"][0]["properties"]["streams"][0]["properties"]
    props = StreamProperties(**data)
    assert props.dict(by_alias=True) == data


def test_stream():
    jdict = get_jdict()
    data = jdict["features"][0]["properties"]["streams"][0]
    stream = Stream(**data)
    sdict = json.loads(stream.json(by_alias=True))
    cmp_dict = json.loads(json.dumps(data))
    assert DeepDiff(cmp_dict, sdict) == {}


def test_feature():
    jdict = get_jdict()
    data = jdict["features"][0]
    feature = Feature(**data)
    fdict = json.loads(feature.json(by_alias=True))
    cmp_dict = json.loads(json.dumps(data))
    assert DeepDiff(cmp_dict, fdict) == {}


if __name__ == "__main__":
    test_metric_properties()
    test_metric_dimensions()
    test_metric()
    test_trace_properties()
    test_trace()
    test_stream_housing()
    test_stream_properties()
    test_stream()
    test_feature()
