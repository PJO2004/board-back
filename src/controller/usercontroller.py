import sys
import os
import logging
from sqlalchemy.orm import Session
from fastapi import APIRouter, BackgroundTasks, Depends, Response, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import timedelta

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)
from vo import uservo, dbvo
from service import userservice
from util.dbconn import db
from config.envconfig import setting
from util.AuthHo import AuthJWT, require_user
from mapper import usermapper
from util import responseho

"""

유저 관련 Controller!!
그 어떤 것도 그렇지만 호영이 만든 파일

"""
router: APIRouter = APIRouter()

db.base.metadata.create_all(bind=db.engine)
ACCESS_TOKEN_EXPIRES_IN: int = setting.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN: int = setting.REFRESH_TOKEN_EXPIRES_IN

# 유저 생성하기 전, 유저 있는지 없는 지 확인하는 것
@router.get("/exist/{userid}", tags=["user"])
async def exist_user(userid: str, db: Session = Depends(db.session)) -> JSONResponse:
    if userservice.get_user(userid, db):
        return responseho.successResponse("", {"exit": True})
    else:
        return responseho.successResponse("", {"exit": False})


@router.get("/{userid}", tags=["user"])
async def get_user(userid: str, db: Session = Depends(db.session)) -> JSONResponse:
    if user_info := userservice.get_user(userid, db):
        user_info.__delattr__("password")
        user_info.__delattr__("token")
        return user_info
    return None


# 유저 등록하는 것
@router.post("/", tags=["user"])
async def register_user(
    user: uservo.UserB, background_tasks: BackgroundTasks, db: Session = Depends(db.session)
) -> JSONResponse:
    try:
        user_info: uservo.UserInfoN = userservice.register_user(user, db)
        background_tasks.add_task(userservice.register_gitlab, user_info, db)
        return responseho.successResponse("created successfully")
    except Exception as e:
        return responseho.errorResponse(str(e))


# 유저 삭제
@router.delete("/{duserid}", status_code=status.HTTP_200_OK, tags=["user"])
def userdeleter(
    duserid: str,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(db.session),
    userid: str = Depends(require_user),
) -> JSONResponse:
    Authorize.jwt_required()
    userinfo: dbvo.UserT = usermapper.get_user(userid, db)
    if duserid == userid or userinfo.administer:
        if userservice.user_delete(userid, db):
            return responseho.successResponse("user delete successfully.")
    return responseho.errorResponse("user delete failed.")


@router.put("/", tags=["user"])
def user_update(
    user_info: dict,
    Authorize: AuthJWT = Depends(),
    userid: str = Depends(require_user),
    db: Session = Depends(db.session),
) -> JSONResponse:
    Authorize.jwt_required()
    if user_info:
        if "userid" in user_info:
            return responseho.errorResponse("userid can`t change")
        userservice.user_update(userid, user_info, db)
        return responseho.successResponse("Succeesfully grant admin.")
    return responseho.errorResponse("You should insert data")


# 유저 로그인 하는 것
@router.post("/login", tags=["user"])
async def login(
    logininfo: uservo.LoginInfo,
    response: Response,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(db.session),
) -> JSONResponse:
    userCorrect, user_info = userservice.login(logininfo, db)
    if not user_info:
        return responseho.errorResponse("user가 존재하지 않습니다.")
    if not userCorrect or not user_info:
        return responseho.errorResponse("username 과 password가 잘못되었습니다.")
    another_claims: dict = {"group": None}
    if user_info.groupname:
        another_claims["group"] = user_info.groupname
    access_token: str = Authorize.create_access_token(
        subject=str(logininfo.userid),
        user_claims=another_claims,
        expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN),
        fresh=True,
    )
    refresh_token: str = Authorize.create_refresh_token(
        subject=str(logininfo.userid),
        user_claims=another_claims,
        expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN),
    )

    response.set_cookie(
        "access_token",
        access_token,
        ACCESS_TOKEN_EXPIRES_IN * 60,
        ACCESS_TOKEN_EXPIRES_IN * 60,
        "/",
        None,
        False,
        True,
        "lax",
    )
    response.set_cookie(
        "refresh_token",
        refresh_token,
        REFRESH_TOKEN_EXPIRES_IN * 60,
        REFRESH_TOKEN_EXPIRES_IN * 60,
        "/",
        None,
        False,
        True,
        "lax",
    )
    response.set_cookie(
        "logged_in",
        "True",
        ACCESS_TOKEN_EXPIRES_IN * 60,
        ACCESS_TOKEN_EXPIRES_IN * 60,
        "/",
        None,
        False,
        False,
        "lax",
    )
    response.headers["access_token"] = access_token
    response.headers["refresh_token"] = refresh_token
    return {"status": "success", "access_token": access_token, "logged_in": True}


# 유저 로그인을 통해 Refresh Token을 관리하는 곳
@router.get("/refresh", tags=["user"])
def refresh_token(
    response: Response,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(db.session),
) -> JSONResponse:
    Authorize.jwt_refresh_token_required()
    userid: str = Authorize.get_jwt_subject()
    if not userid:
        return responseho.errorResponse("refresh token을 가지고 있지 않습니다.")
    user_info: dbvo.UserT = userservice.get_user(userid, db)
    if not user_info:
        return responseho.errorResponse("refresh token이 잘못된 정보를 가지고 있습니다.")
    another_claims: dict = {"group": None}
    if user_info.groupname:
        another_claims["group"] = user_info.groupname
    access_token: str = Authorize.create_access_token(
        subject=str(userid),
        user_claims=another_claims,
        expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN),
    )
    response.set_cookie(
        "access_token",
        access_token,
        ACCESS_TOKEN_EXPIRES_IN * 60,
        ACCESS_TOKEN_EXPIRES_IN * 60,
        "/",
        None,
        False,
        True,
        "lax",
    )
    response.set_cookie(
        "logged_in",
        "True",
        ACCESS_TOKEN_EXPIRES_IN * 60,
        ACCESS_TOKEN_EXPIRES_IN * 60,
        "/",
        None,
        False,
        False,
        "lax",
    )
    return {"status": "success", "access_token": access_token, "logged_in": True}


# 유저 로그아웃
@router.get("/logout", status_code=status.HTTP_200_OK, tags=["user"])
def logout(
    response: Response, Authorize: AuthJWT = Depends(), userid: str = Depends(require_user)
) -> dict:
    Authorize.unset_jwt_cookies()
    response.set_cookie("logged_in", "", -1)
    logging.info(f"user {userid} is logout")
    return {"status": "success"}


@router.post("/get_all_with_conditions", tags=["user_admin"])
def get_all_with_conditions(conditions: dict, db: Session = Depends(db.session)) -> list:
    return usermapper.get_all_with_conditions(conditions, db)


@router.post("/get_one_with_conditions", tags=["user_admin"])
def get_one_with_conditions(conditions: dict, db: Session = Depends(db.session)) -> list:
    return usermapper.get_one_with_conditions(conditions, db)


# 모든 유저를 조회하는 곳
@router.get("/selectallusers", tags=["user_admin"])
def selectallusers(
    Authorize: AuthJWT = Depends(),
    userid: str = Depends(require_user),
    db: Session = Depends(db.session),
) -> JSONResponse:
    Authorize.jwt_required()
    userinfo: dbvo.UserT = usermapper.get_user(userid, db)
    if not userinfo.administer:
        return JSONResponse(
            status_code=401,
            content={"message": "You do not have permission."},
        )
    userdblist: list = usermapper.selectallusers(db)
    json_compatible_item_data = jsonable_encoder(userdblist)
    return responseho.successResponse("", {"result": json_compatible_item_data})


# 유저에게 어드민 권한을 주는 곳
@router.get("/grantadmin/{admineduser}", tags=["user_admin"])
def grantadmin(
    admineduser: str,
    Authorize: AuthJWT = Depends(),
    userid: str = Depends(require_user),
    db: Session = Depends(db.session),
) -> JSONResponse:
    Authorize.jwt_required()
    userinfo: dbvo.UserT = usermapper.get_user(userid, db)
    if not userinfo.administer:
        return responseho.authfailResponse("You do not have permission.")
    usermapper.grantforadmin(admineduser, db)
    return responseho.successResponse("Succeesfully grant admin.")
