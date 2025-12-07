from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from logger import log
from core import config
from core.config import reset_settings
import traceback
from service.utils import mail_utils
from datetime import datetime, timezone
from service.rabbit_mq import rabbit_mq as mq
from model.system_error_mail import SysErrorModel
from core.config import data_source as ds

app_router = APIRouter(
    prefix="/app-config/v1", tags=["app-config:v1.0.0"]
)


@app_router.get('/switch-automation-framework')
def change_selenium_framework():
    try:
        ds = config.data_source
        cfw = ds.SELENIUM_FRAMEWORK
        supported_frameworks = ds.SUPPORTED_FRAMEWORKS
        nfw = ''
        if supported_frameworks:
            fws = supported_frameworks.split(',')
            for fw in fws:
                if cfw != fw:
                    ds.SELENIUM_FRAMEWORK = fw
                    nfw = fw
        return JSONResponse(status_code=200,
                            content={
                                "message":
                                    f'The Selenium framework type has been successfully changed from {cfw} to {nfw}'
                            })
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f'Error occurred while setting into new framework, {e}')


@app_router.post('/change-selenium-framework')
def user_defined_framework(set_framework: str):
    try:
        ds = config.data_source
        cfw = ds.SELENIUM_FRAMEWORK
        supported_frameworks = ds.SUPPORTED_FRAMEWORKS
        nfw = set_framework
        if supported_frameworks:
            fws = supported_frameworks.split(',')
            if nfw in fws:
                ds.SELENIUM_FRAMEWORK = nfw
                return JSONResponse(status_code=200,
                                    content={
                                        "message":
                                            f'The Selenium framework type has been successfully changed from {cfw} to {nfw}'
                                    })
            else:
                return JSONResponse(status_code=400,
                                    content={
                                        "error": "Unsupported Selenium framework type.",
                                        "supported_frameworks": supported_frameworks
                                    })
        else:
            return JSONResponse(status_code=400,
                                content={
                                    "error": "Unsupported Selenium framework type.",
                                    "supported_frameworks": supported_frameworks
                                })
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f'Error occurred while setting into new framework, {e}')


@app_router.get('/refresh')
def reload_config():
    try:
        log.log_info("Reloading the configuration from Application Environment")
        reset_settings()
        return JSONResponse(status_code=200, content={
            "message": "Configuration re-loaded successfully"
        })
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f'Error occurred while resetting the configuration, {e}')


@app_router.get('/check-sys-error-mail')
def check_system_error_mail():
    try:
        # Simulated failure for testing the system error email alert
        raise ValueError("This is a simulated exception for system error alert testing.")
    except Exception as e:
        stacktrace = traceback.format_exc()
        err = SysErrorModel(type="SimulatedTestError",
                            message=str(e),
                            time=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC'),
                            environment=ds.STAGE,
                            stack_trace=stacktrace,
                            component='API Testing in Application Endpoint'
                            )
        mail_utils.system_error_alert(err.dict())


@app_router.get("/rabbitmq/restart")
def restart_rabbitmq_connection():
    try:
        mq.rabbitmq_connection.reconnect()
        return JSONResponse(status_code=200, content={
            "status": "success",
            "message": "RabbitMQ connection restarted successfully"
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )
