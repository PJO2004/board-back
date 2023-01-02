import os
import sys
import yaml
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from service import hokinsservice

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)
from vo import slotvo, dbvo
from mapper import slotmapper, projectmapper, usermapper
from util import gitlabHo
from constantstore import constant


def slotcreate(slotinfo: slotvo.SlotB, userid: str, db: Session) -> bool:
    try:
        token: str = usermapper.taketoken(userid, db)[0]
        projectinfo: dbvo.ProjectT = projectmapper.get_project(slotinfo.projectname, db)
        slotmapper.slotcreate(slotinfo, userid, token, projectinfo, db)
        gitlabHo.slotprojectcreate(slotinfo.projectname, userid, slotinfo.slotid)
        gitlabHo.dockerfileCreate(slotinfo.slotid, slotinfo.dockerimage)
        # gitlabHo.jsonfileCreate(slotinfo.projectname, slotinfo.slotid)
        gitlabHo.anodeupload(slotinfo.slotid)
        if not gitlabHo.detectfile(slotinfo.projectname):
            gitlabHo.requirementfileCreate(slotinfo.slotid)
        return True
    except Exception as e:
        logging.info(str(e))
        return False


def slotdelete(slotid: str, db: Session):
    try:
        gitlabHo.slotdelete(slotid)
        slotmapper.slotdelete(slotid, db)
    except Exception as e:
        logging.info(str(e))
        return False


def slotlistview(userid: str, groupname: str, db: Session) -> list:
    return slotmapper.slot_list(userid, groupname, db)


def slotymlremove(slotid):
    root_path: str = constant.DATA_PATH
    filename: str = f"{root_path}/yaml/param_{slotid}.yml"
    if os.path.exists(filename):
        os.remove(filename)
    hokinsservice.dashboard_delete(slotid)


def get_slot(slotid: str, db: Session) -> dict:
    slotinfo: dbvo.SlotT = slotmapper.get_slot(slotid, db)
    return slotinfo.__dict__


def group_user_checker(slot_info: dbvo.SlotT, userid: str, groupname: str):
    if groupname:
        if slot_info.groupname == groupname:
            return True
    if slot_info.userid == userid:
        return True
    return False


def slot_dockerimage_update(slotupdateinfo: slotvo.SlotUpdateB):
    gitlabHo.dockerfileCreate(slotupdateinfo.slotid, slotupdateinfo.dockerimage)


def slotupdate(slotupdateinfo: slotvo.SlotUpdateB, db: Session):
    if slotupdateinfo.dockerimage:
        slot_dockerimage_update(slotupdateinfo)
    slotmapper.updateslot(slotupdateinfo, db)
