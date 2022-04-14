#!/usr/bin/env python
# -*- encoding: utf8 -*-

import json
import io
from schema import Schema, Optional, Or

from seis_prov_validate import validate

# note:
#   pip install schema

GMP_SCHEMA = Schema(
    {
        "version": str,
        "creation_time": str,
        "provenance": dict,
        "type": "FeatureCollection",
        "features": list,
        Optional("event"): {
            "type": "Feature",
            "properties": {"id": str, "time": str, "magnitude": float},  # ISO 8601
            "geometry": {"type": str, "coordinates": [float, float, float]},
        },
    }
)

FEATURES_SCHEMA = Schema(
    {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [float, float, float]},
        "properties": {
            "network_code": str,
            "station_code": str,
            "name": str,
            "streams": list,
            Optional("structure_reference_orientation"): float,
        },
    }
)

STREAMS_SCHEMA = Schema(
    {
        "properties": {
            "band_code": str,
            "instrument_code": str,
            "samples_per_second": float,
            "stream_housing": {
                "cosmos_code": int,
                "description": str,
                "stream_depth": float,
            },
        },
        "traces": list,
    }
)

TRACES_SCHEMA = Schema(
    {
        "properties": {
            "channel_code": str,
            "location_code": str,
            "as_recorded": bool,
            "azimuth": float,
            "dip": float,
            "start_time": str,  # ISO 8601
            "end_time": str,  # ISO 8601
        },
        "metrics": list,
    }
)

METRICS_SCHEMA = Schema(
    {
        "properties": {
            "description": str,
            "name": str,
            "units": str,
            Optional("provenance_ids"): list,  # list of str
            Optional("time_of_peak"): str,  # ISO 8601
        },
        Optional("dimensions"): {
            "number": int,  # >0
            "names": list,  # check len equals number
            "units": list,  # check len equals number
            "axis_values": list,  # check dims; list of lists
        },
        "values": Or(list, float),  # check dims; list of lists, list if dims exist
    }
)


def gmp_validate(gmp_dict, allow_exceptions=False):
    """Validate GMP schema

    Args:
        gmp_dict (dict):
            A dictionary to check if it meets the GMP spec.
        allow_exceptions (bool):
            Raise exceptions if encountered?

    Returns:
        bool: Did it validate?
    """
    try:
        # Validate base level
        GMP_SCHEMA.validate(gmp_dict)

        # Validate features
        for feature in gmp_dict["features"]:
            FEATURES_SCHEMA.validate(feature)

            # Validate streams
            for stream in feature["properties"]["streams"]:
                STREAMS_SCHEMA.validate(stream)

                # Validate traces
                for trace in stream["traces"]:
                    TRACES_SCHEMA.validate(trace)

                    # Validate metrics
                    for metric in trace["metrics"]:
                        METRICS_SCHEMA.validate(metric)
                        if "provenance_ids" in metric["properties"]:
                            for pid in metric["properties"]["provenance_ids"]:
                                assert isinstance(pid, str)
                        if "dimensions" in metric:
                            assert metric["dimensions"]["number"] > 0
                            assert isinstance(metric["values"], list)
                        else:
                            assert isinstance(metric["values"], float)

        prov = gmp_dict["provenance"]
        prov_string = json.dumps(prov)
        prov_io = io.BytesIO(prov_string.encode())
        result = validate(prov_io)
        assert result.is_valid
        return True
    except BaseException as ex:
        if allow_exceptions:
            raise ex
        return False
