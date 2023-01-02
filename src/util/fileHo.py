import os
import ErrorHo
from typing import List, Dict
import shutil
import zipfile
import tarfile
from fastapi import UploadFile
import logging

sep: str = os.sep


def filecheck(file_location):
    # 파일이 없으면 에러
    if not os.path.exists(file_location):
        raise ErrorHo.FileNoExists(file_location)


def filechecktf(file_location):
    # 파일이 없으면 에러
    if not os.path.exists(file_location):
        return False
    return True


def nofilecheck(file_location):
    # 파일이 있으면 에러
    if os.path.exists(file_location):
        raise ErrorHo.FileAlreadyExists(file_location)


def nofilechecktf(file_location):
    # 파일이 있으면 에러
    if os.path.exists(file_location):
        return False
    return True


def listallfilename(file_location) -> List[str]:
    filecheck(file_location)
    return os.listdir(file_location)


def listallfilepath(file_location) -> List[str]:
    filecheck(file_location)
    file_list: List[str] = os.listdir(file_location)
    return [sep.join([file_location, one]) for one in file_list]


def listfilesname(file_location) -> List[str]:
    filecheck(file_location)
    file_list: List[str] = os.listdir(file_location)
    return [one for one in file_list if os.path.isfile(sep.join([file_location, one]))]


def listfilespath(file_location) -> List[str]:
    filecheck(file_location)
    file_list: List[str] = os.listdir(file_location)
    return [
        sep.join([file_location, one])
        for one in file_list
        if os.path.isfile(sep.join([file_location, one]))
    ]


def listdirsname(file_location) -> List[str]:
    filecheck(file_location)
    file_list: List[str] = os.listdir(file_location)
    return [one for one in file_list if os.path.isdir(sep.join([file_location, one]))]


def listdirspath(file_location) -> List[str]:
    filecheck(file_location)
    file_list: List[str] = os.listdir(file_location)
    return [
        sep.join([file_location, one])
        for one in file_list
        if os.path.isdir(sep.join([file_location, one]))
    ]


def makedir(file_location):
    nofilecheck(file_location)
    os.mkdir(file_location)


def nocheck(file_location):
    # 파일이 있으면 에러
    if os.path.exists(file_location):
        return True
    return False


def makedirs(file_location):
    if not nocheck(file_location):
        os.makedirs(file_location)


def chdir_just(file_location):
    os.chdir(file_location)


def getcwd() -> str:
    return os.getcwd()


def wantexe(file_location) -> str:
    filecheck(file_location)
    if os.path.isfile(file_location):
        return os.path.splitext(file_location)[1]
    return None


def filesize(file_location) -> int:
    filecheck(file_location)
    return os.path.getsize(file_location)


def allfiledetail(file_location) -> List:
    filecheck(file_location)
    file_list: List[str] = os.listdir(file_location)
    result: List = list()
    for onefile in file_list:
        file_full_path: str = sep.join([file_location, onefile])
        file_info: Dict = {
            "filename": onefile,
            "filesize": os.path.getsize(file_full_path),
            "filefull_path": file_full_path,
        }
        if os.path.isdir(file_full_path):
            file_info["fileshape"] = "Dir"
        elif os.path.isfile(file_full_path):
            file_info["fileshape"] = "File"
        result.append(file_info)
    return result


def chdirho(file_location):
    if os.path.exists(file_location):
        shutil.rmtree(file_location, ignore_errors=True)
    os.makedirs(file_location)
    os.chdir(file_location)


def justchdirho(file_location):
    os.chdir(file_location)


def command(commandsql: str):
    error: int = os.system(commandsql)
    return error


def deleteall(dirname: str):
    if os.path.exists(dirname):
        shutil.rmtree(dirname, ignore_errors=True)


def filechecks(file_location) -> bool:
    # 파일이 없으면 에러
    if not os.path.exists(file_location):
        # 없으면 False
        return False
    return True


def listfilesnames(file_location) -> List[str]:
    if filechecks(file_location):
        file_list: List[str] = os.listdir(file_location)
        return [one for one in file_list if os.path.isfile(sep.join([file_location, one]))]
    return None


def mkdirhoho(file_location):
    if not filechecks(file_location):
        os.makedirs(file_location)
        logging.info(f"{file_location} are created!")


def removeall(file_location) -> None:
    if not listfilesnames(file_location):
        return True
    shutil.rmtree(file_location, ignore_errors=True)


def removeallgit(file_location) -> None:
    if not listfilesnames(file_location):
        return True
    os.system(f"rm -rf {file_location}/.git")
    shutil.rmtree(file_location, ignore_errors=True)


def filesaver(file_location, fileone: UploadFile):
    file_locations: str = "/".join([file_location, fileone.filename])
    with open(file_locations, "wb+") as file_object:
        file_object.write(fileone.file.read())


def zipextractor(file_path, dir_path):
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(dir_path)


def tarextractor(file_path, dir_path):
    with tarfile.open(file_path) as tar_ref:
        tar_ref.extractall(path=dir_path)
