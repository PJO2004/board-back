from datetime import datetime
from pydantic import BaseModel, constr
import sys
import os

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)
from typing import Optional, List
from vo import dbvo


class Project_class:
    def __init__(
        self,
        individual: int,
        projectname: str,
        userid: str,
        groupname: str,
        giturl: str,
        token: str,
    ):
        self.individual: int = 1 if individual else 0
        self.projectname: str = projectname
        self.userid: str = userid
        self.groupname: str = groupname if individual else None
        self.giturl: str = giturl
        self.token: str = token


class Projectlist:
    def __init__(self, projectname, userid, groupname, giturl, param, reg_dtm):
        self.projectname = projectname
        self.userid: str = "Group - " + groupname if groupname else userid
        self.giturl = giturl
        self.param = param
        self.reg_dtm = reg_dtm


class ProjectImportInsert:
    def __init__(self, projectname, userid, giturl, token):
        self.projectname = projectname
        self.userid = userid
        self.giturl = giturl
        self.token = token


class Project(BaseModel):
    individual: bool = True
    projectname: constr(min_length=5)


class ProjectGithub(BaseModel):
    projectname: str
    individual: bool
    guthubtoken: str
    repo_id: str
    namespace: str

    class Config:
        orm_mode: bool = True


class ProjectBitbucket(BaseModel):
    projectname: str
    individual: bool
    bitbucketurl: str
    bitbucketid: str
    bitbuckettoken: str
    bitbucketproject: str
    bitbucketrepo: str

    class Config:
        orm_mode: bool = True


class Project_Member_Recomend(BaseModel):
    projectname: str
    userid: str

    class Config:
        orm_mode: bool = True


class GetProject(BaseModel):
    projectname: str
    userid: str
    groupname: Optional[str] = None
    reg_dtm: datetime
    giturl: str
    param: Optional[str] = None

    class Config:
        orm_mode: bool = True


class Project_list_view:
    def __init__(self, project_list: List[dbvo.ProjectT]) -> None:
        self.project_list: list = self.trans(project_list)

    def trans(self, project_list: List[dbvo.ProjectT]):
        returnvalue: list = list()
        for projectone in project_list:
            dictparam: dict = dict()
            if projectone.param:
                dictparam = eval(projectone.param)
            data: Projectlist = Projectlist(
                projectname=projectone.projectname,
                userid=projectone.userid,
                groupname=projectone.groupname,
                giturl=projectone.giturl,
                param=dictparam,
                reg_dtm=projectone.reg_dtm,
            )
            returnvalue.append(data)
        return returnvalue
