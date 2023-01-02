import time
import sys
import os
import logging
import yaml
import subprocess
import time
from multiprocessing import Process
import requests
from typing import List

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)
import redis_queue
import hokinsdb
from constantstore import constant
from util import fileHo


def godhokins() -> None:
    def yamlreader(hokins_path) -> dict:
        yamlresult: dict = None
        with open(hokins_path) as file:
            yamlresult: dict = yaml.load(file, Loader=yaml.FullLoader)
        return yamlresult

    def has_key(hodict: List[dict], keyname: str) -> bool:
        for oneset in hodict:
            if keyname in oneset.keys():
                return oneset.get(keyname)
        return None

    def gitcloneho(projectname) -> str:
        fileHo.chdir_just(f"{constant.WORKSPACE_PATH}")
        # 일단 여기서 git clone
        pipeinfo = hokinsdb.gitfound(projectname)
        stream = os.popen(
            f"git clone -b main --single-branch http://{pipeinfo.git_username}:{pipeinfo.git_usertoken}@{constant.GITLAB_IP_S}/{pipeinfo.git_path_with_namespaces}.git"
        )
        output: str = stream.read()
        return output

    def endofqueue(msg: str, buildnum: int, error_cause: str = None):
        project: str = redis_queue.ProceedingQueue.get()
        logging.info(f"{project} {msg}")
        if error_cause:
            hokinsdb.errorinsert(projectname, buildnum, error_cause)
        else:
            hokinsdb.successinsert(projectname, buildnum)

    def docker_deplot_checher():
        time_sleep: int = 1
        while 1:
            result = subprocess.run(
                ["docker inspect --format='{{.State.Status}}' fastapiho"],
                stdout=subprocess.PIPE,
                shell=True,
                text=True,
            )
            if result.stdout.strip() == "running":
                return False
            if time_sleep > 10:
                return True
            time.sleep(time_sleep)
            time_sleep = time_sleep * 2

    def contentsReplace(contents: str):
        return (
            contents.replace(constant.PROJECTNAME, projectname)
            .replace(constant.BUILDNAME, str(build_num))
            .replace(constant.BRIDGE, constant.BRIDGESERVER)
        )

    while 1:
        if projectname := redis_queue.WaitingQueue.get():
            redis_queue.ProceedingQueue.put(projectname)
            projectdir: str = f"{constant.WORKSPACE_PATH}/{projectname}"
            build_num: int = hokinsdb.presentbuilder(projectname)
            output: str = gitcloneho(projectname)
            fileHo.chdir_just(projectdir)
            yaml_result: dict = yamlreader(f"{constant.FILE_PATH}/hokins.yml")
            fail_step: str = None
            streams: int = 0
            for step in yaml_result:
                dictvalue: list = yaml_result[step]
                if contents := has_key(dictvalue, "content"):
                    streams: int = os.system(contentsReplace(contents))
                    logging.info(f"{step} start")
                if streams and step != "deleteContainer":
                    if failcontent := has_key(dictvalue, "iffail"):
                        os.system(failcontent)
                        logging.info(f"{step} error")
                    fail_step: str = step
                    break
            if fail_step or docker_deplot_checher():
                endofqueue(f"fail {fail_step}", build_num, fail_step)
                continue
            endofqueue(f"are successfully close", build_num)
            requests.get(url=f"http://takeproxyload:8010/addContainer/{projectname}")
            requests.get(url=f"http://localhost:8080/build/prometheus/{projectname}")
        else:
            time.sleep(1)


def load():
    process_one: Process = Process(target=godhokins, args=())
    process_one.start()
