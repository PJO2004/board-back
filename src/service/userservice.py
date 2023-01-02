import sys
import os
import logging
from sqlalchemy.orm import Session
from typing import Tuple

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)
from vo import uservo, dbvo
from mapper import usermapper
from util import AuthHo, gitlabHo
from constantstore import constant


def get_user(userid: str, db: Session) -> dbvo.UserT:
    user_info: dbvo.UserT = usermapper.get_user(userid, db)
    return user_info


def register_user(user: uservo.UserB, db: Session) -> uservo.UserInfoN:
    user_info: uservo.UserInfoN = uservo.UserInfoN(**user.dict())
    usermapper.create_user(user_info, db)
    return user_info


def login(logininfo: uservo.LoginInfo, db: Session) -> Tuple[bool, dbvo.UserT]:
    user_info_db: dbvo.UserT = usermapper.get_user(logininfo.userid, db)
    if user_info_db:
        return AuthHo.compare_password(logininfo.password, user_info_db.password), user_info_db
    else:
        return False, None


def user_delete(userid: str, db: Session) -> bool:
    try:
        usermapper.user_delete(userid, db)
        gitlabHo.user_delete_gitlab(userid)
        return True
    except Exception as e:
        logging.error(e)
        return False


def register_gitlab(user_info: uservo.UserInfoN, db: Session, have_group: bool = True) -> None:
    try:
        gitlabHo.git_user_create(user_info)
        gitlab_user_token: str = gitlabHo.user_token(user_info.userid)
        user_info.token = gitlab_user_token
        usermapper.user_token_register(user_info, db)
        if not user_info.groupname:
            have_group: bool = False
        if have_group and user_info.userid not in gitlabHo.group_member(user_info):
            gitlabHo.group_add(user_info)
    except Exception as e:
        logging.error(e)


def user_update(userid: str, user_info: dict, db: Session):
    if "password" in user_info:
        user_info["password"] = constant.PASSWORD_CONTEXT.hash(user_info.get("password"))
    usermapper.user_update(userid, user_info, db)
