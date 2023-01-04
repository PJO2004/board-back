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
# 기본 세팅
PASSWORD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OS
PLATFORMS: str = platform.system()

# 프로젝트 관련 정보
PROJECTNAME: str = envsetting.PROJECTNAME
BASE_PATH: str = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# DB 관련 정보
SQLALCHEMY_DATABASE_URL: str = f"mysql+pymysql://{envsetting.DBUSERNAME}:{envsetting.DBPASSWORD}@{envsetting.DBHOST}:{envsetting.DBPORT}/{envsetting.DBNAME}?charset=utf8mb4"

# 서버
SERVER_IP: str = envsetting.SERVER_IP
SERVER_URL: str = f"http://{SERVER_IP}"