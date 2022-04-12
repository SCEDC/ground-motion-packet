# -*- coding: utf-8 -*-

import glob
from distutils.core import setup


setup(
    name="gmpacket",
    description="A GeoJSON Specification for Ground Motion Metrics",
    include_package_data=True,
    author="Ellen Yu, Lijam Hagos, Jamie Steidl, Eric Thompson, Bruce Worden",
    author_email="emthompson@usgs.gov",
    url="https://github.com/SCEDC/ground-motion-packet",
    packages=["gmpacket"],
    package_data={"gmpacket": glob.glob("gmpacket/data/**", recursive=True)},
    entry_points={
        "console_scripts": [
            "gmpformat = gmpacket.bin.gmpformat:main",
        ]
    },
)
