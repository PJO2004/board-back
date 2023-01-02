import sys
import os
import logging
from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)

from mapper import slotmapper
from vo import slotvo, dbvo
from service import slotservice
from util import responseho, AuthHo, dbconn

"""

슬롯(모델이 실행되는 컨테이너) 관련 Controller!!
그 어떤 것도 그렇지만 호영이 만든 파일

"""
router: APIRouter = APIRouter()
dbconn.db.base.metadata.create_all(bind=dbconn.db.engine)

# 슬롯 생성하기 전, 슬롯 있는지 없는 지 확인하는 것
@router.get("/exist/{slotid}", tags=["slot"])
async def exist_slot(slotid: str, db: Session = Depends(dbconn.db.session)) -> JSONResponse:
    slotinfo: dbvo.SlotT = slotmapper.get_slot(slotid, db)
    if slotinfo:
        return responseho.successResponse("I`m update.", {"result": False})
    else:
        return responseho.successResponse("I`m update.", {"result": True})


# 슬롯 생성
@router.post("/", tags=["slot"])
async def slotcreate(
    slotinfo: slotvo.SlotB,
    db: Session = Depends(dbconn.db.session),
    Authorize: AuthHo.AuthJWT = Depends(),
    userid: str = Depends(AuthHo.require_user),
) -> JSONResponse:
    Authorize.jwt_required()
    if slotservice.slotcreate(slotinfo, userid, db):
        # background_tasks.add_task(slotservice.updateparam, slotinfo, db)
        return responseho.successResponse("I`m update.", {"result": True})
    return responseho.errorResponse("I`m not update.", {"result": False})


# 슬롯 조회하는 곳
@router.get("/", tags=["slot"])
async def slotlist(
    db: Session = Depends(dbconn.db.session),
    Authorize: AuthHo.AuthJWT = Depends(),
    userid: str = Depends(AuthHo.require_user),
) -> JSONResponse:
    Authorize.jwt_required()
    groupname: str = Authorize.get_raw_jwt()["group"]
    lista: list = slotservice.slotlistview(userid, groupname, db)
    if lista:
        json_compatible_item_data = jsonable_encoder(lista)
        return responseho.successResponse("", {"resultlist": json_compatible_item_data})
    return responseho.successResponse("", {"resultlist": None})


# 단일 슬롯 조회 곳
@router.get("/{slotid}", tags=["slot"])
def get_slot(
    slotid: str, Authorize: AuthHo.AuthJWT = Depends(), db: Session = Depends(dbconn.db.session)
) -> dict:
    Authorize.jwt_required()
    return slotservice.get_slot(slotid, db)


# 슬롯 삭제하는 곳
@router.delete("/{slotid}", tags=["slot"])
async def slotdelete(
    slotid: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(dbconn.db.session),
    Authorize: AuthHo.AuthJWT = Depends(),
    userid: str = Depends(AuthHo.require_user),
) -> JSONResponse:
    Authorize.jwt_required()
    slotinfo: dbvo.SlotT = slotmapper.get_slot(slotid, db)
    groupname: str = Authorize.get_raw_jwt()["group"]
    if not slotservice.group_user_checker(slotinfo, userid, groupname):
        return responseho.authfailResponse("who are you?!?!")
    slotservice.slotdelete(slotid, db)
    background_tasks.add_task(slotservice.slotymlremove, slotid)
    return responseho.successResponse("Successfully deleted slot")


@router.put("/", tags=["slot"])
def slotupdate(
    slotupdateinfo: slotvo.SlotUpdateB,
    db: Session = Depends(dbconn.db.session),
    Authorize: AuthHo.AuthJWT = Depends(),
    userid: str = Depends(AuthHo.require_user),
):
    Authorize.jwt_required()
    groupname: str = Authorize.get_raw_jwt()["group"]
    slot_info = slotmapper.get_slot(slotupdateinfo.slotid, db)
    if not slotservice.group_user_checker(slot_info, userid, groupname):
        return responseho.authfailResponse("who are you?!?!")
    try:
        slotservice.slotupdate(slotupdateinfo)
        return responseho.successResponse("successfully update")
    except Exception as e:
        logging.error(str(e))
        return responseho.errorResponse("error updating")


# 슬롯 상태 업데이트하는 곳
# @router.get("/state/{state}/slot/{slotid}", tags=["slot"])
# async def updateprojectstate(
#     state: str, slotid: str, db: Session = Depends(dbconn.db.session)
# ) -> JSONResponse:
#     try:
#         slotmapper.defstateupdate(state, slotid, db)
#         return responseho.successResponse("I`m update.")
#     except Exception as e:
#         return responseho.errorResponse("I`m not update.")


# 슬롯 파라미터 조회하는 곳
@router.get("/paramselect/{slotid}", tags=["slot"])
def paramselect(slotid: str, db: Session = Depends(dbconn.db.session)) -> JSONResponse:
    slot: dbvo.SlotT = slotmapper.get_slot(slotid, db)
    if slot.param:
        json_data = jsonable_encoder(slot.param)
        return responseho.successResponse("have param", {"result": json_data})
    return responseho.successResponse("have not param", {"result": None})


@router.post("/get_all_with_conditions", tags=["slot_admin"])
def get_all_with_conditions(conditions: dict, db: Session = Depends(dbconn.db.session)) -> list:
    return slotmapper.get_all_with_conditions(conditions, db)


@router.post("/get_one_with_conditions", tags=["slot_admin"])
def get_one_with_conditions(conditions: dict, db: Session = Depends(dbconn.db.session)) -> list:
    return slotmapper.get_one_with_conditions(conditions, db)
