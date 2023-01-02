import sys
import os
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)
from constantstore import constant
from vo import dbvo

engine = create_engine(constant.SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(bind=engine)


def findadmin() -> dbvo.UserT:
    session = Session()
    userinfo: dbvo.UserT = session.query(dbvo.UserT).filter(dbvo.UserT.userid == "admin").first()
    session.close()
    return userinfo


def makeadmin():
    if not findadmin():
        session = Session()
        db_user: dbvo.UserT = dbvo.UserT(
            userid="admin",
            username="admin",
            email="admin@hoyoung.com",
            password=constant.PASSWORD_CONTEXT.hash("admin"),
            administer=True,
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
