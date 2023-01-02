import os
import sys
from sqlalchemy import or_

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)
from vo import slotvo, paramvo, dbvo
from sqlalchemy.orm import Session
from datetime import datetime
import commonmapper

deploysa: str = "no"
deploysarunning: str = "st"


def get_slot(slotid: str, db: Session) -> dbvo.SlotT:
    slot: dbvo.SlotT = db.query(dbvo.SlotT).filter(dbvo.SlotT.slotid == slotid).first()
    return slot


def paramupdate(slotid: str, param: str, db: Session):
    db.query(dbvo.SlotT).filter(dbvo.SlotT.slotid == slotid).update({"param": param})
    db.commit()


def slotcreate(
    slotinfo: slotvo.SlotB, userid: str, token: str, projectinfo: dbvo.ProjectT, db: Session
) -> dbvo.SlotT:
    db_slot: dbvo.SlotT = dbvo.SlotT(
        slotid=slotinfo.slotid,
        projectname=slotinfo.projectname,
        userid=userid,
        token=token,
        param=projectinfo.param,
        deploystate=deploysa,
        naspath=slotinfo.naspath,
        nasdockerpath=slotinfo.nasdockerpath,
        filepath=slotinfo.filepath,
        filedockerpath=slotinfo.filedockerpath,
        dockerimage=slotinfo.dockerimage,
    )
    commonmapper.insert_db(db_slot, db)
    return db_slot


def deploystart(slotid: str, db: Session) -> str:
    db.query(dbvo.SlotT).filter(dbvo.SlotT.slotid == slotid).update({"deploydtm": datetime.now()})
    db.commit()
    return slotid


def slotdelete(slotid: str, db: Session):
    db.query(dbvo.SlotT).filter(dbvo.SlotT.slotid == slotid).delete()
    db.commit()


def defstateupdate(state: str, slotid: str, db: Session) -> str:
    if state == deploysarunning:
        db.query(dbvo.SlotT).filter(dbvo.SlotT.slotid == slotid).update(
            {"deploystate": state, "deploydtm": datetime.now()}
        )
    else:
        db.query(dbvo.SlotT).filter(dbvo.SlotT.slotid == slotid).update({"deploystate": state})
    db.commit()
    return slotid


def project_select_only(userid: str, db: Session) -> list:
    return db.query(dbvo.SlotT).filter(dbvo.SlotT.userid == userid).all()


def slot_list(userid: str, groupname: str, db: Session) -> list:
    if groupname:
        return (
            db.query(
                dbvo.SlotT.slotid,
                dbvo.SlotT.projectname,
                dbvo.SlotT.userid,
                dbvo.SlotT.deploystate,
                dbvo.SlotT.regdtm,
                dbvo.SlotT.deploydtm,
            )
            .filter(or_(dbvo.SlotT.userid == userid, dbvo.SlotT.groupname == groupname))
            .all()
        )
    return (
        db.query(
            dbvo.SlotT.slotid,
            dbvo.SlotT.projectname,
            dbvo.SlotT.userid,
            dbvo.SlotT.deploystate,
            dbvo.SlotT.regdtm,
            dbvo.SlotT.deploydtm,
        )
        .filter(dbvo.SlotT.userid == userid)
        .all()
    )


def get_all_with_conditions(conditions: dict, db: Session) -> list:
    condition_list: list = commonmapper.conditioncreater(conditions, dbvo.SlotT)
    return (
        db.query(
            dbvo.SlotT.slotid,
            dbvo.SlotT.projectname,
            dbvo.SlotT.userid,
            dbvo.SlotT.groupname,
            dbvo.SlotT.param,
            dbvo.SlotT.deploystate,
            dbvo.SlotT.regdtm,
            dbvo.SlotT.deploydtm,
            dbvo.SlotT.naspath,
            dbvo.SlotT.nasdockerpath,
            dbvo.SlotT.filepath,
            dbvo.SlotT.filedockerpath,
            dbvo.SlotT.dockerimage,
        )
        .filter(*condition_list)
        .all()
    )


def get_one_with_conditions(conditions: dict, db: Session) -> list:
    condition_list: list = commonmapper.conditioncreater(conditions, dbvo.SlotT)
    return (
        db.query(
            dbvo.SlotT.slotid,
            dbvo.SlotT.projectname,
            dbvo.SlotT.userid,
            dbvo.SlotT.groupname,
            dbvo.SlotT.param,
            dbvo.SlotT.deploystate,
            dbvo.SlotT.regdtm,
            dbvo.SlotT.deploydtm,
            dbvo.SlotT.naspath,
            dbvo.SlotT.nasdockerpath,
            dbvo.SlotT.filepath,
            dbvo.SlotT.filedockerpath,
            dbvo.SlotT.dockerimage,
        )
        .filter(*condition_list)
        .first()
    )


def updateslot(slotupdateinfo: slotvo.SlotUpdateB, db: Session):
    slotid: str = slotupdateinfo.slotid
    slotupdateinfo.__delattr__("slotid")
    db.query(dbvo.SlotT).filter(dbvo.SlotT.slotid == slotid).update(slotupdateinfo.__dict__)
    db.commit()


def paramupdate(param: paramvo.ParamRequestS, params: list, db: Session):
    db.query(dbvo.SlotT).filter(dbvo.SlotT.slotid == param.slotid).update({"param": str(params)})
    db.commit()
    return param
