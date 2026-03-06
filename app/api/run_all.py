import subprocess
import sys
import time

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
            "127.0.0.1",
            "--port",
            "8000",
        ]
    )

