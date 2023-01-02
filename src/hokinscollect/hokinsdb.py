from sqlalchemy import create_engine, and_
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
import sys
import os

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)

from vo import dbvo
from constantstore import constant

engine = create_engine(constant.SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(bind=engine)


def gitfound(projectname) -> dbvo.PipeT:
    session = Session()
    pipeinfo: dbvo.PipeT = (
        session.query(dbvo.PipeT).filter(dbvo.PipeT.project_name == projectname).first()
    )
    session.close()
    return pipeinfo


def presentbuilder(projectname) -> int:
    session = Session()
    before:list[int] = (
        session.query(func.max(dbvo.ExecPipeT.num))
        .filter(dbvo.ExecPipeT.project_name == projectname)
        .first()
    )
    session.close()
    return before[0]


def errorinsert(projectname, buildnum, error):
    session = Session()
    session.query(dbvo.ExecPipeT).filter(
        and_(dbvo.ExecPipeT.project_name == projectname, dbvo.ExecPipeT.num == buildnum)
    ).update({"dep_state": "er", "error_cause": error})
    session.commit()
    session.close()


def successinsert(projectname, buildnum):
    session = Session()
    session.query(dbvo.ExecPipeT).filter(
        and_(dbvo.ExecPipeT.project_name == projectname, dbvo.ExecPipeT.num == buildnum)
    ).update({"dep_state": "su"})
    session.commit()
    session.close()
