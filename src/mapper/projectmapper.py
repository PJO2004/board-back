import os
import sys
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime
import commonmapper

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)
from vo import projectvo, paramvo, dbvo


def get_project(projectname: str, db: Session) -> dbvo.ProjectT:
    return db.query(dbvo.ProjectT).filter(dbvo.ProjectT.projectname == projectname).first()


def projectCreate(projectinfo: projectvo.Project_class, db: Session) -> dbvo.ProjectT:
    db_project: dbvo.ProjectT = dbvo.ProjectT(
        projectname=projectinfo.projectname,
        userid=projectinfo.userid,
        groupname=projectinfo.groupname,
        giturl=projectinfo.giturl,
        token=projectinfo.token,
    )
    commonmapper.insert_db(db_project, db)
    return db_project


def project_select_with_group(userid: str, groupname: str, db: Session) -> list:
    return (
        db.query(dbvo.ProjectT)
        .filter(or_(dbvo.ProjectT.userid == userid, dbvo.ProjectT.groupname == groupname))
        .all()
    )


def project_select_only(userid: str, db: Session) -> list:
    return db.query(dbvo.ProjectT).filter(dbvo.ProjectT.userid == userid).all()


def deploystart(prject_name: str, db: Session) -> str:
    db.query(dbvo.ProjectT).filter(dbvo.ProjectT.projectname == prject_name).update(
        {"deploytime": datetime.now()}
    )
    db.commit()
    return prject_name


def defstateupdate(state: str, projectname: str, db: Session) -> str:
    db.query(dbvo.ProjectT).filter(dbvo.ProjectT.projectname == projectname).update(
        {"deploystate": state}
    )
    db.commit()
    return projectname


def projectdelete(projectname: str, userid: str, db: Session) -> None:
    db.query(dbvo.ProjectT).filter(dbvo.ProjectT.projectname == projectname).delete()
    db.commit()


def paramselect(projectname: str, db: Session) -> dbvo.ProjectT:
    return db.query(dbvo.ProjectT).filter(dbvo.ProjectT.projectname == projectname).first()


def paramupdate(param: paramvo.ParamRequest, params: list, db: Session):
    db.query(dbvo.ProjectT).filter(dbvo.ProjectT.projectname == param.projectname).update(
        {"param": str(params)}
    )
    db.commit()
    return param


def projectImport(
    project_info: projectvo.ProjectImportInsert, groupname: str, db: Session
) -> dbvo.ProjectT:
    db_project: dbvo.ProjectT = dbvo.ProjectT(
        projectname=project_info.projectname,
        userid=project_info.userid,
        groupname=groupname if groupname else None,
        giturl=project_info.giturl,
        token=project_info.token,
    )
    commonmapper.insert_db(db_project, db)
    return db_project


def get_all_with_conditions(conditions: dict, db: Session) -> list:
    condition_list: list = commonmapper.conditioncreater(conditions, dbvo.ProjectT)
    return (
        db.query(
            dbvo.ProjectT.projectname,
            dbvo.ProjectT.userid,
            dbvo.ProjectT.groupname,
            dbvo.ProjectT.reg_dtm,
            dbvo.ProjectT.giturl,
            dbvo.ProjectT.param,
        )
        .filter(*condition_list)
        .all()
    )


def get_one_with_conditions(conditions: dict, db: Session) -> list:
    condition_list: list = commonmapper.conditioncreater(conditions, dbvo.ProjectT)
    return (
        db.query(
            dbvo.ProjectT.projectname,
            dbvo.ProjectT.userid,
            dbvo.ProjectT.groupname,
            dbvo.ProjectT.reg_dtm,
            dbvo.ProjectT.giturl,
            dbvo.ProjectT.param,
        )
        .filter(*condition_list)
        .first()
    )
