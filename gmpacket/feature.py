# stdlib imports
from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

# third party imports
import numpy as np
from pydantic import BaseModel, ConfigDict, model_validator

# local imports
from gmpacket.utils import datetime_to_iso8601


class CosmosCode(Enum):
    FIBERGLASS_SHELTER = (1, "Small fiberglass shelter")
    PREFAB_METAL_BLDG = (2, "Small prefabricated metal bldg")
    SENSOR_BURIED = (3, "Sensors buried/set in ground")
    REFERENCE_STATION = (4, "Reference station")
    BUILDING_BASE = (5, "Base of building")
    FREEFIELD = (6, "Freefield, Unspecified")
    OCEAN_BOTTOM = (7, "Ocean-bottom sensors")
    SHALLOW_VAULT = (8, "Sensors in small near-surface vault (1-2m deep)")
    LARGE_VAULT = (
        9,
        "Sensors in underground observatory or large vault (~3 m^3 or larger)",
    )
    BUILDING = (10, "Building")
    BRIDGE = (11, "Bridge")
    DAM = (12, "Dam")
    WHARF = (13, "Wharf")
    TUNNEL = (14, "Tunnel or mine adit (3m or more from surface)")
    LIFELINE_STRUCTURE = (15, "Other lifeline structure")
    OTHER_STRUCTURE = (20, "Other structure")
    GEOTECH_ARRAY = (50, "Geotechnical array")
    OTHER_ARRAY = (51, "Other array")
    UNSPECIFIED = (999, "Other array")


BUILDING_TYPES = {
    1: "Small fiberglass shelter",
    2: "Small prefabricated metal bldg",
    3: "Sensors buried/set in ground",
    4: "Reference station",
    5: "Base of building",
    6: "Freefield, Unspecified",
    7: "Ocean-bottom sensors",
    8: "Sensors in small near-surface vault (1-2m deep)",
    9: "Sensors in underground observatory or large vault (~3 m^3 or larger)",
    10: "Building",
    11: "Bridge",
    12: "Dam",
    13: "Wharf",
    14: "Tunnel or mine adit (3m or more from surface)",
    15: "Other lifeline structure",
    20: "Other structure",
    50: "Geotechnical array",
    51: "Other array",
    999: "Unspecified",
}


class MetricProperties(BaseModel):
    """Represent a ground motion packet MetricProperties object."""

    description: str
    name: str
    units: str
    provenance_ids: Optional[List[str]] = None
    time_of_peak: Optional[datetime] = None


class MetricDimensions(BaseModel):
    """Represent a ground motion packet MetricDimensions object."""

    number: int
    names: List[str]
    units: List[str]
    axis_values: List[List[float]]

    @model_validator(mode="before")
    def check_dimensions(cls, values):
        ndims = values["number"]
        assert len(values["names"]) == ndims
        return values


class Metric(BaseModel):
    """Represent a ground motion packet Metric object."""

    properties: MetricProperties
    dimensions: Optional[MetricDimensions] = None  # required when metric is an array
    values: Union[List[List[float]], List[float], float]

    @model_validator(mode="before")
    def check_dimensions(cls, values):
        if "dimensions" in values and values["dimensions"] is not None:
            if "number" in values["dimensions"]:
                ndims = values["dimensions"]["number"]
            else:
                ndims = values["dimensions"].number
            assert ndims == np.array(values["values"]).ndim
        return values


class TraceProperties(BaseModel):
    """Represent a ground motion packet TraceProperties object."""

    channel_code: str
    location_code: str
    as_recorded: bool
    azimuth: float
    dip: float
    start_time: datetime
    end_time: datetime


class Trace(BaseModel):
    """Represent a ground motion packet Trace object."""

    properties: TraceProperties
    metrics: List[Metric]


class StreamHousing(BaseModel):
    """Represent a ground motion packet StreamHousing object."""

    cosmos_code: int
    description: str
    stream_depth: float
    stream_location: Optional[str] = None

    @classmethod
    def from_enum(cls, code: CosmosCode, depth: float, location: str = ""):
        cosmos_code, description = CosmosCode(code).value
        return cls(
            cosmos_code=cosmos_code,
            description=description,
            stream_depth=depth,
            stream_location=location,
        )

    @classmethod
    def from_int(cls, code: int, depth: float, location: str = ""):
        description = BUILDING_TYPES[code]
        return cls(
            cosmos_code=code,
            description=description,
            stream_depth=depth,
            stream_location=location,
        )


class StreamProperties(BaseModel):
    """Represent a ground motion packet StreamProperties object."""

    band_code: str
    instrument_code: str
    samples_per_second: float
    stream_housing: StreamHousing


class Stream(BaseModel):
    """Represent a ground motion packet Stream object."""

    properties: StreamProperties
    traces: List[Trace]


class FeatureGeometry(BaseModel):
    """Represent a ground motion packet FeatureGeometry object."""

    type: str = "Point"
    coordinates: List[float]


class FeatureProperties(BaseModel):
    """Represent a ground motion packet FeatureProperties object."""

    network_code: str
    station_code: str
    name: Optional[str] = None
    streams: List[Stream]
    structure_reference_orientation: Optional[int] = None


class Feature(BaseModel):
    """Represent a ground motion packet Feature object."""

    type: str = "Feature"
    geometry: FeatureGeometry
    properties: FeatureProperties
