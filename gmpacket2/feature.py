# stdlib imports
from datetime import datetime
from typing import List, Optional

# third party imports
from pydantic import BaseModel

# local imports
from gmpacket2.utils import datetime_to_iso8601


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


class MetricValues(BaseModel):
    values: List[List[float]]


class Metric(BaseModel):
    properties: MetricProperties
    dimensions: Optional[MetricDimensions]  # required when metric is an array
    values: MetricValues


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
