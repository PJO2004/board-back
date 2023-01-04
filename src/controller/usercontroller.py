import sys
import os
from sqlalchemy.orm import Session
from fastapi import APIRouter, BackgroundTasks, Depends, Response, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)
from util.dbconn import db
from config.envconfig import setting

router: APIRouter = APIRouter()
