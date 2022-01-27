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
    print(
        f"Summary of metrics for event {event['id']} "
        f"(file created {gmp['creation_time']})"
    )
    print("PROVENANCE")
    prov = gmp["provenance"]
    # To validate:
    # http://seismicdata.github.io/SEIS-PROV/validation.html
    # git clone https://github.com/SeismicData/SEIS-PROV.git
    # cd SEIS-PROV/validator
    # pip install -v -e .
    # from seis_prov_validate import validate
    # with open('test.json', 'w') as outfile:
    #     json.dump(prov, outfile)
    # result = validate("test.json")
    # result.is_valid
    # result.warnings
    #
    agents = prov["agent"]
    for provid, prov_dict in agents.items():
        print_provenance_agent(prov_dict)
    print("-" * 80)
    print("EVENT")
    print(f"  magnitude:    {event['magnitude']}")
    event_coords = gmp["event"]["geometry"]["coordinates"]
    print(f"  longitude:    {event_coords[0]} deg")
    print(f"  latitude:     {event_coords[1]} deg")
    print(f"  elevation:    {event_coords[2]} m")
    print("-" * 80)

    print("FEATURES")
    for station in gmp["features"]:
        sta_properties = station["properties"]
        sta_coords = station["geometry"]["coordinates"]
        print("── STATION")
        print(f"   name:           {sta_properties['name']}")
        print(f"   network code:   {sta_properties['network_code']}")
        print(f"   station code:   {sta_properties['station_code']}")

        for stream in sta_properties["streams"]:
            stream_properties = stream["properties"]
            print("──── STREAM")
            print(f"     band code:    {stream_properties['band_code']}")
            print(f"     inst code:    {stream_properties['instrument_code']}")
            print(f"     sample rate:  {stream_properties['samples_per_second']} Hz")

            housing = stream_properties["stream_housing"]
            print(f"     Housing: {housing}")
            print(f"       COSMOS code: {housing['cosmos_code']}")
            print(f"       description: {housing['description']}")
            print(f"       depth:       {housing['stream_depth']} m")

            for trace in stream["traces"]:
                trace_properties = trace["properties"]
                print("────── TRACE")
                print(f"       channel code:   {trace_properties['channel_code']}")
                print(f"       location code:  {trace_properties['location_code']}")
                print(f"       as recorded:    {trace_properties['as_recorded']}")
                print(f"       dip:            {trace_properties['dip']} deg")
                print(f"       azimuth:        {trace_properties['azimuth']} deg")
                print(f"       start time:     {trace_properties['start_time']}")
                print(f"       end time:       {trace_properties['end_time']}")

                print("──────── METRICS")
                for metric in trace["metrics"]:
                    print_metrics(metric, indent=9)


def print_provenance_agent(prov_dict):
    if prov_dict["prov:type"]["$"] == "prov:SoftwareAgent":
        software = prov_dict["seis_prov:software_name"]
        software_version = prov_dict["seis_prov:software_version"]
        print("── SOFTWARE")
        print(f"   name: {software}")
        print(f"   version: {software_version}")
    elif prov_dict["seis_prov:role"] == "data distributor":
        print("── DATA DISTRIBUTOR")
        dist_name = prov_dict["seis_prov:name"]
        print(f"   name: {dist_name}")
    elif prov_dict["seis_prov:role"] == "data provider":
        print("── DATA PROVIDER")
        provider_name = prov_dict["seis_prov:name"]
        print(f"   name: {provider_name}")
    if "seis_prov:website" in prov_dict:
        software_url = prov_dict["seis_prov:website"]["$"]
        print(f"   url: {software_url}")


def print_metrics(metric, indent=0):
    instr = " " * indent
    ndims = metric["dimensions"]["number"]
    metric_properties = metric["properties"]
    desc = metric_properties["description"]
    munits = format_units(metric_properties["units"])
    mvals = metric["values"]
    if ndims == 0:
        print(instr + f"{desc}: {mvals}{munits}")
    elif ndims == 1:
        dims = metric["dimensions"]
        dnames = dims["names"]
        dunits = dims["units"]
        dvals = dims["axis_values"]
        shape = len(dvals)
        dname0 = dnames[0]
        dunit0 = format_units(dunits[0])
        for ind0 in range(shape):
            dval0 = dvals[ind0]
            val = mvals[ind0]
            print(instr + f"{desc} [{dname0}={dval0}{dunit0}]: {val}{munits}")
    elif ndims == 2:
        dims = metric["dimensions"]
        dnames = dims["names"]
        dunits = dims["units"]
        dvals = dims["axis_values"]
        shape = [len(d) for d in dvals]
        for ind0 in range(shape[0]):
            dname0 = dnames[0]
            dunit0 = format_units(dunits[0])
            dval0 = dvals[0][ind0]

            for ind1 in range(shape[1]):
                dname1 = dnames[1]
                dunit1 = format_units(dunits[1])
                dval1 = dvals[1][ind1]

                val = mvals[ind0][ind1]
                print(
                    instr + f"{desc} "
                    f"[{dname0}={dval0}{dunit0}, "
                    f"{dname1}={dval1}{dunit1}]: {val}{munits}"
                )


def format_units(s):
    if s == "%":
        return s
    else:
        return f" {s}"


if __name__ == "__main__":
    main()
