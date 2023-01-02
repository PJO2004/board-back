import sys
import os
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)

from util.AuthHo import AuthJWT, require_user
from util.dbconn import db
from mapper import execmapper
from vo import execvo, dbvo
from service import execservice
from util import responseho

"""

슬롯 실행 관련 Controller!!
슬롯(모델을 가지고 있는 컨테이너)
팀장님이 개발하신 Anode를 돌리는 틀


그 어떤 것도 그렇지만 호영이 만든 파일

"""
# 프로젝트(모델을 위한 공간!)
router: APIRouter = APIRouter()
db.base.metadata.create_all(bind=db.engine)

# 슬롯을 생성하기 전, 슬롯이 있는지 없는 지 확인하는 것
@router.get("/exists/{jobid}", status_code=status.HTTP_200_OK,tags=["exec"])
def jobidchecker(
    jobid: str, Authorize: AuthJWT = Depends(), db: Session = Depends(db.session)
) -> JSONResponse:
    Authorize.jwt_required()
    exit: dbvo.ExecT = execmapper.get_exec_jobid(jobid, db)
    if exit:
        return responseho.successResponse("project already exists", {"result": False})
    return responseho.successResponse("project not exists", {"result": True})


# 슬롯을 실행하는 것
@router.post("/start",tags=["exec"])
def jobstart(
    execinfo: execvo.ExecB,
    db: Session = Depends(db.session),
    Authorize: AuthJWT = Depends(),
    userid: str = Depends(require_user),
) -> JSONResponse:
    Authorize.jwt_required()
    execservice.startjob(execinfo, userid, db)
    # 여기서 리퀘스트 보냄!
    return responseho.successResponse("good", {"result": True})


# 아직 훨씬 해야함 - 이거말고 콜백으로 받자!
@router.get("/jobid/{jobid}/state/{state}",tags=["exec"])
def jobupdate(jobid: str, state: str, db: Session = Depends(db.session)) -> JSONResponse:
    execmapper.updatejob(jobid, state, db)
    return responseho.successResponse("Success")


# 모든 슬롯을 조회하는 것
@router.get("/selectall",tags=["exec"])
def selectexec(
    Authorize: AuthJWT = Depends(),
    userid: str = Depends(require_user),
    db: Session = Depends(db.session),
) -> list:
    Authorize.jwt_required()
    returnlist: list = execmapper.selectalljob(userid, db)
    if returnlist:
        return responseho.successResponse("Success", {"result": jsonable_encoder(returnlist)})
    return responseho.successResponse("Fail", {"result": None})


# 슬롯의 결과를 콜백 받는 곳
@router.post("/callback",tags=["exec"])
def exec_callback(data: execvo.Receive, db: Session = Depends(db.session)) -> JSONResponse:
    """
    슬롯의 결과를 콜백 받는 곳:
    """
    execservice.update_exec_history(data, db)
    return JSONResponse(
        status_code=200, content={"msssage": "Callback process has completed", "data": data}
    )


# 실행 이력을 조회하는 곳
@router.get("/history",tags=["exec"])
def get_history(
    userid: str = None,
    state: str = None,
    starttime: str = None,
    endtime: str = None,
    db: Session = Depends(db.session),
    Authorize: AuthJWT = Depends(),
) -> list:
    """
    실행 이력을 조회하는 곳:
    """
    return execmapper.get_historyho(userid, state, starttime, endtime, db)
