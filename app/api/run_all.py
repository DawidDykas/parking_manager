import subprocess
import sys
import time
from sqlalchemy.exc import OperationalError
from config.setting import fastapi_settings


def init_db_first_user():
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
    except OperationalError:
        print("Database is existing")

def start_redis():
    return subprocess.Popen(["redis-server"])

def start_celery():
    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "celery",
            "-A",
            "app.celery.celery_drive:celery",
            "worker",
            "--loglevel=info",
            "--pool=solo"
        ]
    )


def start_fastapi():
    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app.api.main:app",
            "--reload",
            "--host",
            fastapi_settings.HOST,
            "--port",
            str(fastapi_settings.PORT),
        ]
    )


def run_all():
    init_db_first_user()
    redis_process = start_redis()
    time.sleep(2)
    celery_process = start_celery()
    time.sleep(2)
    fastapi_process = start_fastapi()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down processes...")
        celery_process.terminate()
        fastapi_process.terminate()
        redis_process.terminate()
        celery_process.wait()
        fastapi_process.wait()
        redis_process.wait()
        print("Processes terminated.")
