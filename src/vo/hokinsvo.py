from pydantic import BaseModel


class RequestB(BaseModel):
    project_name: str
    git_username: str
    git_usertoken: str
    git_ip_s: str
    git_path_with_namespaces: str

    class Config:
        orm_mode: bool = True
