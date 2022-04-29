#!/usr/bin/env python
# -*- encoding: utf8 -*-

import sys
import json
import csv

from gmpacket.validate import gmp_validate


def scan_gmp(gmp_file, print_what="all", csvfile=None):
    """Parse and scan through a GMP file.

    Args:
        gmp_file (str):
            Path to file to inspect.
        print (str):
            What to print? Valid values are: "all", "none", "summary".
        csvfile (str):
            Optional path to write contents as a CSV flatfile.

    """
    append = False
    if print_what == "all":
        print_summary = True
        print_detail = True
    elif print_what == "summary":
        print_summary = True
        print_detail = False
    elif print_what == "none":
        print_summary = False
        print_detail = False
    else:
        print(f"{print} not a valid option or 'print' argument. Exiting.")
        sys.exit()

    with open(gmp_file, "rt") as f:
        gmp = json.load(f)

    event = gmp["event"]["properties"]

    result = gmp_validate(gmp)
    print("-" * 80)
    print(f"Is GMP format valid? {result}")

    if print_summary:
        print("-" * 80)
        print(
            f"Summary of metrics for event {event['id']} "
            f"(file created {gmp['creation_time']})"
        )
        print("PROVENANCE")

    prov = gmp["provenance"]
    agents = prov["agent"]
    for _, prov_dict in agents.items():
        print_provenance_agent(prov_dict, print_summary)

    event_coords = gmp["event"]["geometry"]["coordinates"]

    if print_summary:
        print("-" * 80)
        print("EVENT")
        print(f"  magnitude:    {event['magnitude']}")
        print(f"  longitude:    {event_coords[0]} deg")
        print(f"  latitude:     {event_coords[1]} deg")
        print(f"  elevation:    {event_coords[2]} m")
        print("-" * 80)

    if print_detail:
        print("FEATURES")

    for station in gmp["features"]:
        sta_properties = station["properties"]
        # sta_coords = station["geometry"]["coordinates"]
        if print_detail:
            print("── STATION", print_detail)
            print(f"   name:           {sta_properties['name']}")
            print(f"   network code:   {sta_properties['network_code']}")
            print(f"   station code:   {sta_properties['station_code']}")

        for stream in sta_properties["streams"]:
            stream_properties = stream["properties"]
            housing = stream_properties["stream_housing"]
            if print_detail:
                print("──── STREAM")
                print(f"     band code:    {stream_properties['band_code']}")
                print(
                    f"     inst code:    {stream_properties['instrument_code']}",
                )
                print(
                    f"     sample rate:  {stream_properties['samples_per_second']} Hz",
                )

                print(f"     Housing: {housing}")
                print(f"       COSMOS code: {housing['cosmos_code']}")
                print(f"       description: {housing['description']}")
                print(f"       depth:       {housing['stream_depth']} m")

            for trace in stream["traces"]:
                trace_properties = trace["properties"]
                if print_detail:
                    print("────── TRACE")
                    print(
                        f"       channel code:   {trace_properties['channel_code']}",
                    )
                    print(
                        f"       location code:  {trace_properties['location_code']}",
                    )
                    print(
                        f"       as recorded:    {trace_properties['as_recorded']}",
                    )
                    print(
                        f"       dip:            {trace_properties['dip']} deg",
                    )
                    print(
                        f"       azimuth:        {trace_properties['azimuth']} deg",
                    )
                    print(
                        f"       start time:     {trace_properties['start_time']}",
                    )
                    print(
                        f"       end time:       {trace_properties['end_time']}",
                    )
                    print("──────── METRICS")

                for metric in trace["metrics"]:
                    # Collect list of items for each row in CSV file:
                    prop_dicts = [sta_properties, stream_properties, trace_properties]
                    col_info = get_init_row_names_vals(prop_dicts)
                    met_info = print_metrics(
                        metric, indent=9, print_detail=print_detail
                    )
                    if csvfile is not None:
                        write_csvfile(csvfile, col_info, met_info, append)
                        append = True


def write_csvfile(csvfile, col_info, met_info, append=False):
    colnames = col_info[0] + ["Metric Description"] + ["Metric Value"]
    if append:
        mode = "a"
    else:
        mode = "w"
    with open(csvfile, mode, newline="") as f:
        writer = csv.writer(f, delimiter=",", quoting=csv.QUOTE_MINIMAL)
        if not append:
            writer.writerow(colnames)
        for mname, mval in zip(met_info[0], met_info[1]):
            writer.writerow(col_info[1] + [mname] + [mval])


def get_init_row_names_vals(prop_dicts):
    col_names = []
    col_vals = []
    skip_keys = ["properties", "streams"]
    for properties in prop_dicts:
        for k, v in properties.items():
            if k in skip_keys:
                continue
            if k == "stream_housing":
                for k1, v1 in v.items():
                    col_names.append(f"housing, {k1}")
                    col_vals.append(v1)
            else:
                col_names.append(k)
                col_vals.append(v)
    return col_names, col_vals


def print_provenance_agent(prov_dict, print_summary):
    prov_type = prov_dict["prov:type"]["$"].replace("prov:", "")
    print(f"── {prov_type}")
    if "seis_prov:role" in prov_dict:
        print(f"   role: {prov_dict['seis_prov:role']}")
    if "seis_prov:name" in prov_dict:
        print(f"   name: {prov_dict['seis_prov:name']}")
    if "software" in prov_type.lower():
        software = prov_dict["seis_prov:software_name"]
        software_version = prov_dict["seis_prov:software_version"]
        if print_summary:
            print(f"   software_name: {software}")
            print(f"   software_version: {software_version}")
    if "seis_prov:website" in prov_dict:
        software_url = prov_dict["seis_prov:website"]["$"]
        if print_summary:
            print(f"   url: {software_url}")


def print_metrics(metric, indent=0, print_detail=True):
    metric_names = []
    metric_vals = []
    instr = " " * indent
    if "dimensions" in metric:
        ndims = metric["dimensions"]["number"]
    else:
        ndims = 0
    metric_properties = metric["properties"]
    desc = metric_properties["description"]
    munits = __format_units(metric_properties["units"])
    mvals = metric["values"]
    if ndims == 0:
        if print_detail:
            metric_name = desc
            metric_val = f"{mvals}{munits}"
            metric_names.append(metric_name)
            metric_vals.append(metric_val)
            print(instr + f"{metric_name}: {metric_val}")
    elif ndims == 1:
        dims = metric["dimensions"]
        dnames = dims["names"]
        dunits = dims["units"]
        dvals = dims["axis_values"][0]
        shape = len(dvals)
        dname0 = dnames[0]
        dunit0 = __format_units(dunits[0])
        for ind0 in range(shape):
            dval0 = dvals[ind0]
            val = mvals[ind0]
            if print_detail:
                metric_name = f"{desc} [{dname0}={dval0}{dunit0}]"
                metric_val = f"{val}{munits}"
                metric_names.append(metric_name)
                metric_vals.append(metric_val)
                print(instr + f"{metric_name}: {metric_val}")
    elif ndims == 2:
        dims = metric["dimensions"]
        dnames = dims["names"]
        dunits = dims["units"]
        dvals = dims["axis_values"]
        shape = [len(d) for d in dvals]
        for ind0 in range(shape[0]):
            dname0 = dnames[0]
            dunit0 = __format_units(dunits[0])
            dval0 = dvals[0][ind0]

            for ind1 in range(shape[1]):
                dname1 = dnames[1]
                dunit1 = __format_units(dunits[1])
                dval1 = dvals[1][ind1]

                val = mvals[ind0][ind1]
                if print_detail:
                    metric_name = (
                        f"{desc} [{dname0}={dval0}{dunit0}, "
                        f"{dname1}={dval1}{dunit1}]"
                    )
                    metric_val = f"{val}{munits}"
                    metric_names.append(metric_name)
                    metric_vals.append(metric_val)
                    print(instr + f"{metric_name}: {metric_val}")
    return metric_names, metric_vals


def __format_units(s):
    if s == "%":
        return s
    else:
        return f" {s}"
