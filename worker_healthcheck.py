"""
Worker healthcheck service

If the worker is banned for any of the services it returns 503.
"""
import logging

import uvicorn
from fastapi import FastAPI, HTTPException
from starlette import status

import json

app = FastAPI()


@app.get("/healthcheck", status_code=status.HTTP_200_OK)
async def healthcheck():
    with open("health.json", "r") as f:
        health = json.load(f)["healthy"]
    if health:
        print(health)
        return {"healthy": True}
    else:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )

    uvicorn.run(app, host="0.0.0.0", port=8001)
