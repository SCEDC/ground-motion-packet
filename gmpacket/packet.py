# stdlib imports
import re
from datetime import datetime
from typing import List, Optional

# third party imports
import numpy as np
import pandas as pd
from pydantic import BaseModel

# local imports
from gmpacket.feature import Feature
from gmpacket.provenance import Provenance
from gmpacket.utils import datetime_to_iso8601


class Event(BaseModel):
    type: str = "Feature"
    properties: dict
    geometry: dict

    @classmethod
    def from_parameters(cls, id, time, magnitude, lat, lon, depth):
        props = {"id": id, "time": time, "magnitude": magnitude}
        geometry = {"type": "Point", "coordinates": [lon, lat, depth * 1000]}
        return cls(properties=props, geometry=geometry)

    class Config:
        json_encoders = {
            # custom output conversion for datetime
            datetime: datetime_to_iso8601
        }


class GroundMotionPacket(BaseModel):
    type = "FeatureCollection"
    version: str
    creation_time: datetime = datetime.utcnow()
    event: Optional[Event]
    provenance: Provenance
    features: List[Feature]

    class Config:
        json_encoders = {
            # custom output conversion for datetime
            datetime: datetime_to_iso8601
        }

    def to_dataframe(self):
        event_dict = self.event.properties.copy()
        cdict = dict(
            zip(
                ["event_longitude", "event_latitude", "event_depth"],
                self.event.geometry["coordinates"],
            )
        )
        event_dict.update(cdict)
        rows = []
        for feature in self.features:
            row = {}
            row.update(event_dict)
            row["network"] = feature.properties.network_code
            row["station"] = feature.properties.station_code
            row["station_name"] = feature.properties.name
            (
                row["station_longitude"],
                row["station_latitude"],
                row["station_elevation"],
            ) = feature.geometry.coordinates
            for stream in feature.properties.streams:
                for trace in stream.traces:
                    row["channel"] = trace.properties.channel_code
                    row["location"] = trace.properties.location_code
                    for metric in trace.metrics:
                        metric_type = metric.properties.name
                        metric_units = metric.properties.units
                        values = np.array(metric.values)
                        if metric.dimensions is None:  # scalar value
                            key = f"{metric_type}({metric_units})"
                            value = metric.values
                            row[key] = value
                        elif metric.dimensions.number == 2:
                            nrows, ncols = values.shape
                            key_template = f"{metric_type}({metric_units})_"
                            for irow in range(0, nrows):
                                row_name = re.sub(
                                    r"\s+", "_", metric.dimensions.names[0]
                                )
                                row_label = metric.dimensions.axis_values[0][irow]
                                row_unit = metric.dimensions.units[0]
                                for jcol in range(0, ncols):
                                    col_name = re.sub(
                                        r"\s+", "_", metric.dimensions.names[1]
                                    )
                                    col_label = metric.dimensions.axis_values[1][jcol]
                                    col_unit = metric.dimensions.units[1]
                                    key = (
                                        key_template
                                        + f"{row_name}_{row_label}{row_unit}_{col_name}_{col_label}{col_unit}"
                                    )
                                    value = values[irow, jcol]
                                    row[key] = value
                        elif metric.dimensions.number != 2:
                            raise Exception("Can't support 1d arrays yet!")
                        rows.append(row)

        dataframe = pd.DataFrame(rows)
        return dataframe
