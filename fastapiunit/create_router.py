from fastapi import FastAPI


def include_router(app: FastAPI) -> FastAPI:
    from src.controller import (
        usercontroller,
        groupcontroller,
        projectcontoller,
        slotcontoller,
        paramcontroller,
        buildcontroller,
        execcontroller,
    )

    app.include_router(usercontroller.router, prefix="/user")
    app.include_router(groupcontroller.router, prefix="/group")
    app.include_router(projectcontoller.router, prefix="/project")
    app.include_router(slotcontoller.router, prefix="/slot")
    app.include_router(paramcontroller.router, prefix="/param")
    app.include_router(buildcontroller.router, prefix="/build")
    app.include_router(execcontroller.router, prefix="/exec")
    return app
