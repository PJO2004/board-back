from pydantic import BaseModel
from typing import Any, Dict, List

JSONObject = Dict[str, Any]


class ParamDefine(BaseModel):
    name: str
    type: str
    defalutvalue: Any


class ParamRequest(BaseModel):
    projectname: str
    param: List[ParamDefine]


class ParamRequestS(BaseModel):
    slotid: str
    param: List[ParamDefine]
