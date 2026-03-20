from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ORMBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TimestampModel(ORMBaseModel):
    created_at: datetime
