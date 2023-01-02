from pydantic import BaseSettings
import sys
import os

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

"""
ENV 등을 읽어오는 곳
"""
BASE_PATH: str = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))


class Settings(BaseSettings):
    PROJECTNAME: str
    SERVER_IP: str
    JENKINS_USERNAME: str
    JENKINS_PASSWORD: str
    GRAFANA_API_KEY: str
    GITLAB_TOKEN: str
    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    REFRESH_TOKEN_EXPIRES_IN: int
    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str
    DBHOST: str
    DBPORT: int
    DBUSERNAME: str
    DBPASSWORD: str
    DBNAME: str
    REDISHOST: str
    REDISPORT: str

    class Config:
        env_file: str = f"{BASE_PATH}/config/.env"
        env_file_encoding = "utf-8"


setting: Settings = Settings()
