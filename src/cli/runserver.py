import os
from src import BASE_DIR
import click


@click.command(name="runserver")
@click.option("--host", default="0.0.0.0", help="The host to bind the server to.")
@click.option("--port", default=8000, help="The port to run the server on.")
def runserver(host: str, port: int):
    """Run the server with specified host and port."""
    os.system(f"cd {BASE_DIR.parent} && uvicorn app:app --host {host} --port {port}")
