import os

import click
from src import BASE_DIR


@click.command(name="run-worker-healthcheck")
@click.option("--host", default="0.0.0.0", help="The host to bind the server to.")
@click.option("--port", default=8001, help="The port to run the server on.")
def run_worker_healthcheck(host: str, port: int):
    """Run worker healthcheck."""
    os.system(f"cd {BASE_DIR.parent} && uvicorn worker_healthcheck:app --host {host} --port {port}")
