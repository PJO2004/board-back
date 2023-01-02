import sys
import os
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)
from util import dbconn
from pydantic import BaseModel
from typing import Optional

class SlotB(BaseModel):
    slotid: str
    projectname: str
    individual: bool
    param: str = None
    naspath: Optional[str] = None
    nasdockerpath: Optional[str] = None
    filepath: Optional[str] = None
    filedockerpath: Optional[str] = None
    dockerimage: Optional[str] = None

    class Config:
        orm_mode: bool = True

class SlotUpdateB(BaseModel):
    slotid: str
    param: str = None
    naspath: Optional[str] = None
    nasdockerpath: Optional[str] = None
    filepath: Optional[str] = None
    filedockerpath: Optional[str] = None
    dockerimage: Optional[str] = None

    class Config:
        orm_mode: bool = True

class Slotlist:
    def __init__(self, slotid, projectname, userid, deploystate, regdtm, deploydtm):
        self.slotid = slotid
        self.projectname = projectname
        self.userid = userid
        self.deploystate = deploystate
        self.regdtm = regdtm
        self.deploydtm = deploydtm
