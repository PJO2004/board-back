import os
import sys
from sqlalchemy.orm import Session

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)
from vo import dbvo
from sqlalchemy.sql import func
from constantstore import constant
import commonmapper

def exist_pipe(projectname: str, db: Session) -> dbvo.PipeT:
    return db.query(dbvo.PipeT).filter(dbvo.PipeT.project_name == projectname).first()


def pipe_all(db: Session) -> list:
    return db.query(dbvo.PipeT).filter().all()


def create_pipe(slotinfo: dbvo.SlotT, db: Session):
    db_pipe: dbvo.PipeT = dbvo.PipeT(
        project_name=slotinfo.slotid,
        git_username=slotinfo.userid,
        git_usertoken=slotinfo.token,
        git_ip_s=constant.GIT_IP,
        git_path_with_namespaces=f"{slotinfo.userid}/{slotinfo.slotid}",
        dep_state="no",
    )
    commonmapper.insert_db(db_pipe,db)


def create_exec(project_name: str, db: Session):
    before = (
        db.query(func.max(dbvo.ExecPipeT.num))
        .filter(dbvo.ExecPipeT.project_name == project_name)
        .first()  # <- one에서 first로 바꿈
    )
    maxexec: int = 1
    if before[0]:
        maxexec = before[0] + 1
    db_pipe: dbvo.ExecPipeT = dbvo.ExecPipeT(project_name=project_name, dep_state="st", num=maxexec)
    db.add(db_pipe)
    db.commit()
    db.refresh(db_pipe)
