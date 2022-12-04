#!/usr/local/bin python3

import os
import uvicorn
from fastapi import FastAPI, status, BackgroundTasks, Request
from random import randint

app = FastAPI()


def write_log_stub(message: str):
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../tmp/log_stub.txt')), mode='a') as log:
        log.write(message)


@app.get('/get_age/{name}')
async def get_user_age(name: str, background_tasks: BackgroundTasks, request: Request):
    content = randint(18, 105)
    message = f"{status.HTTP_200_OK}, {request.headers}, {await request.body()}, {content} \n"
    background_tasks.add_task(write_log_stub, message)
    return content


if __name__ == "__main__":
    host = os.environ.get('APP_HOST', '127.0.0.1')
    port = os.environ.get('APP_PORT', '8081')

    uvicorn.run(app, host=host, port=port)
