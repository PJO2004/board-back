import os
import platform
from passlib.context import CryptContext
import sys

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)
from config import envconfig

envsetting = envconfig.setting
# 기본세팅 불러오기!
# 비밀번호 해시
PASSWORD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OS 찾기
PLATFORMS: str = platform.system()

# 프로젝트 관련 정보
PROJECTNAME: str = envsetting.PROJECTNAME
UPLOAD_FILE_LIST: list = ["Dockerfile", "Jenkinsfile"]
BASE_PATH: str = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
DATA_PATH: str = f"{BASE_PATH}/data"
CODE_PATH: str = f"{DATA_PATH}/anode"
FILE_PATH: str = f"{DATA_PATH}/file"
WORKSPACE_PATH: str = f"{BASE_PATH}/workspaces"
ANODE_FILENAME: str = "hoho.zip"

# DB 관련 정보
SQLALCHEMY_DATABASE_URL: str = f"mariadb+pymysql://{envsetting.DBUSERNAME}:{envsetting.DBPASSWORD}@{envsetting.DBHOST}:{envsetting.DBPORT}/{envsetting.DBNAME}?charset=utf8mb4"
# SQLALCHEMY_DATABASE_URL: str = f"mariadb+mariadbconnector://{settings.DBUSERNAME}:{settings.DBPASSWORD}@{settings.DBHOST}:{settings.DBPORT}/{settings.DBNAME}?charset=utf8mb4"
# SERVER
SERVER_IP: str = envsetting.SERVER_IP
SERVER_URL: str = f"http://{SERVER_IP}"

# 프로메테우스 관련 정보
# PROMETHEUS_PORT: str = "9091"
if PLATFORMS == "Windows":
    PROMETHEUS_PORT: str = "9091"
else:
    PROMETHEUS_PORT: str = "9090"

if PLATFORMS == "Windows":
    PROMETHEUS_URL: str = f"http://{SERVER_IP}:{PROMETHEUS_PORT}"
else:
    PROMETHEUS_URL: str = f"http://prometheus:{PROMETHEUS_PORT}"

if PLATFORMS == "Windows":
    PROMETHEUS_CONFIG_PATH: str = f"{BASE_PATH}/prometheus.yml"
else:
    PROMETHEUS_CONFIG_PATH: str = "/usr/srcs/prometheus.yml"

# GITLAB 관련 정보
if PLATFORMS == "Windows":
    GITLAB_PORT: str = "4000"
else:
    GITLAB_PORT: str = "80"
if PLATFORMS == "Windows":
    GITLAB_URL: str = f"{SERVER_URL}:{GITLAB_PORT}"
else:
    GITLAB_URL: str = f"http://gitlab:{GITLAB_PORT}"
# GITLAB_URL: str = f"{SERVER_URL}:{GITLAB_PORT}"
if PLATFORMS == "Windows":
    GITLAB_IP: str = f"{SERVER_IP}:{GITLAB_PORT}"
else:
    GITLAB_IP: str = f"gitlab:{GITLAB_PORT}"
GITLAB_IPFORJENKINS: str = f"gitlab:80"
# GITLAB_IP: str = f"{SERVER_IP}:{GITLAB_PORT}"
GITLAB_TOKEN: str = envsetting.GITLAB_TOKEN  # envsetting

# 젠킨스 관련 정보
if PLATFORMS == "Windows":
    JENKINS_PORT: str = "9090"
else:
    JENKINS_PORT: str = "8080"
if PLATFORMS == "Windows":
    JENKINS_URL: str = f"{SERVER_URL}:{JENKINS_PORT}"
else:
    JENKINS_URL: str = f"http://jenkins:{JENKINS_PORT}"
# JENKINS_URL: str = f"{SERVER_URL}:{JENKINS_PORT}"
JENKINS_USERNAME: str = envsetting.JENKINS_USERNAME
JENKINS_PASSWORD: str = envsetting.JENKINS_PASSWORD

# 그라파나 관련
if PLATFORMS == "Windows":
    GRAFANA_PORT: str = "3001"
else:
    GRAFANA_PORT: str = "3000"

if PLATFORMS == "Windows":
    GRAFANA_IP: str = f"{SERVER_URL}:{GRAFANA_PORT}"
else:
    GRAFANA_IP: str = f"http://grafana:{GRAFANA_PORT}"
# GRAFANA_IP: str = f"{SERVER_URL}:{GRAFANA_PORT}"
GRAFANA_API_KEY = envsetting.GRAFANA_API_KEY
# GRAFANA_API_KEY: str = (
#     "eyJrIjoiVGF6VEZaMDZnSDU2V2x1ZUhkVUJ4SXRJUkRRZXoySDAiLCJuIjoiYWFhYWFhIiwiaWQiOjF9"
# )

# ANODE 관련 정보
ANODE_PORT: int = 8000

# 젠킨스 파일 관련
HTTP: str = "http://"
GITLABIP_BEFORE: str = "(git_ip_s)"
JENKINS_BRANCH: str = "(branch)"
PROJECT_NAME_REPLACEMENT: str = "(project_name)"
GITLABIP_USERNAME: str = "(git_username)"
GITLABIP_TOKEN: str = "(git_usertoken)"
PROJECTNAME: str = "${projectname}"
BUILDNAME: str = "${buildname}"
BRIDGE: str = "${bridge}"
BRIDGESERVER: str = "hadoop_cluster_v3_projectnet"

# 레디스 관련
REDIS_IP: str = envsetting.REDISHOST
REDIS_PORT: int = envsetting.REDISPORT
REDISTARTQUEUENAME: str = "start"
REDISJOBQUEUENAME: str = "waiting"
REDISPROCEEDINGQUEUENAME: str = "proceeding"

if PLATFORMS == "Windows":
    GITLAB_IP_S: str = f"{SERVER_IP}:4000"
else:
    GITLAB_IP_S: str = "gitlab:80"

if PLATFORMS == "Windows":
    GIT_IP: str = f"{SERVER_IP}:4000"
else:
    GIT_IP: str = "gitlab:80"
