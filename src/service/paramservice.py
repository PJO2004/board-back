from datetime import datetime
from sqlalchemy.orm import Session
import os
import sys
import json

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)
from util import gitlabHo
from constantstore import constant
from vo import paramvo
from mapper import slotmapper


def paramcreate(paramwithname: paramvo.ParamRequestS, userid, db: Session):
    projectid: str = paramwithname.slotid
    root_path: str = constant.DATA_PATH
    param: list = [i.__dict__ for i in paramwithname.param]
    dictvalue: dict = dict()
    for value in param:
        dictvalue[value.get("name")] = {
            "type": value.get("type"),
            "default": value.get("defalutvalue") if value.get("defalutvalue") is not None else None,
        }
    date: str = datetime.now().strftime("%Y%m%d%H%M%S")
    if os.path.exists(f"{root_path}/json/param_{projectid}.json"):
        file_oldname: str = os.path.join(f"{root_path}/json/", f"param_{projectid}.json")
        file_newname_newfile: str = os.path.join(
            f"{root_path}/json/", f"_param_{projectid}_{date}.json"
        )
        os.rename(file_oldname, file_newname_newfile)
    with open(f"{root_path}/json/param_{projectid}.json", "w", encoding="utf-8") as file:
        json.dump(dictvalue, file, indent=2)
    slotmapper.paramupdate(paramwithname, param, db)
    gitlabHo.jsonfileCreate(projectid)


def paramlist(projectid) -> dict:
    with open(f"{constant.DATA_PATH}/json/param_{projectid}.json", "r") as jsonfile:
        param_json: dict = json.load(jsonfile)
    return param_json
