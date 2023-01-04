from fastapi import FastAPI

def include_router(app: FastAPI) -> FastAPI:
    from src.controller import (
        usercontroller,
        boardcontroller
)

    app.include_router(usercontroller.router, prefix='/user')
    app.include_router(boardcontroller.router, prefix='/group')
    return app