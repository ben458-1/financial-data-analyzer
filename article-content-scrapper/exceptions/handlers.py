from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions.custom_exception import CustomException


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=500,
            content={
                "detail": exc.detail
            }
        )