# app/lifespans/app_lifespan.py

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core import config
from app.db.session import PooledDatabase


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    print("🔧 [Startup] Creating config instance & initializing DB pool")
    config.create_instance()
    PooledDatabase.initialize(minconn=2, maxconn=20)

    yield  # 🔄 App runs here

    print("🧹 [Shutdown] Closing DB pool")
    PooledDatabase.close_all()
