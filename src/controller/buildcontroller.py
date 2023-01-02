import sys
import os
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Dict

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)

from service import hokinsservice
from util import responseho, dbconn
from hokinscollect import redis_queue

"""
젠킨스 관련 Controller!!
젠킨스 빌드 및 도커 빌드
그 어떤 것도 그렇지만 호영이 만든 파일
"""

router: APIRouter = APIRouter()
dbconn.db.base.metadata.create_all(bind=dbconn.db.engine)


@router.get("/{projectname}", tags=["build"])
async def createjob(
    projectname: str,
    db: Session = Depends(dbconn.db.session),
) -> JSONResponse:
    if not hokinsservice.confirmRedis(projectname):
        return responseho.errorResponse("already waiting")
    hokinsservice.createpipe(projectname, db)
    # background_tasks.add_task(hokinsservice.createpipe, projectname, db)
    return responseho.successResponse("Good")


@router.get("/exist/{project_name}", tags=["build"])
async def existprojectname(project_name: str) -> int:
    if not hokinsservice.confirmRedis(project_name):
        return responseho.errorResponse("already waiting")
    return responseho.successResponse("Good")


@router.get("/outS", tags=["build"])
async def queuenum() -> int:
    q: redis_queue.RedisQueue = redis_queue.ProceedingQueue
    a: str = q.get()
    q: redis_queue.RedisQueue = redis_queue.WaitingQueue
    b: str = q.get()
    q: redis_queue.RedisQueue = redis_queue.StartQueue
    c: str = q.get()
    return f"ProceedingQueue :{a}, WaitingQueue:{b},StartQueue: {c}"


@router.get("/proceeding_size", tags=["build"])
async def proceeding_size() -> int:
    q: redis_queue.RedisQueue = redis_queue.ProceedingQueue
    return q.size()


@router.get("/waiting_size", tags=["build"])
async def waiting_size() -> int:
    q: redis_queue.RedisQueue = redis_queue.WaitingQueue
    return q.size()


@router.get("/starting_size", tags=["build"])
async def starting_size() -> int:
    q: redis_queue.RedisQueue = redis_queue.StartQueue
    return q.size()


@router.get("/prometheus/{project_name}", tags=["build"])
async def prometheus(project_name) -> Dict[str, bool]:
    """
    젠킨스의 Job으로 생성된 것을 프로메테우스와 그라파나 연결.:

    - **prject_name**:	Jenkins build로 Docker에 배포된 프로젝트 네임
    """
    hokinsservice.prometheusymlupdate(project_name)
    return {"Hoyoung is God": True}


@router.get("/onlygrafana/{project_name}", tags=["build"])
async def onlygrafana(project_name) -> Dict[str, bool]:
    hokinsservice.only_grafana(project_name)
    return {"Hoyoung is God": True}
