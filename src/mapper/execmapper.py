import os
import sys
from sqlalchemy import or_, and_, text, case, desc, asc

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)
from vo import execvo
from sqlalchemy.orm import Session
from datetime import datetime
from vo import execvo, dbvo
import commonmapper

starta: str = "st"


def selectalljob(userid: str, db: Session) -> list:
    execinfo: list = db.query(dbvo.ExecT).filter(dbvo.ExecT.userid == userid).all()
    return execinfo


def get_exec_jobid(jobid: str, db: Session) -> dbvo.ExecT:
    jobinfo: dbvo.ExecT = db.query(dbvo.ExecT).filter(dbvo.ExecT.jobid == jobid).first()
    return jobinfo


def startjob(execinfo: execvo.ExecB, userid: str, db: Session) -> dbvo.ExecT:
    db_exec: dbvo.ExecT = dbvo.ExecT(
        jobid=execinfo.jobid,
        userid=userid,
        slotid=execinfo.slotid,
        state=starta,
        param=str(execinfo.param),
        filelist=execinfo.filelist,
    )
    commonmapper.insert_db(db_exec, db)
    return db_exec


# 아직 훨씬 해야함
def updatejob(jobid: str, state: str, db: Session) -> None:
    db.query(dbvo.ExecT).filter(dbvo.ExecT.jobid == jobid).update(
        {"state": state, "deploytime": datetime.now()}
    )
    db.commit()


def get_historyho(userid: str, state: str, starttime: str, endtime: str, db: Session):
    state_case = case(
        [
            (dbvo.ExecT.state == "RC", "데이터 수신"),
            (dbvo.ExecT.state == "RE", "수신 실패"),
            (dbvo.ExecT.state == "PR", "전처리"),
            (dbvo.ExecT.state == "PE", "전처리 실패"),
            (dbvo.ExecT.state == "EX", "처리 중"),
            (dbvo.ExecT.state == "PT", "후처리"),
            (dbvo.ExecT.state == "TE", "후처리 실패"),
            (dbvo.ExecT.state == "CP", "완료"),
            (dbvo.ExecT.state == "ER", "오류"),
            (dbvo.ExecT.state == "SS", "전송 완료"),
            (dbvo.ExecT.state == "SE", "전송 실패"),
        ]
    ).label("state")
    querys = db.query(
        dbvo.ExecT.jobid,
        dbvo.ExecT.slotid,
        dbvo.ExecT.userid,
        state_case,
        dbvo.ExecT.param,
        dbvo.ExecT.result,
        dbvo.ExecT.starttime,
        dbvo.ExecT.endtime,
        dbvo.ExecT.filelist,
    )
    if userid:
        querys = querys.filter(dbvo.ExecT.userid == userid)
    if state:
        querys = querys.filter(dbvo.ExecT.state == state)
    if starttime and endtime:
        querys = querys.filter(dbvo.ExecT.starttime.between(starttime, endtime))
    querys = querys.order_by(dbvo.ExecT.starttime.desc())
    querys = querys.order_by(dbvo.ExecT.jobid.asc())
    return querys.all()


def update_exec_history(data: execvo.Receive, db: Session) -> None:
    db.query(dbvo.ExecT).filter(dbvo.ExecT.jobid == data.jobid).update(
        {
            "param": str(data.param),
            "endtime": data.job_end_date,
            "state": data.state,
            "result": str(data.results),
        }
    )
    db.commit()
