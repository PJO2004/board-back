# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import os
import sys


sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)
from vo import paramvo
from service import paramservice
from util import gitlabHo, responseho, dbconn, AuthHo

router: APIRouter = APIRouter()
dbconn.db.base.metadata.create_all(bind=dbconn.db.engine)


@router.post("/", tags=["param"])
async def yml_creater(
    paramwithname: paramvo.ParamRequestS,
    Authorize: AuthHo.AuthJWT = Depends(),
    username: str = Depends(AuthHo.require_user),
    db: Session = Depends(dbconn.db.session),
) -> JSONResponse:
    Authorize.jwt_required()
    projectid: str = paramwithname.slotid
    if not gitlabHo.project_search(projectid):
        return responseho.errorResponse("There is no such project..", {"result": False})
    if not gitlabHo.project_member_confirm(projectid, username):
        return responseho.errorResponse("You do not have permission", {"result": False})
    try:
        paramservice.paramcreate(paramwithname, username, db)
        return responseho.successResponse("param successfully created", {"result": True})
    except Exception as e:
        return responseho.errorResponse(f"{str(e)}", {"result": False})


@router.get("/{projectname}", tags=["param"])
async def param_list(projectname: str) -> dict:
    return {"paramList": paramservice.paramlist(projectname)}
