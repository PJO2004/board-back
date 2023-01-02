import sys
import os
from sqlalchemy import Column, String, DateTime, Boolean, Integer
from sqlalchemy.sql import func

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)
from util import dbconn


class UserT(dbconn.db.base):
    __tablename__: str = "userho"
    userid: Column = Column(String(length=100), primary_key=True, index=True)
    username: Column = Column(String(length=100))
    email: Column = Column(String(length=100), unique=True)
    password: Column = Column(String(length=2000))
    groupname: Column = Column(String(length=100), nullable=True)
    token: Column = Column(String(length=1000), nullable=True)
    regdtm: Column = Column(DateTime(timezone=True), server_default=func.now())
    administer: Column = Column(Boolean(), default=False)


class GroupT(dbconn.db.base):
    __tablename__: str = "groupho"
    groupname: Column = Column(String(length=100), primary_key=True, index=True)
    ownername: Column = Column(String(length=100))
    token: Column = Column(String(length=1000), nullable=True)
    regdtm: Column = Column(DateTime(timezone=True), server_default=func.now())


class SlotT(dbconn.db.base):
    __tablename__: str = "slotho"
    slotid: Column = Column(String(length=100), primary_key=True, index=True)
    projectname: Column = Column(String(length=100))
    userid: Column = Column(String(length=100))
    groupname: Column = Column(String(length=100))
    param: Column = Column(String(length=2000))
    token: Column = Column(String(length=2000))
    deploystate: Column = Column(String(length=100))
    regdtm: Column = Column(DateTime(timezone=True), server_default=func.now())
    deploydtm: Column = Column(DateTime(timezone=True), nullable=True)
    naspath: Column = Column(String(length=100), nullable=True)
    nasdockerpath: Column = Column(String(length=100), nullable=True)
    filepath: Column = Column(String(length=100), nullable=True)
    filedockerpath: Column = Column(String(length=100), nullable=True)
    dockerimage: Column = Column(String(length=100), nullable=True)


class ProjectT(dbconn.db.base):
    __tablename__: str = "projectho"
    projectname: Column = Column(String(length=100), primary_key=True, index=True)
    userid: Column = Column(String(length=100), nullable=True)
    groupname: Column = Column(String(length=100), nullable=True)
    reg_dtm: Column = Column(DateTime(timezone=True), server_default=func.now())
    giturl: Column = Column(String(length=100), nullable=True)
    token: Column = Column(String(length=100), nullable=True)
    param: Column = Column(String(length=2000), nullable=True)


class PipeT(dbconn.db.base):
    __tablename__: str = "pipe"
    project_name: Column = Column(String(length=100), primary_key=True, index=True)
    git_username: Column = Column(String(length=100))
    git_usertoken: Column = Column(String(length=2000))
    git_path_with_namespaces: Column = Column(String(length=200))
    git_ip_s: Column = Column(String(length=100), nullable=True)
    reg_dtm: Column = Column(DateTime(timezone=True), server_default=func.now())
    dep_state: Column = Column(String(length=10), nullable=True)
    dep_dtm: Column = Column(DateTime(timezone=True), nullable=True)


class ExecPipeT(dbconn.db.base):
    __tablename__: str = "execpipe"
    index: Column = Column(Integer, primary_key=True, autoincrement=True)
    project_name: Column = Column(String(length=100))
    num: Column = Column(Integer, nullable=True)
    dep_state: Column = Column(String(length=10), nullable=True)
    error_cause: Column = Column(String(length=1000), nullable=True)
    dep_dtm: Column = Column(DateTime(timezone=True), server_default=func.now())
    end_dep_dtm: Column = Column(DateTime(timezone=True), nullable=True, onupdate=func.now())


class ExecT(dbconn.db.base):
    __tablename__: str = "execho"
    jobid: Column = Column(String(length=100), primary_key=True, index=True)
    slotid: Column = Column(String(length=100))
    userid: Column = Column(String(length=100))
    state: Column = Column(String(length=100))
    param: Column = Column(String(length=2000), nullable=True)
    result: Column = Column(String(length=2000), nullable=True)
    starttime: Column = Column(DateTime(timezone=True), server_default=func.now())
    endtime: Column = Column(DateTime(timezone=True), nullable=True)
    filelist: Column = Column(String(length=2000), nullable=True)

