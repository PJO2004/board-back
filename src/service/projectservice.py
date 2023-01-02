import os
import sys
import requests
import json
import logging
from sqlalchemy.orm import Session
from fastapi import UploadFile, File
from typing import List

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)
from vo import projectvo, uservo, dbvo
from util import gitlabHo, fileHo
from constantstore import constant
from mapper import usermapper, groupmapper, projectmapper


def get_project(projectname, db: Session):
    return projectmapper.get_project(projectname, db)


def projectonlyinsert(project: projectvo.Project, userid: str, groupname: str, db: Session):
    try:
        token: str = None
        if project.individual:
            userinfo: dbvo.UserT = usermapper.get_user(userid, db)
            token = userinfo.token
        else:
            groupinfo: dbvo.GroupT = groupmapper.get_group(groupname, db)
            token = groupinfo.token
        name_space: str = gitlabHo.get_path_with_namespaces(project.projectname)
        gitlaburl: str = f"{constant.HTTP}{constant.GITLAB_IP}/{name_space}"
        project_info: projectvo.Project_class = projectvo.Project_class(
            **project.dict(), userid=userid, groupname=groupname, giturl=gitlaburl, token=token
        )
        projectmapper.projectCreate(project_info, db)
        return True, None
    except Exception as e:
        logging.info(str(e))
        return False, str(e)


def projectCreate(project: projectvo.Project, userid, groupname, db: Session):
    try:
        token: str = None
        if project.individual:
            userinfo: dbvo.UserT = usermapper.get_user(userid, db)
            token = userinfo.token
            gitlabHo.gitlab_project_create(userid, project.projectname)
        else:
            groupinfo: dbvo.GroupT = groupmapper.get_group(groupname, db)
            token = groupinfo.token
            gitlabHo.gitlab_group_project(groupname, project.projectname)
        name_space: str = gitlabHo.get_path_with_namespaces(project.projectname)
        gitlaburl: str = f"{constant.HTTP}{constant.GITLAB_IP}/{name_space}"  # constant.HTTP + constant.GITLAB_IP + "/" + name_space
        project_info: projectvo.Project_class = projectvo.Project_class(
            **project.dict(), userid=userid, groupname=groupname, giturl=gitlaburl, token=token
        )
        projectmapper.projectCreate(project_info, db)
        return True
    except Exception as e:
        logging.info(str(e))
        return False


def project_add_member(project_add_member: projectvo.Project_Member_Recomend, userid) -> bool:
    if gitlabHo.project_member_confirm(project_add_member.projectname, userid):
        gitlabHo.project_member_add(project_add_member.projectname, project_add_member.userid)
        return True
    return False


def project_list_view(username: str, groupname: str, db: Session) -> list:
    returnvalue: list = list()
    if groupname:
        returnvalue: list = projectmapper.project_select_with_group(username, groupname, db)
    else:
        returnvalue: list = projectmapper.project_select_only(username, db)
    return projectvo.Project_list_view(returnvalue).project_list


def projectymlremove(projectname: str):
    root_path: str = constant.DATA_PATH
    ymlpath: str = os.path.join(root_path, f"/yaml/param_{projectname}.yml")
    if os.path.exists(ymlpath):
        os.remove(ymlpath)


def get_project(projectname: str, db: Session):
    return projectmapper.get_project(projectname, db)


def projectImport(project_info: projectvo.ProjectImportInsert, groupname: str, db: Session):
    projectmapper.projectImport(project_info, groupname, db)


def has_key(hodict: dict, keyname: str) -> bool:
    if keyname in hodict.keys():
        return True
    return False


def source_check(projectname: str, token: str) -> dict:
    name_space: str = gitlabHo.get_path_with_namespaces(projectname)
    name: str = name_space.split("/")[0]
    URL: str = f"{constant.GITLAB_URL}/api/v4/projects/{name}%2F{projectname}"
    headers: dict = {"Authorization": f"Bearer {token}"}
    response: requests.Response = requests.get(URL, headers=headers)
    response_dict: dict = response.json()
    response_json: dict = {"empty_repo": None}
    if has_key(response_dict, "empty_repo"):
        response_json: dict = {"empty_repo": response_dict["empty_repo"]}
    return response_json


def onlyfile(
    project: projectvo.Project,
    userid: str,
    groupname: str,
    db: Session,
    file_list: List[UploadFile] = File(...),
):
    file_location: str = "/".join([constant.FILE_PATH, userid, project.projectname])
    os.makedirs(file_location)
    if len(file_list) > 1:
        for fileone in file_list:
            fileHo.filesaver(file_location, fileone)
    else:
        fileone: UploadFile = file_list[0]
        fileHo.filesaver(file_location, fileone)
        if file_list[0].filename.endswith(".zip"):
            fileHo.zipextractor(f"{file_location}/{fileone.filename}", file_location)
        elif file_list[0].filename.endswith(".tar") or file_list[0].filename.endswith(".tar.gz"):
            fileHo.tarextractor(f"{file_location}/{fileone.filename}", file_location)
    os.chdir(file_location)
    create_owner: str = None
    if project.individual:
        gitlabHo.gitlab_project_create(userid, project.projectname)
        create_owner: str = userid
    else:
        gitlabHo.gitlab_group_project(groupname, project.projectname)
        create_owner: str = groupname
    user_info = usermapper.get_user(userid, db)
    os.system("git init --initial-branch=main")
    os.system(
        f"git remote add origin http://{userid}:{user_info.token}@192.168.0.49:4000/{create_owner}/{project.projectname}/"
    )
    os.system("git add .")
    os.system('git commit -m "Initial commit"')
    os.system("git push -u origin main")
    fileHo.removeallgit(file_location)
    name_space: str = gitlabHo.get_path_with_namespaces(project.projectname)
    gitlaburl: str = f"{constant.HTTP}{constant.GITLAB_IP}/{name_space}"
    return gitlaburl


def onlygithub(importproject: projectvo.ProjectGithub, userid: str, groupname: str, db: Session):
    creator_info = None
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
    response: requests.Response = requests.post(
        url=f"http://{constant.GITLAB_IP_S}/api/v4/import/github",
        headers=headers,
        data=json.dumps(data),
    )
    gitlaburl: str = f"{constant.HTTP}{constant.GITLAB_IP}/{userid}/{importproject.projectname}"
    return response, gitlaburl


def onlybitbucket(
    importproject: projectvo.ProjectBitbucket, userid: str, groupname: str, db: Session
):
    creator_info = None
    if importproject.individual:
        creator_info: dbvo.UserT = usermapper.get_user(userid, db)
    else:
        creator_info: dbvo.GroupT = groupmapper.get_group(groupname, db)
        userid: str = groupname
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
    gitlaburl: str = f"{constant.HTTP}{constant.GITLAB_IP}/{userid}/{importproject.projectname}"
    return response, gitlaburl
