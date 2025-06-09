from pydantic import BaseModel
from typing import List
from typing import Optional

"""
Objectives

PrintJob {
time_elapsed (integer, optional),
time_total (integer, optional),
datetime_started (string, optional): Moment this print job started in ISO 8601 format ,
datetime_finished (string, optional): Moment this print job finished in ISO 8601 format or empty string if not finished yet ,
datetime_cleaned (string, optional): Moment this print job was cleaned in ISO 8601 format or empty string if build plate not cleaned yet ,
source (string, optional),
source_user (string, optional),
source_application (string, optional),
name (string, optional),
uuid (string, optional): UUID in UUID4 format. ,
reprint_original_uuid (string, optional): UUID in UUID4 format. ,
progress (number, optional): Estimated progress for the current print job, a value between 0 and 1 ,
state (string, optional) = ['none', 'printing', 'pausing', 'paused', 'resuming', 'pre_print', 'post_print', 'wait_cleanup', 'wait_user_action'],
result (string, optional) = ['Failed', 'Aborted', 'Finished']
}
"""

class PrintJobModel(BaseModel):
    time_elapsed: int
    time_total: int
    datetime_started: Optional[str] = None
    datetime_finished: Optional[str] = None
    datetime_cleaned: Optional[str] = None
    source: Optional[str] = None
    source_user: Optional[str] = None
    pause_source: Optional[str] = None
    source_application: Optional[str] = None
    name: Optional[str] = None
    uuid: str
    reprint_original_uuid: Optional[str] = None
    progress: float = 0.0
    state: str = 'none'  # Possible states: 'none', 'printing', 'pausing', 'paused', 'resuming', 'pre_print', 'post_print', 'wait_cleanup', 'wait_user_action'
    result: str = 'Failed'  # Possible results: 'Failed', 'Aborted', 'Finished'
