import sys
import os
import traceback
import logging
import logging.config
from http import HTTPStatus
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi_jwt_auth.exceptions import MissingTokenError
from fastapi import Request, Response, FastAPI
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette_exporter import PrometheusMiddleware, handle_metrics
from typing import Dict

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)
from loggingho import importlogdic
from src.hokinscollect import hokins
from src.util import fileHo, ErrorHo, adminmaker, dbconn
from src.constantstore import constant

status_reasons: Dict[int, str] = {x.value: x.name for x in list(HTTPStatus)}
"""
FastApi와 관련된 모든 첫 세팅을 하는 곳
"""


def get_extra_info(request: Request, response: Response) -> dict:
    return {
        "req": {
            "url": request.url.path,
            "headers": {
                "host": request.headers["host"],
                "user-agent": request.headers["user-agent"],
                "accept": request.headers["accept"],
            },
            "method": request.method,
            "httpVersion": request.scope["http_version"],
            "originalUrl": request.url.path,
            "query": {},
        },
        "res": {
            "statusCode": response.status_code,
            "body": {
                "statusCode": response.status_code,
                "status": status_reasons.get(response.status_code),
            },
        },
    }


def create_app(app: FastAPI) -> FastAPI:
    logging.config.dictConfig(importlogdic())
    # app.mount("/static", StaticFiles(directory="static"), name="static")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://192.168.0.49:7777"],  # *
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
    app.add_middleware(PrometheusMiddleware)
    app.add_route("/metrics", handle_metrics)

    @app.exception_handler(MissingTokenError)
    async def token_exception_handler(request: Request, exc: MissingTokenError) -> JSONResponse:
        return JSONResponse(
            status_code=401,
            content={"message": "There are not anything token."},
        )
        # response: RedirectResponse = RedirectResponse(url="/user/refresh", status_code=303)
        # return response

    @app.exception_handler(ErrorHo.Anythingdonthave)
    async def token_all_exception_handler(
        request: Request, exc: ErrorHo.Anythingdonthave
    ) -> JSONResponse:
        return JSONResponse(
            status_code=401,
            content={"message": "There are not anything token."},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        logging.error(str(exc))
        return JSONResponse(
            status_code=400,
            content={"message": "There is no required value."},
        )

    @app.exception_handler(ValueError)
    async def value_error_exception_handler(request: Request, exc: ValueError) -> JSONResponse:
        logging.error(str(exc))
        return JSONResponse(
            status_code=400,
            content={"message": "There is no required value."},
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        logging.error(str(exc.__class__.__name__))
        logging.error(str(exc.detail))
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": str(exc.detail)},
        )

    @app.exception_handler(Exception)
    async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
        errorcontent = "".join(
            traceback.format_exception(etype=type(exc), value=exc, tb=exc.__traceback__)
        )
        logging.error(errorcontent)
        return JSONResponse(
            status_code=400,
            content={"message": "Error"},
        )

    @app.middleware("http")
    async def log_request(request: Request, call_next):
        response = await call_next(request)
        if request.url.path != "/metrics":
            logging.info(
                f"{request.method} {request.url.path} {str(get_extra_info(request, response))}"
            )
        return response

    @app.on_event("startup")
    async def startup_event():
        dbconn.db.engine.connect()
        hokins.load()
        adminmaker.makeadmin()
        fileHo.mkdirhoho(constant.FILE_PATH)
        fileHo.mkdirhoho(constant.WORKSPACE_PATH)
        logging.info("FastApi Start now!")

    @app.on_event("shutdown")
    async def startup_event():
        dbconn.db.session.close_all()
        dbconn.db.engine.dispose()
        logging.info("FastApi Shutdown now!")

    return app
