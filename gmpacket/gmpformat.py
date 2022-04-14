#!/usr/bin/env python
# -*- encoding: utf8 -*-

import json
import argparse
from gmpacket.scan import scan_gmp
from gmpacket.validate import gmp_validate


def run_gmpformat():
    # Main program parser
    description = """
        This is a program for describing, validating, and converting Ground
        Motion Packet (GMP) formatted data.
        """
    parser = argparse.ArgumentParser(description=description)
    subparsers = parser.add_subparsers(title="subcommands")

    parsers = []
    sub_name = ["print", "csv", "validate"]
    sub_desc = [
        "Print GMP file contents.",
        "Convert GMP file contents to a CSV flatfile.",
        "Validate a GMP file; will print encountered error messages.",
    ]
    methods = [__print, __convert, __validate]
    for name, desc, meth in zip(sub_name, sub_desc, methods):
        sub = subparsers.add_parser(name, help=desc)
        sub.add_argument("file", type=str, help="Path to GMP file.")
        if name == "print":
            sub.add_argument(
                "-w",
                "--what",
                type=str,
                help="What to print. Default: 'summary'.",
                choices=["all", "summary"],
                default="summary",
            )
        elif name == "csv":
            sub.add_argument(
                "-o",
                "--outfile",
                type=str,
                help="Output CSV file.",
            )

        sub.set_defaults(func=meth)
        parsers.append(sub)

    args = parser.parse_args()

    if args.func:
        args.func(args)


def __print(args):
    scan_gmp(args.file, print_what=args.what)


def __convert(args):
    scan_gmp(args.file, csvfile=args.outfile)


def __validate(args):
    with open(args.file, "rt") as f:
        gmp = json.load(f)
    result = gmp_validate(gmp, allow_exceptions=True)
    print(f"Is GMP format valid? {result}")
