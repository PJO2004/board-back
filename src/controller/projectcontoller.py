import sys
import os
import json
import requests
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, status, BackgroundTasks, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from fastapi.encoders import jsonable_encoder

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)
from util.AuthHo import AuthJWT, require_user
from vo import projectvo, dbvo
from service import projectservice
from util.dbconn import db
from mapper import projectmapper, usermapper, groupmapper
from util import responseho, gitlabHo
from constantstore import constant

"""

모델 프로젝트 생성 관련 Controller!!
모델(사용자가 개발한 모델을 올리는 곳)

그 어떤 것도 그렇지만 호영이 만든 파일

"""
# 프로젝트(모델을 위한 공간!)
router: APIRouter = APIRouter()
db.base.metadata.create_all(bind=db.engine)

# 프로젝트 존재 유무 확인
@router.get("/exists/{projectname}", status_code=status.HTTP_200_OK, tags=["project"])
def projectChecker(projectname: str, db: Session = Depends(db.session)) -> JSONResponse:
    exit = projectmapper.get_project(projectname, db)
    if exit:
        return responseho.successResponse("project already exists", {"result": False})
    return responseho.successResponse("project not exists", {"result": True})


# 프로젝트 파라미터 조회하는 곳
@router.get("/paramselect/{projectname}", tags=["project"])
def paramselect(projectname: str, db: Session = Depends(db.session)) -> JSONResponse:
    project: dbvo.ProjectT = projectmapper.paramselect(projectname, db)
    if project.param:
        json_data = jsonable_encoder(project.param)
        return responseho.successResponse("parameter have", {"result": json_data})
    return responseho.successResponse("parameter have not", {"result": None})


# 단일 프로젝트 조회
@router.get(
    "/{projectname}",
    status_code=status.HTTP_200_OK,
    tags=["project"],
)
def get_project(projectname: str, db: Session = Depends(db.session)) -> JSONResponse:
    project_info = projectmapper.get_project(projectname, db)
    project_info.__delattr__("token")
    return project_info


# 프로젝트 삭제
@router.delete("/delete/{projectname}", tags=["project"])
async def projectdelete(
    projectname: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(db.session),
    Authorize: AuthJWT = Depends(),
    userid: str = Depends(require_user),
) -> JSONResponse:
    Authorize.jwt_required()
    projectinfo: dbvo.ProjectT = projectmapper.get_project(projectname, db)
    if projectinfo.userid != userid:
        return responseho.authfailResponse("who are you?")
    projectmapper.projectdelete(projectname, userid, db)
    background_tasks.add_task(projectservice.projectymlremove, projectname)
    return responseho.successResponse("Successfully deleted slot")


# 프로젝트 생성
@router.post("/", status_code=status.HTTP_200_OK, tags=["project"])
def createProject(
    project: projectvo.Project,
    Authorize: AuthJWT = Depends(),
    userid: str = Depends(require_user),
    db: Session = Depends(db.session),
) -> JSONResponse:
    Authorize.jwt_required()
    if projectservice.get_project(project.projectname, db):
        return responseho.errorResponse("project already exists.")
    groupname: str = Authorize.get_raw_jwt()["group"]
    success: bool = projectservice.projectCreate(project, userid, groupname, db)
    if success:
        return responseho.successResponse("created successfully", {"result": True})
    return responseho.successResponse("project not created", {"result": False})


@router.post("/project_only_file", status_code=status.HTTP_200_OK, tags=["project"])
def onlyfile(
    project: projectvo.Project,
    db: Session = Depends(db.session),
    file_list: List[UploadFile] = File(...),
    Authorize: AuthJWT = Depends(),
    userid: str = Depends(require_user),
) -> JSONResponse:
    Authorize.jwt_required()
    groupname: str = Authorize.get_raw_jwt()["group"]
    try:
        gitlaburl: str = projectservice.onlyfile(project, userid, groupname, db, file_list)
        return responseho.successResponse("project created", {"giturl": gitlaburl})
    except Exception as e:
        return responseho.successResponse("project not created", {"giturl": None})


@router.post("/project_only_gitlab", status_code=status.HTTP_200_OK, tags=["project"])
def onlygitlab(
    project: projectvo.Project,
    Authorize: AuthJWT = Depends(),
    userid: str = Depends(require_user),
) -> JSONResponse:
    Authorize.jwt_required()
    groupname: str = Authorize.get_raw_jwt()["group"]
    try:
        if project.individual:
            gitlabHo.gitlab_project_create(userid, project.projectname)
        else:
            gitlabHo.gitlab_group_project(groupname, project.projectname)
        name_space: str = gitlabHo.get_path_with_namespaces(project.projectname)
        gitlaburl: str = f"{constant.HTTP}{constant.GITLAB_IP}/{name_space}"
        return responseho.successResponse("project created", {"giturl": gitlaburl})
    except Exception as e:
        return responseho.errorResponse("project not created", {"giturl": None})


@router.post("/project_only_github", status_code=status.HTTP_200_OK, tags=["project"])
def onlygithub(
    importproject: projectvo.ProjectGithub,
    db: Session = Depends(db.session),
    Authorize: AuthJWT = Depends(),
    userid: str = Depends(require_user),
) -> JSONResponse:
    Authorize.jwt_required()
    groupname: str = Authorize.get_raw_jwt()["group"]
    response, gitlaburl = onlygithub(importproject, userid, groupname, db)
    if response.status_code == 201 or response.status_code == 200:
        return responseho.successResponse("Successfully Import", {"giturl": gitlaburl})
    return responseho.errorResponse("Import Failed", {"giturl": None})


@router.post("/project_only_bitbucket", status_code=status.HTTP_200_OK, tags=["project"])
def onlybitbucket(
    importproject: projectvo.ProjectBitbucket,
    Authorize: AuthJWT = Depends(),
    userid: str = Depends(require_user),
    db: Session = Depends(db.session),
) -> JSONResponse:
    Authorize.jwt_required()
    groupname: str = Authorize.get_raw_jwt()["group"]
    response, gitlaburl = onlybitbucket(importproject, userid, groupname, db)
    if response.status_code == 201 or response.status_code == 200:
        return responseho.successResponse("Successfully Import", {"giturl": gitlaburl})
    return responseho.errorResponse("Import Failed", {"giturl": gitlaburl})


@router.post("/project_insert", status_code=status.HTTP_200_OK, tags=["project"])
def onlyinsert(
    project: projectvo.Project,
    Authorize: AuthJWT = Depends(),
    userid: str = Depends(require_user),
    db: Session = Depends(db.session),
) -> JSONResponse:
    Authorize.jwt_required()
    groupname: str = Authorize.get_raw_jwt()["group"]
    success, error = projectservice.projectonlyinsert(project, userid, groupname, db)
    if success:
        return responseho.successResponse("created successfully", {"result": True})
    return responseho.successResponse("project not created", {"result": error})


# DB를 통해서 전체 프로젝트 조회
@router.get("/project_totals", status_code=status.HTTP_200_OK, tags=["project"])
def project_total_views(
    Authorize: AuthJWT = Depends(),
    userid: str = Depends(require_user),
    db: Session = Depends(db.session),
) -> JSONResponse:
    Authorize.jwt_required()
    groupname: str = Authorize.get_raw_jwt()["group"]
    lista: list = projectservice.project_list_view(userid, groupname, db)
    if lista:
        json_compatible_item_data = jsonable_encoder(lista)
        return responseho.successResponse(
            "Successfully slot", {"resultlist": json_compatible_item_data}
        )
    return responseho.successResponse("Successfully slot", {"resultlist": None})


# GITLAB API 전체 프로젝트 조회
@router.get("/project_total", status_code=status.HTTP_200_OK, tags=["project"])
def project_total_view(Authorize: AuthJWT = Depends(), userid: str = Depends(require_user)) -> dict:
    Authorize.jwt_required()
    groupname: str = Authorize.get_raw_jwt()["group"]
    total_project_list: list = [one.path for one in gitlabHo.project_total_list(userid, groupname)]
    return {"project": total_project_list}


# GITLAB API 개인 프로젝트 조회
@router.get("/project_user", status_code=status.HTTP_200_OK, tags=["project"])
def project_user_view(Authorize: AuthJWT = Depends(), userid: str = Depends(require_user)) -> dict:
    Authorize.jwt_required()
    user_project_list: list = [one.path for one in gitlabHo.project_user_list(userid)]
    return {"project": user_project_list}


# GITLAB API 그룹 프로젝트 조회
@router.get("/project_group", status_code=status.HTTP_200_OK, tags=["project"])
def project_group_view(Authorize: AuthJWT = Depends(), userid: str = Depends(require_user)) -> dict:
    Authorize.jwt_required()
    groupname: str = Authorize.get_raw_jwt()["group"]
    group_project_list: list = [one.path for one in gitlabHo.project_group_list(groupname)]
    return {"project": group_project_list}


# 프로젝트에 멤버를 추가하는 곳
@router.post("/project_add_member", status_code=status.HTTP_200_OK, tags=["project"])
def project_add_member(
    projectaddmember: projectvo.Project_Member_Recomend,
    Authorize: AuthJWT = Depends(),
    userid: str = Depends(require_user),
) -> JSONResponse:
    Authorize.jwt_required()
    if projectservice.project_add_member(projectaddmember, userid):
        return responseho.successResponse("member added successfully")
    return responseho.errorResponse("member add failed")


# Github Insert
@router.post("/importgithub", status_code=status.HTTP_200_OK, tags=["project"])
def projectimport_github(
    importproject: projectvo.ProjectGithub,
    background_tasks: BackgroundTasks,
    Authorize: AuthJWT = Depends(),
    userid: str = Depends(require_user),
    db: Session = Depends(db.session),
) -> JSONResponse:
    Authorize.jwt_required()
    creator_info = None
    groupname: str = Authorize.get_raw_jwt()["group"]
    if importproject.individual:
        creator_info: dbvo.UserT = usermapper.get_user(userid, db)
    else:
        creator_info: dbvo.GroupT = groupmapper.get_group(groupname, db)
    headers: dict = {"CONTENT-TYPE": "application/json", "PRIVATE-TOKEN": creator_info.token}
    data: dict = {
        "personal_access_token": importproject.guthubtoken,
        "repo_id": importproject.repo_id,
        "target_namespace": importproject.namespace,
        "new_name": importproject.projectname,
    }
    response = requests.request(
        "POST",
        url=f"http://{constant.GITLAB_IP_S}/api/v4/import/github",
        headers=headers,
        data=json.dumps(data),
    )
    if response.status_code == 201 or response.status_code == 200:
        project_info = projectvo.ProjectImportInsert(
            projectname=importproject.projectname,
            userid=userid,
            giturl=constant.GITLAB_IP_S,
            token=creator_info.token,
        )
        background_tasks.add_task(projectservice.projectImport, project_info, groupname, db)
        return responseho.successResponse("Successfully Import")
    return responseho.errorResponse("Import Failed")


# Bitbucket Insert
@router.post("/importbitbucket", status_code=status.HTTP_200_OK, tags=["project"])
def projectimport_bitbucket(
    importproject: projectvo.ProjectBitbucket,
    background_tasks: BackgroundTasks,
    Authorize: AuthJWT = Depends(),
    userid: str = Depends(require_user),
    db: Session = Depends(db.session),
) -> JSONResponse:
    Authorize.jwt_required()
    creator_info = None
    groupname: str = Authorize.get_raw_jwt()["group"]
    if importproject.individual:
        creator_info: dbvo.UserT = usermapper.get_user(userid, db)
    else:
        creator_info: dbvo.GroupT = groupmapper.get_group(groupname, db)
    headers: dict = {"CONTENT-TYPE": "application/json", "PRIVATE-TOKEN": creator_info.token}
    data: dict = {
        "bitbucket_server_url": importproject.bitbucketurl,
        "bitbucket_server_username": importproject.bitbucketid,
        "personal_access_token": importproject.bitbuckettoken,
        "bitbucket_server_project": importproject.bitbucketproject,
        "bitbucket_server_repo": importproject.bitbucketrepo,
        "new_name": importproject.projectname,
    }
    response = requests.post(
        url=f"http://{constant.GITLAB_IP_S}/api/v4/import/bitbucket_server",
        headers=headers,
        data=json.dumps(data),
    )
    if response.status_code == 201 or response.status_code == 200:
        project_info = projectvo.ProjectImportInsert(
            projectname=importproject.projectname,
            userid=userid,
            giturl=constant.GITLAB_IP_S,
            token=creator_info.token,
        )
        background_tasks.add_task(projectservice.projectImport, project_info, groupname, db)
        return responseho.successResponse("Successfully Import")
    return responseho.errorResponse("Import Failed")


@router.get("/source_check/{projectname}", tags=["project"])
def git_source_check(
    projectname: str,
    Authorize: AuthJWT = Depends(),
    userid: str = Depends(require_user),
    db: Session = Depends(db.session),
):
    Authorize.jwt_required()
    project_info: dbvo.ProjectT = projectmapper.get_project(projectname, db)
    if not project_info:
        return responseho.errorResponse("no have project")
    return projectservice.source_check(projectname, project_info.token)


@router.post("/get_all_with_conditions", tags=["project_admin"])
def get_all_with_conditions(conditions: dict, db: Session = Depends(db.session)):
    return projectmapper.get_all_with_conditions(conditions, db)


@router.post("/get_one_with_conditions", tags=["project_admin"])
def get_one_with_conditions(conditions: dict, db: Session = Depends(db.session)):
    return projectmapper.get_one_with_conditions(conditions, db)
