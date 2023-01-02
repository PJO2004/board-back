import os
import sys
from sqlalchemy.orm import Session

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)
from mapper import execmapper
from vo import execvo


def startjob(execinfo: execvo.ExecB, userid: str, db: Session) -> None:
    execmapper.startjob(execinfo, userid, db)


def update_exec_history(data: execvo.Receive, db: Session) -> None:
    execmapper.update_exec_history(data, db)
