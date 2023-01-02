from fastapi.responses import JSONResponse
import logging


def successResponse(msg: str, another: dict = None) -> JSONResponse:
    contents: dict = {"message": msg}
    if another:
        for key, value in another.items():
            contents[key] = value
    return JSONResponse(
        status_code=200,
        content=contents,
    )


def authfailResponse(msg: str, another: dict = None) -> JSONResponse:
    contents: dict = {"message": msg}
    if another:
        for key, value in another.items():
            contents[key] = value
    logging.error(contents)
    return JSONResponse(
        status_code=401,
        content=contents,
    )


# responseho.errorResponse("username 과 password가 잘못되었습니다.")
# responseho.successResponse("created successfully")
def errorResponse(msg: str, another: dict = None) -> JSONResponse:
    contents: dict = {"message": msg}
    if another:
        for key, value in another.items():
            contents[key] = value
    logging.error(contents)
    return JSONResponse(
        status_code=400,
        content=contents,
    )
