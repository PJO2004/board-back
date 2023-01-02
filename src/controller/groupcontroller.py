import sys
import os
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.encoders import jsonable_encoder

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)
from vo import groupvo, dbvo
from service import userservice, groupservice
from mapper import groupmapper, usermapper
from util import gitlabHo, responseho, dbconn, AuthHo

"""

그룹(팀) 관련 Controller!!
그룹을 생성하고 추가하며, GITLAB에 추가하는 것

그 어떤 것도 그렇지만 호영이 만든 파일

"""
router: APIRouter = APIRouter()

dbconn.db.base.metadata.create_all(bind=dbconn.db.engine)


@router.get("/exist/{groupname}", tags=["group"])
async def exist_group(groupname: str, db: Session = Depends(dbconn.db.session)) -> JSONResponse:
    if groupservice.get_group(groupname, db):
        return responseho.successResponse("", {"exit": True})
    else:
        return responseho.successResponse("", {"exit": False})


# 유저용 조회
@router.get("/", tags=["group"])
async def allgroup(db: Session = Depends(dbconn.db.session)) -> JSONResponse:
    grouplist: list = groupmapper.grouplist(db)
    if grouplist:
        json_data = jsonable_encoder(grouplist)
        return responseho.successResponse("", {"exit": "True", "result": json_data})
    return responseho.successResponse("", {"exit": "False", "result": None})


# 유저용 조회
@router.get("/{groupname}", tags=["group"])
async def allgroup(groupname: str, db: Session = Depends(dbconn.db.session)) -> JSONResponse:
    if group_info := groupservice.get_group(groupname, db):
        group_info.__delattr__("token")
        return group_info
    return None


# 어드민용 조회
@router.get("/all", tags=["group_admin"])
async def allgroup(db: Session = Depends(dbconn.db.session)) -> JSONResponse:
    grouplist: list = groupmapper.allgroup(db)
    if grouplist:
        json_data = jsonable_encoder(grouplist)
        return responseho.successResponse("", {"exit": "True", "result": json_data})
    return responseho.successResponse("", {"exit": "False", "result": None})


@router.delete("/{groupname}", tags=["group"])
async def deletegroup(
    groupname: str,
    Authorize: AuthHo.AuthJWT = Depends(),
    userid: str = Depends(AuthHo.require_user),
    db: Session = Depends(dbconn.db.session),
) -> JSONResponse:
    Authorize.jwt_required()
    groupinfo: dbvo.GroupT = groupmapper.get_group(groupname, db)
    userinfo: dbvo.UserT = usermapper.get_user(userid, db)
    if groupinfo.ownername == userid or userinfo.administer:
        groupmapper.deletegroup(groupname, db)
        gitlabHo.group_delete(groupname)
        return responseho.successResponse("", {"result": True})
    return responseho.successResponse("", {"result": False})


@router.post("/", tags=["group"])
async def register_group(
    usergroup: groupvo.UserGroup,
    background_tasks: BackgroundTasks,
    db: Session = Depends(dbconn.db.session),
) -> JSONResponse:
    try:
        groupservice.register_group(usergroup, db)
        background_tasks.add_task(groupservice.register_gitlab_group, usergroup, db)
        return responseho.successResponse("created successfully")
    except Exception as e:
        return responseho.errorResponse(str(e))


# 누가 가입해줌
@router.post("/groupadd", status_code=status.HTTP_200_OK, tags=["group"])
def groupadd(
    user_group: groupvo.UserGroup,
    Authorize: AuthHo.AuthJWT = Depends(),
    userid: str = Depends(AuthHo.require_user),
    db: Session = Depends(dbconn.db.session),
) -> JSONResponse:
    Authorize.jwt_required()
    user: dbvo.UserT = userservice.get_user(userid, db)
    if user:
        if user.groupname == user_group.groupname:
            groupmapper.add_group_member(user_group, db)
            gitlabHo.group_addw(user_group)
            return responseho.successResponse("sucessfully added")
        else:
            return responseho.authfailResponse("user are not group member")
    return responseho.errorResponse("user not found")


# 자기가 가입
@router.get("/joingroup/{groupname}", status_code=status.HTTP_200_OK, tags=["group"])
def joingroup(
    groupname: str,
    Authorize: AuthHo.AuthJWT = Depends(),
    userid: str = Depends(AuthHo.require_user),
    db: Session = Depends(dbconn.db.session),
) -> JSONResponse:
    Authorize.jwt_required()
    user: dbvo.UserT = userservice.get_user(userid, db)
    if user:
        if user.groupname:
            return responseho.errorResponse("Already have group")
        else:
            groupmapper.joingroup(userid, groupname, db)
            gitlabHo.group_add_str(userid, groupname)
            return responseho.successResponse("sucessfully added")
    return responseho.errorResponse("User not found")


@router.post("/get_all_with_conditions", tags=["group_admin"])
def get_all_with_conditions(conditions: dict, db: Session = Depends(dbconn.db.session)) -> list:
    return groupmapper.get_all_with_conditions(conditions, db)


@router.post("/get_one_with_conditions", tags=["group_admin"])
def get_one_with_conditions(conditions: dict, db: Session = Depends(dbconn.db.session)) -> list:
    return groupmapper.get_one_with_conditions(conditions, db)
