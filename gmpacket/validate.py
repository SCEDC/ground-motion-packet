#!/usr/bin/env python
# -*- encoding: utf8 -*-

import json
import io
from schema import Schema, Optional, Or
from datetime import datetime

from seis_prov_validate import validate


def datetime_valid(str):
    """Check that str is ISO 8601 extended.

    Args:
        str (str):
            String to validte.

    Returns:
        bool: is it ISO 8601 extended?
    """
    try:
        datetime.fromisoformat(str)
    except BaseException:
        try:
            datetime.fromisoformat(str.replace("Z", "+00:00"))
        except BaseException:
            return False
        return True
    return True


def get_dims(a):
    if not type(a) == list:
        return []
    return [len(a)] + get_dims(a[0])


GMP_SCHEMA = Schema(
    {
        "version": str,
        "creation_time": str,
        "provenance": dict,
        "type": "FeatureCollection",
        "features": list,
        Optional("event"): {
            "type": "Feature",
            "properties": {"id": str, "time": str, "magnitude": float},
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
            "start_time": str,
            "end_time": str,
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
            Optional("provenance_ids"): list,
            Optional("time_of_peak"): str,
        },
        Optional("dimensions"): {
            "number": int,
            "names": list,
            "units": list,
            "axis_values": list,
        },
        "values": Or(list, float),
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

        if not datetime_valid(gmp_dict["creation_time"]):
            raise ValueError("creation_time is not a valid format.")

        # event dict is optional
        if "event" in gmp_dict:
            event_time = gmp_dict["event"]["properties"]["time"]
            if not datetime_valid(event_time):
                raise ValueError("Event time is not a valid format.")

        # Validate features
        for feature in gmp_dict["features"]:
            FEATURES_SCHEMA.validate(feature)

            # Validate streams
            for stream in feature["properties"]["streams"]:
                STREAMS_SCHEMA.validate(stream)

                # Validate traces
                for trace in stream["traces"]:
                    TRACES_SCHEMA.validate(trace)

                    if not datetime_valid(trace["properties"]["start_time"]):
                        raise ValueError("Trace start_time is not a valid format.")
                    if not datetime_valid(trace["properties"]["end_time"]):
                        raise ValueError("Trace end_time is not a valid format.")

                    # Validate metrics
                    for metric in trace["metrics"]:
                        METRICS_SCHEMA.validate(metric)

                        # time_of_peak is optional
                        mproperties = metric["properties"]
                        if "time_of_peak" in mproperties:
                            if not datetime_valid(mproperties["time_of_peak"]):
                                raise ValueError(
                                    "Metric time_of_peak is not a valid format."
                                )

                        if "provenance_ids" in metric["properties"]:
                            for pid in metric["properties"]["provenance_ids"]:
                                if not isinstance(pid, str):
                                    raise ValueError(
                                        "provenance_ids must be a list of strings."
                                    )
                        if "dimensions" in metric:
                            # Metric dimension number
                            ndim = metric["dimensions"]["number"]
                            if not ndim > 0:
                                raise ValueError(
                                    "metric dimension number must be greater than zero."
                                )
                            if ndim > 2:
                                # Note, to support higher dimensions we will need to
                                # gmpacket.scan.print_metrics to handle it. There
                                # should be a more elgant way to handle this than what
                                # we are currently doing.
                                raise ValueError(
                                    "metric dimension number must be greater than 2 "
                                    "not yet supported."
                                )

                            # Metric dimension names
                            md_names = metric["dimensions"]["names"]
                            if len(md_names) != ndim:
                                raise ValueError(
                                    "length of metric dimension names must be equal to "
                                    "metric dimension number."
                                )

                            # Metric dimension units
                            md_units = metric["dimensions"]["units"]
                            if len(md_units) != ndim:
                                raise ValueError(
                                    "length of metric dimension units must be equal to "
                                    "metric dimension number."
                                )

                            # Metric dimension axis_values
                            md_avals = metric["dimensions"]["axis_values"]
                            if len(md_avals) != ndim:
                                raise ValueError(
                                    "length of metric dimension axis_values must be "
                                    "equal to metric dimension number."
                                )
                            metric_dims = [len(a) for a in md_avals]

                            # Metric values
                            if not isinstance(metric["values"], list):
                                raise ValueError(
                                    "metric dimension values must be a list when the "
                                    "metric is an array."
                                )
                            metric_val_dims = get_dims(metric["values"])
                            if not metric_val_dims == metric_dims:
                                raise ValueError(
                                    "metric value dimensions are inconsistent with "
                                    "metric dimesion axis_values."
                                )

                        else:
                            # Metric values
                            if not isinstance(metric["values"], float):
                                raise ValueError(
                                    "metric values must be float when the metric is "
                                    "scalar."
                                )

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
