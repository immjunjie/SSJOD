from pydantic import BaseModel
from typing import List, Optional, Dict

"""
Objectives

HistoriesModel [
    History
]

HistoryModel {
    time_elapsed (interger, optional),
    time_estimated (interger, optional),
    time_total (interger, optional),
    datetime_started (string, optional),
    datetime_finished (string, optional),
    datetime_cleaned (string, optional),
    results (string, optional) = ['Finished', 'Aborted'],
    source (string, optional),
    reprint_orginal_uuid (string, optional): UUID in UUID4 format,
    name: (string, optional),
    uuid: (string, optional): UUID in UUID4 format,
}

"""

class HistoryModel(BaseModel):
    time_elapsed: Optional[int] = None
    time_estimated: Optional[int] = None
    time_total: Optional[int] = None
    datetime_started: Optional[str] = None
    datetime_finished: Optional[str] = None
    datetime_cleaned: Optional[str] = None
    result: Optional[str] = None  # 'Finished' or 'Aborted'
    source: Optional[str] = None
    reprint_original_uuid: Optional[str] = None  # UUID in UUID4 format
    name: Optional[str] = None
    uuid: Optional[str] = None  # UUID in UUID4 format

class HistoriesModel(BaseModel):
    history: List[HistoryModel]

