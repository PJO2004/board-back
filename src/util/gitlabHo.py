import sys
import os
import gitlab
import base64

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)

from vo import uservo, groupvo
from constantstore import constant
from typing import List

"""

GITLAB 관련 API 사용!!
GITLAB 유저, 프로젝트, 그룹, 파일 올리기
그 어떤 것도 그렇지만 호영이 만든 파일

"""
githo: gitlab.Gitlab = gitlab.Gitlab(constant.GITLAB_URL, private_token=constant.GITLAB_TOKEN)
githo.auth()
TOKEN_SCOPE: List[str] = ["api", "read_api", "read_user", "read_repository", "write_repository"]

# GitLab User 만들기
def git_user_create(user_info: uservo.UserInfoN) -> None:
    email: str = user_info.email
    userid: str = user_info.userid
    username: str = user_info.username
    password: str = user_info.password
    user = githo.users.create(
        {
            "email": email,
            "password": password,
            "username": userid,
            "name": username,
            "skip_confirmation": True,
        }
    )


# GitLAb User 삭제
def user_delete_gitlab(userid: str) -> None:
    usersomeone = githo.users.list(username=userid)[0]
    user_id: str = usersomeone.id
    githo.users.delete(user_id)


# 슬롯 삭제
def slotdelete(slotid: str) -> None:
    project = githo.projects.list(search=slotid)[0]
    project.delete()


# 그룹 생성
def group_create(usergroup: groupvo.UserGroup) -> None:
    groupname: str = usergroup.groupname
    userid: str = usergroup.ownername
    usersomeone = githo.users.list(username=userid)[0]
    group = githo.groups.create({"name": groupname, "path": groupname})
    group_member = group.members.create(
        {"user_id": usersomeone.id, "access_level": gitlab.const.AccessLevel.OWNER}
    )


# 그룹에 유저 추가
def group_add(userinfo: uservo.UserInfoN) -> None:
    groupname: str = userinfo.groupname
    userid: str = userinfo.userid
    usersomeone = githo.users.list(username=userid)[0]
    group = githo.groups.list(search=groupname)[0]
    member = group.members.create(
        {"user_id": usersomeone.id, "access_level": gitlab.const.AccessLevel.DEVELOPER}
    )


# 그룹에 유저 추가 str
def group_add_str(userid: str, groupname: str) -> None:
    usersomeone = githo.users.list(username=userid)[0]
    group = githo.groups.list(search=groupname)[0]
    member = group.members.create(
        {"user_id": usersomeone.id, "access_level": gitlab.const.AccessLevel.DEVELOPER}
    )


# 그룹 삭제
def group_delete(groupname: str) -> None:
    group = githo.groups.list(search=groupname)[0]
    group.delete()


# 그룹에 유저 추가
def group_addw(user_group: groupvo.UserGroup) -> None:
    groupname: str = user_group.groupname
    userid: str = user_group.ownername
    usersomeone = githo.users.list(username=userid)[0]
    group = githo.groups.list(search=groupname)[0]
    member = group.members.create(
        {"user_id": usersomeone.id, "access_level": gitlab.const.AccessLevel.DEVELOPER}
    )


# 유저 토큰 생성
def user_token(userid: str):
    usersomeone = githo.users.list(username=userid)[0]
    usertoken = usersomeone.impersonationtokens.create({"name": "usertoken", "scopes": TOKEN_SCOPE})
    return usertoken.token


# 그룹 멤버 조회
def group_member(userinfo: uservo.UserInfoN) -> List:
    groupname: str = userinfo.groupname
    group = githo.groups.list(search=groupname)[0]
    members = group.members.list()
    member_list: list = [i.username for i in members]
    return member_list


# 그룹 토큰 생성
def group_token(group_info: groupvo.GroupInfo) -> str:
    groupname: str = group_info.groupname
    group = githo.groups.list(search=groupname)[0]
    grouptoken = group.access_tokens.create({"name": "grouptoken", "scopes": TOKEN_SCOPE})
    return grouptoken.token


# 프로젝트 생성
def gitlab_project_create(userid, projectname) -> None:
    usersomeone = githo.users.list(username=userid)[0]
    userproject = usersomeone.projects.create({"name": projectname})


# 그룹 프로젝트 생성
def gitlab_group_project(group_name, projectname) -> None:
    group_id: str = githo.groups.list(search=group_name)[0].id
    groupproject = githo.projects.create({"name": projectname, "namespace_id": group_id})


# 프로젝트 멤버 확인
def project_member_confirm(projectname, recomenduser) -> bool:
    project: str = githo.projects.list(search=projectname)[0]
    userlist: list = [member.username for member in project.users.list()]
    if recomenduser in userlist:
        return True
    return False


# 프로젝트 멤버 추가
def project_member_add(projectname, userid) -> None:
    usersomeone = githo.users.list(username=userid)[0]
    project = githo.projects.list(search=projectname)[0]
    project.members.create(
        {"user_id": usersomeone.id, "access_level": gitlab.const.AccessLevel.DEVELOPER}
    )


# 프로젝트 멤버 셀프 추가
def project_member_selfadd() -> None:
    projectname: str = "aaa"
    username: str = "take"
    usersomeone = githo.users.list(username=username)[0]
    project = githo.projects.list(search=projectname)[0]
    project.members.create(
        {"user_id": usersomeone.id, "access_level": gitlab.const.AccessLevel.DEVELOPER}
    )


# 프로젝트 전체 리스트
def project_total_list(userid, group_name) -> list:
    usersomeone: str = githo.users.list(username=userid)[0]
    user_projects: list = usersomeone.projects.list()
    group: str = githo.groups.list(search=group_name)[0]
    group_projects: list = group.projects.list()
    total_projects: list = list(set(user_projects + group_projects))
    total_projects_result: list = [githo.projects.get(ids.id) for ids in total_projects]
    return total_projects_result


# 유저 프로젝트 리스트
def project_user_list(userid) -> list:
    usersomeone = githo.users.list(username=userid)[0]
    user_projects = usersomeone.projects.list()
    user_projects_result = [githo.projects.get(ids.id) for ids in user_projects]
    return user_projects_result


# 그룹 프로젝트 리스트
def project_group_list(group_name) -> list:
    group = githo.groups.list(search=group_name)[0]
    group_projects = group.projects.list()
    group_projects_result = [githo.projects.get(ids.id) for ids in group_projects]
    return group_projects_result


# 프로젝트 브랜치 생성 -> stg prd
def branch_create(projectname) -> bool:
    project = githo.projects.list(search=projectname)[0]
    stg = project.branches.create({"branch": "stg", "ref": "main"})
    prd = project.branches.create({"branch": "prd", "ref": "main"})
    if len(project.branches.list()) != 3:
        return False
    return True


# 프로젝트 path 조회
def get_path_with_namespaces(project_name) -> str:
    project_name_id = githo.projects.list(search=project_name)
    project = githo.projects.get(project_name_id[0].id)
    return project.path_with_namespace


# 프로젝트 검색
def project_search(projectname) -> list:
    projects: list = githo.projects.list(search=projectname)
    return projects

def filecontentcreate(project, filecontent, filename, anode=False) -> None:
    f = project.files.create(
        {
            "file_path": filename,
            "branch": "main",
            "content": filecontent,
            "author_email": "test@example.com",
            "author_name": "yourname",
            "commit_message": f"Create {filename}",
        }
    )
    f.content = filecontent
    if not anode:
        f.save(branch="main", commit_message=f"Update {filename}")
    else:
        f.save(branch="main", commit_message=f"Update modelzip", encoding="base64")


def dockerfileCreate(slotid: str, dockerimage: str) -> None:
    project = githo.projects.list(search=slotid)[0]
    filename: str = "Dockerfile"
    f = open(f"{constant.DATA_PATH}/modelfiles/{filename}", "r")
    filecontent: str = f.read()  # {dockerimage}
    if dockerimage:
        filecontent: str = filecontent.replace("{dockerimage}", dockerimage)
    else:
        filecontent: str = filecontent.replace("{dockerimage}", "python:3.8-buster")
    f.close()
    filecontentcreate(project, filecontent, filename)


def dockerfile_delete(slotid: str):
    project = githo.projects.list(search=slotid)[0]
    project.files.delete(file_path="Dockerfile", commit_message="Delete Dockerfile", branch="main")


def jsonfileCreate(slotid: str) -> None:
    project = githo.projects.list(search=slotid)[0]
    filename: str = "paramjson.json"
    if os.path.exists(f"{constant.DATA_PATH}/json/param_{slotid}.json"):
        f = open(f"{constant.DATA_PATH}/json/param_{slotid}.json", "r")
        filecontent: str = f.read()  # {paramjson}
        f.close()
        filecontentcreate(project, filecontent, filename)

# 슬롯 생성
def slotprojectcreate(projectname: str, userid: str, slotid: str) -> None:
    projects = githo.projects.list(search=projectname)[0]
    fork = projects.forks.create({"namespace": userid, "name": slotid, "path": slotid})
    projects.delete_fork_relation()


# Anode upload to zip
def anodeupload(slotid: str) -> None:
    filecontentbyte: bytes = base64.b64encode(
        open(f"{constant.CODE_PATH}/{constant.ANODE_FILENAME}", "rb").read()
    )
    filecontent: str = str(filecontentbyte, "utf-8")
    afterproject: str = githo.projects.list(search=slotid)[0]
    filecontentcreate(afterproject, filecontent, constant.ANODE_FILENAME, True)


# requirement.txt 찾기
def detectfile(projectname: str, filename: str = "requirement.txt") -> bool:
    projects = githo.projects.list(search=projectname)[0]
    try:
        f = projects.files.get(file_path=filename, ref="main")
    except Exception as e:
        # 파일이 없다.
        return False
    else:
        # 파일이 있다.
        return True


# requirement.txt 추가
def requirementfileCreate(slotid: str) -> None:
    project: str = githo.projects.list(search=slotid)[0]
    filename: str = "requirement.txt"
    f = open(f"{constant.DATA_PATH}/modelfiles/{filename}", "r")
    filecontent: str = f.read()  # {dockerimage}
    f.close()
    filecontentcreate(project, filecontent, filename)


import time


def importrequest(filename: str, projectname: str, projectuserid: str):
    with open(filename, "rb") as f:
        output: dict = githo.projects.import_project(
            f, path=projectname, name=projectname, namespace=projectuserid
        )
    project_import = githo.projects.get(output["id"], lazy=True).imports.get()
    while project_import.import_status != "finished":
        time.sleep(1)
        project_import.refresh()
