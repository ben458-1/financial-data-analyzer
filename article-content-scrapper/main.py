import uvicorn
from fastapi import FastAPI
from api import articles, application
from contextlib import asynccontextmanager
from logger import log
from service.rabbit_mq import rabbit_mq as mq
from core import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown events."""
    log.log_application_start()
    log.log_application_start_time()
    config.create_instance()

    yield  # Application runs here

    mq.rabbitmq_connection.close()
    log.log_application_end_time()
    log.log_application_shutdown()


# Initialize FastAPI with lifespan management
app = FastAPI(lifespan=lifespan)
app.include_router(articles.router)
app.include_router(application.app_router)

if __name__ == '__main__':
    uvicorn.run(app=app, host="0.0.0.0", port=9005)
