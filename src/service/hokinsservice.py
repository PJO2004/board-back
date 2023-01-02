import os
import sys
import logging
import requests
import json
import yaml
from typing import Any
from sqlalchemy.orm import Session

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)
from constantstore import constant
from hokinscollect import redis_queue
from vo import dbvo
from mapper import hokinsmapper, slotmapper
from util import fileHo, grafanafile


def confirmRedis(projectname) -> bool:
    q: redis_queue.RedisQueue = redis_queue.StartQueue
    startqueuelist: list = q.get_without_all()
    q: redis_queue.RedisQueue = redis_queue.WaitingQueue
    waitingqueuelist: list = q.get_without_all()
    q: redis_queue.RedisQueue = redis_queue.ProceedingQueue
    proceeingqueuelist: list = q.get_without_all()
    totallist: list = list()
    if startqueuelist:
        totallist: list = totallist + startqueuelist
    if waitingqueuelist:
        totallist: list = totallist + waitingqueuelist
    if proceeingqueuelist:
        totallist: list = totallist + proceeingqueuelist
    if projectname in totallist:
        return False
    return True


def createpipe(projectname: str, db: Session):
    redis_queue.StartQueue.put(projectname)
    exit: dbvo.PipeT = hokinsmapper.exist_pipe(projectname, db)
    project_dir: str = f"{constant.WORKSPACE_PATH}/{projectname}"
    if not exit:
        slot_info: dbvo.SlotT = slotmapper.get_slot(projectname, db)
        hokinsmapper.create_pipe(slot_info, db)
    else:
        fileHo.removeallgit(project_dir)
    # 여기서부터
    hokinsmapper.create_exec(projectname, db)
    project: str = redis_queue.StartQueue.get()
    redis_queue.WaitingQueue.put(project)


def prometheusymlupdate(project_name) -> None:
    isNew: bool = True
    logging.info("jenkins pipeline end & prometheus add start.")
    with open(constant.PROMETHEUS_CONFIG_PATH) as f:
        yamlData: dict = yaml.load(f, Loader=yaml.FullLoader)
    yamlDataBefore = yamlData["scrape_configs"]
    for value in yamlDataBefore:
        if value["job_name"] == project_name:
            isNew: bool = False
        prometheus_data_deleter(project_name)
    if isNew:
        confignewupdate(yamlDataBefore, project_name, yamlData)
    promethus_datasource_uid, loki_uid = datasource_get_uid()
    if grafana_create_dashboard(project_name, promethus_datasource_uid, loki_uid):
        logging.info("Dashboard created.")
    else:
        logging.info("Dashboard Not created.")


def only_grafana(project_name):
    promethus_datasource_uid, loki_uid = datasource_get_uid()
    if grafana_create_dashboard(project_name, promethus_datasource_uid, loki_uid):
        logging.info("Dashboard created.")
    else:
        logging.info("Dashboard Not created.")


def confignewupdate(yamlDataBefore: list, project_name, yamlData) -> None:
    yamlDataBefore.append(
        {
            "job_name": project_name,
            "scrape_interval": "10s",
            "static_configs": [{"targets": [f"{project_name}:{constant.ANODE_PORT}"]}],
        }
    )
    yamlData["scrape_configs"] = yamlDataBefore
    with open(constant.PROMETHEUS_CONFIG_PATH, "w") as f:
        yaml.dump(yamlData, f)
    requests.post(f"{constant.PROMETHEUS_URL}/-/reload")
    logging.info("prometheus reload.")


def prometheus_data_deleter(project_name) -> requests.Response:
    url: str = "".join(
        [
            f"{constant.PROMETHEUS_URL}",
            '/api/v1/admin/tsdb/delete_series?match[]={job="',
            project_name,
            '"}',
        ]
    )
    return requests.post(url)


def grafana_create_dashboard(project_name, promethus_datasource_uid, loki_uid) -> bool:
    new_dash_str: str = json.dumps(grafanafile.new_dash)
    grafana_json: str = (
        new_dash_str.replace("(Project_name)", project_name)
        .replace("(prometheus_uid)", promethus_datasource_uid)
        .replace("(loki_uid)", loki_uid)
    )
    url: str = f"{constant.GRAFANA_IP}/api/dashboards/db"
    headers: dict[str, str] = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {constant.GRAFANA_API_KEY}",
    }
    response: requests.Response = requests.post(
        url, data=grafana_json, headers=headers, verify=False
    )
    logging.info(response.json())
    if response.status_code == 200:
        if response.json()["status"] == "success":
            return True
    return False


def datasource_get_uid() -> tuple:
    url: str = f"{constant.GRAFANA_IP}/api/datasources"
    headers: dict[str, str] = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {constant.GRAFANA_API_KEY}",
    }
    response: requests.Response = requests.get(url, headers=headers)
    datasource_json: dict = response.json()
    prometheus_uid: list = [i["uid"] for i in datasource_json if i["name"] == "Prometheus"]
    loki_uid: list = [i["uid"] for i in datasource_json if i["name"] == "Loki"]
    return prometheus_uid[0], loki_uid[0]


def datasource_create() -> requests.Response:
    url: str = f"{constant.GRAFANA_IP}/api/datasources"
    headers: dict[str, str] = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {constant.GRAFANA_API_KEY}",
    }
    data: dict[str, Any] = {
        "name": "prometheus",
        "type": "prometheus",
        "url": f"{constant.SERVER_URL}:{constant.PROMETHEUS_PORT}",
        "access": "proxy",
        "basicAuth": False,
    }
    response: requests.Response = requests.post(url, headers=headers, data=data)
    return response


def dashboard_delete(project_name=None) -> bool:
    url: str = f"{constant.GRAFANA_IP}/api/search?query=%"
    headers: dict[str, str] = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {constant.GRAFANA_API_KEY}",
    }
    response: requests.Response = requests.get(url, headers=headers)
    dashboardlist: dict = response.json()
    dashboard_uid: str = [
        value["uid"] for value in dashboardlist if value["title"] == project_name
    ][0]
    url: str = f"{constant.GRAFANA_IP}/api/dashboards/uid/{dashboard_uid}"
    response: requests.Response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        return True
    return False
