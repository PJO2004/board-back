import sys
import os
from pydantic import BaseModel

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)
from typing import Any, Dict, List, Optional

JSONObject = Dict[str, Any]


class ExecB(BaseModel):
    jobid: str
    slotid: str
    param: Optional[JSONObject] = None
    filelist: Optional[List] = None

    class Config:
        orm_mode: bool = True


class Result(BaseModel):
    outdir: str
    outparam: str

    class Config:
        orm_mode: bool = True


class Receive(BaseModel):
    jobid: str
    param: dict
    job_start_date: str
    job_end_date: str
    state: str
    errlog: Optional[str]
    results: Result

    class Config:
        orm_mode: bool = True
