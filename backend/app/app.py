from fastapi import FastAPI
from .routers import users


def init_routers(app: FastAPI) -> None:
    app.include_router(users.router, prefix="/api/v1")


def create_app() -> FastAPI:
    app = FastAPI()
    init_routers(app=app)

    return app


app = create_app()
