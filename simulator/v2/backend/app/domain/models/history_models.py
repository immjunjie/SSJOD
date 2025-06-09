from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime
import uuid

class HistoryModel(BaseModel):
    time_elapsed: Optional[int] = None
    time_estimated: Optional[int] = None
    time_total: Optional[int] = None
    datetime_started: Optional[str] = None
    datetime_finished: Optional[str] = None
    datetime_cleaned: Optional[str] = None
    result: Optional[Literal["Finished", "Aborted"]] = None
    source: Optional[str] = None
    reprint_original_uuid: Optional[str] = None  # Should be UUID4 format
    name: Optional[str] = None
    uuid: Optional[str] = None  # Should be UUID4 format

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

class HistoriesModel(BaseModel):
    history: List[HistoryModel] = Field(default_factory=list)