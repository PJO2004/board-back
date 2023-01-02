import sys
import os
from sqlalchemy.orm import Session
from util import gitlabHo

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)
from vo import groupvo
from mapper import groupmapper


def get_group(groupname: str, db: Session):
    exist = groupmapper.get_group(groupname, db)
    return exist


def register_group(usergroup: groupvo.UserGroup, db: Session):
    groupmapper.register_group(usergroup, db)
    return usergroup


def register_gitlab_group(usergroup: groupvo.UserGroup, db: Session) -> None:
    gitlabHo.group_create(usergroup)
    group_info = groupvo.GroupInfo(**usergroup.dict())
    gitlab_group_token: str = gitlabHo.group_token(group_info)
    group_info.token = gitlab_group_token
    groupmapper.group_token_register(group_info, db)
