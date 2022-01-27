#!/usr/bin/env python

import argparse
import json


def main():
    description = "Parse and print metrics from a GMP file."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("file", help="Path to GMP file.", type=str)
    args = parser.parse_args()
    gmp_file = args.file
    with open(gmp_file, "rt") as f:
        gmp = json.load(f)

    event = gmp["event"]["properties"]

    print("-" * 80)
    print(f"Summary of metrics for event {event['id']}")
    print(f"    magnitude:\t{event['magnitude']}")
    event_coords = gmp["event"]["geometry"]["coordinates"]
    print(f"    longitude:\t{event_coords[0]} degrees")
    print(f"    latitude:\t{event_coords[1]} degrees")
    print(f"    elevation:\t{event_coords[2]} m")

    for station in gmp["features"]:
        sta_properties = station["properties"]
        sta_coords = station["geometry"]["coordinates"]
        print(f"── name:\t{sta_properties['name']}")
        print(f"   network code:\t{sta_properties['network_code']}")
        print(f"   station code:\t{sta_properties['station_code']}")

        for stream in sta_properties["streams"]:
            stream_properties = stream["properties"]
            print(f"──── band code:\t{stream_properties['band_code']}")
            print(f"     inst code:\t{stream_properties['instrument_code']}")
            print(f"     sampel rate:\t{stream_properties['samples_per_second']} Hz")

            housing = stream_properties["stream_housing"]
            print(f"     Housing: {housing}")

            for trace in stream["traces"]:
                trace_properties = trace["properties"]
                print(f"────── channel code:\t{trace_properties['channel_code']}")
                print(f"       location code:\t{trace_properties['location_code']}")
                print(f"       as recorded:\t{trace_properties['as_recorded']}")
                print(f"       dip:\t{trace_properties['dip']} deg")
                print(f"       azimuth:\t{trace_properties['azimuth']} deg")
                print(f"       start time:\t{trace_properties['start_time']}")
                print(f"       end time:\t{trace_properties['end_time']}")

                print("       METRICS:")
                for metric in trace["metrics"]:
                    print_metrics(metric, indent=9)


def print_metrics(metric, indent=0):
    instr = " " * indent
    ndims = metric["dimensions"]["number"]
    metric_properties = metric["properties"]
    desc = metric_properties["description"]
    munits = metric_properties["units"]
    mvals = metric["values"]
    if ndims == 0:
        print(instr + f"{desc}: {mvals}, {munits}")
    elif ndims == 1:
        dims = metric["dimensions"]
        dnames = dims["names"]
        dunits = dims["units"]
        dvals = dims["axis_values"]
        shape = len(dvals)
        dname0 = dnames[0]
        dunit0 = dunits[0]
        for ind0 in range(shape):
            dval0 = dvals[ind0]
            val = mvals[ind0]
            print(instr + f"{desc} [{dname0}={dval0} {dunit0}]: {val}, {munits}")
    elif ndims == 2:
        dims = metric["dimensions"]
        dnames = dims["names"]
        dunits = dims["units"]
        dvals = dims["axis_values"]
        shape = [len(d) for d in dvals]
        for ind0 in range(shape[0]):
            dname0 = dnames[0]
            dunit0 = dunits[0]
            dval0 = dvals[0][ind0]

            for ind1 in range(shape[1]):
                dname1 = dnames[1]
                dunit1 = dunits[1]
                dval1 = dvals[1][ind1]

                val = mvals[ind0][ind1]
                print(
                    instr + f"{desc} "
                    f"[{dname0}={dval0} {dunit0}, "
                    f"{dname1}={dval1} {dunit1}]: {val} {munits}"
                )


if __name__ == "__main__":
    main()
