from fastapi import Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
import sys
import os

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)
from service import userservice
from vo import authvo
from constantstore import constant

from util import ErrorHo, dbconn

"""

유저 검사 관련 For JWT Authentication
그 어떤 것도 그렇지만 호영이 만든 파일

"""


@AuthJWT.load_config
def get_config() -> authvo.Settings:
    return authvo.Settings()


def require_user(Authorize: AuthJWT = Depends(), db: Session = Depends(dbconn.db.session)) -> str:
    Authorize.jwt_required()
    userid: str = Authorize.get_jwt_subject()
    if not userservice.get_user(userid, db):
        raise ErrorHo.UserNotFound("User not exist")
    return userid


def compare_password(password, hasedpassword) -> bool:
    return constant.PASSWORD_CONTEXT.verify(password, hasedpassword)
