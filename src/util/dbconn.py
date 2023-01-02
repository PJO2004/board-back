from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sys
import os

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)
from constantstore import constant

"""

DB 연결 관련 처리
그 어떤 것도 그렇지만 호영이 만든 파일

"""


class AlchemyHo:
    def __init__(self):
        self._engine = None
        self._session = None
        self.init_app()

    def init_app(self):
        self._engine = create_engine(constant.SQLALCHEMY_DATABASE_URL)
        self._session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self._base = declarative_base()

    def get_db(self):
        db_session = None
        try:
            db_session = self._session()
            yield db_session
        finally:
            db_session.close()

    @property
    def session(self):
        return self.get_db

    @property
    def base(self):
        return self._base

    @property
    def engine(self):
        return self._engine


db: AlchemyHo = AlchemyHo()
