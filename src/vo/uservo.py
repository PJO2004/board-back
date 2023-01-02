import sys
import os
from pydantic import BaseModel, constr, EmailStr
from typing import Optional

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)
from constantstore import constant


class UserB(BaseModel):
    userid: str
    username: str
    password: constr(min_length=8)
    email: EmailStr
    groupname: Optional[str] = None

    class Config:
        orm_mode: bool = True


class LoginInfo(BaseModel):
    userid: str
    password: str


class UserInfoN:
    def __init__(self, userid: str, username: str, password: str, email: str, groupname: str):
        self.userid: str = userid
        self.username: str = username
        self.password: str = password
        self.email: str = email
        self.groupname: str = groupname
        self.hashedpassword: str = self.hashpasswords(self.password)
        self.token: str = None

    def hashpasswords(self, password) -> str:
        return constant.PASSWORD_CONTEXT.hash(password)
