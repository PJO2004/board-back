import os
import sys
from sqlalchemy.orm import Session

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)
from vo import uservo, dbvo
import commonmapper


def get_user(userid: str, db: Session) -> dbvo.UserT:
    return db.query(dbvo.UserT).filter(dbvo.UserT.userid == userid).first()


def create_user(user: uservo.UserInfoN, db: Session) -> dbvo.UserT:
    db_user: dbvo.UserT = dbvo.UserT(
        userid=user.userid,
        username=user.username,
        email=user.email,
        password=user.hashedpassword,
        groupname=user.groupname,
    )
    commonmapper.insert_db(db_user, db)
    return db_user


def user_token_register(user_info: uservo.UserInfoN, db: Session) -> uservo.UserInfoN:
    db.query(dbvo.UserT).filter(dbvo.UserT.userid == user_info.userid).update(
        {"token": user_info.token}
    )
    db.commit()
    return user_info


def taketoken(userid: str, db: Session):
    return db.query(dbvo.UserT.token).filter(dbvo.UserT.userid == userid).first()


def user_delete(userid: str, db: Session) -> str:
    db.query(dbvo.UserT).filter(dbvo.UserT.userid == userid).delete()
    db.commit()
    return userid


def selectallusers(db: Session) -> list:
    return db.query(
        dbvo.UserT.userid,
        dbvo.UserT.username,
        dbvo.UserT.email,
        dbvo.UserT.password,
        dbvo.UserT.groupname,
        dbvo.UserT.regdtm,
    ).all()


def grantforadmin(userid: str, db: Session):
    db.query(dbvo.UserT).filter(dbvo.UserT.userid == userid).update({"administer": True})
    db.commit()


def get_all_with_conditions(conditions: dict, db: Session) -> list:
    condition_list: list = commonmapper.conditioncreater(conditions, dbvo.UserT)
    return (
        db.query(
            dbvo.UserT.userid,
            dbvo.UserT.username,
            dbvo.UserT.email,
            dbvo.UserT.groupname,
            dbvo.UserT.regdtm,
            dbvo.UserT.administer,
        )
        .filter(*condition_list)
        .all()
    )


def get_one_with_conditions(conditions: dict, db: Session) -> list:
    condition_list: list = commonmapper.conditioncreater(conditions, dbvo.UserT)
    return (
        db.query(
            dbvo.UserT.userid,
            dbvo.UserT.username,
            dbvo.UserT.email,
            dbvo.UserT.groupname,
            dbvo.UserT.regdtm,
            dbvo.UserT.administer,
        )
        .filter(*condition_list)
        .first()
    )


def user_update(userid: str, user_info: dict, db: Session):
    db.query(dbvo.UserT).filter(dbvo.UserT.userid == userid).update(user_info)
    db.commit()
