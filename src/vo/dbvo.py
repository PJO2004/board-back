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
    __tablename__: str = "user"
    usernumber: Column = Column(Integer, primary_key=True, index=True)
    userid: Column = Column(String(length=45))
    userpassword: Column = Column(String(length=45))
    username: Column = Column(String(length=45))
    useradmin: Column = Column(Integer)

class ReplyT(dbconn.db.base):
    __tablename__: str = 'reply'
    replyid: Column = Column(Integer, pimary_key=True, index=True)
    replycontent: Column = Column(String(length=200))
    replydatetime: Column = Column(DateTime(timezone=True))

class BoardT(dbconn.db.base):
    __tablename__: str = 'board'
    boardtitle: Column = Column(String(length=45))
    boarddatetime: Column = Column(DateTime(timezone=True))
    boardcontent: Column = Column(String(length=1000))