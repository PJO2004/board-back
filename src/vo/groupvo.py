from pydantic import BaseModel


class UserGroup(BaseModel):
    ownername: str
    groupname: str


class GroupInfo:
    def __init__(self, ownername: str, groupname: str):
        self.ownername: str = ownername
        self.groupname: str = groupname
        self.token: str = None
