from sqlalchemy.orm import Session
import os
import sys

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)
from vo import dbvo, groupvo
import commonmapper


def allgroup(db: Session) -> list:
    return db.query(dbvo.GroupT).all()


def grouplist(db: Session) -> list:
    return db.query(dbvo.GroupT.groupname, dbvo.GroupT.ownername, dbvo.GroupT.regdtm).all()


def get_group(groupname: str, db: Session):
    return db.query(dbvo.GroupT).filter(dbvo.GroupT.groupname == groupname).first()


def deletegroup(groupname: str, db: Session) -> None:
    db.query(dbvo.GroupT).filter(dbvo.GroupT.groupname == groupname).delete()


def add_group_member(user_group: groupvo.UserGroup, db: Session) -> groupvo.UserGroup:
    db.query(dbvo.UserT).filter(dbvo.UserT.userid == user_group.ownername).update(
        {"groupname": user_group.groupname}
    )
    db.commit()
    return user_group


def register_group(usergroup: groupvo.UserGroup, db: Session) -> dbvo.GroupT:
    db_group: dbvo.GroupT = dbvo.GroupT(
        groupname=usergroup.groupname, ownername=usergroup.ownername
    )
    commonmapper.insert_db(db_group,db)
    return db_group


def group_token_register(usergroup: groupvo.GroupInfo, db: Session) -> groupvo.GroupInfo:
    db.query(dbvo.GroupT).filter(dbvo.GroupT.groupname == usergroup.groupname).update(
        {"token": usergroup.token}
    )
    db.commit()
    return usergroup


def joingroup(userid: str, groupname: str, db: Session):
    db.query(dbvo.UserT).filter(dbvo.UserT.userid == userid).update({"groupname": groupname})
    db.commit()
    return groupname


def get_all_with_conditions(conditions: dict, db: Session) -> list:
    condition_list: list = commonmapper.conditioncreater(conditions, dbvo.GroupT)

    return (
        db.query(dbvo.GroupT.groupname, dbvo.GroupT.ownername, dbvo.GroupT.regdtm)
        .filter(*condition_list)
        .all()
    )


def get_one_with_conditions(conditions: dict, db: Session) -> list:
    condition_list: list = commonmapper.conditioncreater(conditions, dbvo.GroupT)
    return (
        db.query(dbvo.GroupT.groupname, dbvo.GroupT.ownername, dbvo.GroupT.regdtm)
        .filter(*condition_list)
        .first()
    )
