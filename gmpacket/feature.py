# stdlib imports
from datetime import datetime
from typing import List, Optional, Union

# third party imports
from pydantic import BaseModel

# local imports
from gmpacket.utils import datetime_to_iso8601


class MetricProperties(BaseModel):
    description: str
    name: str
    units: str
    provenance_ids: Optional[List[str]]
    time_of_peak: Optional[datetime]


class MetricDimensions(BaseModel):
    number: int
    names: List[str]
    units: List[str]
    axis_values: List[List[float]]


class Metric(BaseModel):
    properties: MetricProperties
    dimensions: Optional[MetricDimensions]  # required when metric is an array
    values: Union[List[List[float]], List[float], float]

    class Config:
        json_encoders = {
            # custom output conversion for datetime
            datetime: datetime_to_iso8601
        }


class TraceProperties(BaseModel):
    channel_code: str
    location_code: str
    as_recorded: bool
    azimuth: float
    dip: float
    start_time: datetime
    end_time: datetime

    class Config:
        json_encoders = {
            # custom output conversion for datetime
            datetime: datetime_to_iso8601
        }


class Trace(BaseModel):
    properties: TraceProperties
    metrics: List[Metric]

    class Config:
        json_encoders = {
            # custom output conversion for datetime
            datetime: datetime_to_iso8601
        }


class StreamHousing(BaseModel):
    cosmos_code: int
    description: str
    stream_depth: float
    stream_location: Optional[str]


class StreamProperties(BaseModel):
    band_code: str
    instrument_code: str
    samples_per_second: float
    stream_housing: StreamHousing


class Stream(BaseModel):
    properties: StreamProperties
    traces: List[Trace]

    class Config:
        json_encoders = {
            # custom output conversion for datetime
            datetime: datetime_to_iso8601
        }


class FeatureGeometry(BaseModel):
    type = "Point"
    coordinates: List[float]


class FeatureProperties(BaseModel):
    network_code: str
    station_code: str
    name: Optional[str]
    streams: List[Stream]
    structure_reference_orientation: Optional[int]


class Feature(BaseModel):
    type = "Feature"
    geometry: FeatureGeometry
    properties: FeatureProperties

    class Config:
        json_encoders = {
            # custom output conversion for datetime
            datetime: datetime_to_iso8601
        }
