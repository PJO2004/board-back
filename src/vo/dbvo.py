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
    '''
     userno : user number
     userid : user id
     userpw : user password
     usernm : user name
     userad : user admin
    '''

    userno: Column = Column(Integer, primary_key=True, index=True)
    userid: Column = Column(String(length=45))
    userpw: Column = Column(String(length=45))
    usernm: Column = Column(String(length=45))
    userad: Column = Column(Integer)

class ReplyT(dbconn.db.base):
    __tablename__: str = 'reply'
    '''
     repid   : reply id
     repcont : reply content
     repdtm  : reply datetime
    '''
    
    repid: Column = Column(Integer, pimary_key=True, index=True)
    repcont: Column = Column(String(length=200))
    repdtm: Column = Column(DateTime(timezone=True))

class BoardT(dbconn.db.base):
    __tablename__: str = 'board'
    '''
     boardid  : board
     boardt   : board title
     boarddtm : board datetime
     boardcon : board content
    '''

    boardid: Column = Column(Integer)
    boardt: Column = Column(String(length=45))
    boarddtm: Column = Column(DateTime(timezone=True))
    boardcon: Column = Column(String(length=1000))