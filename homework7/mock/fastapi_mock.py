#!/usr/local/bin python3

import os
import uvicorn
from fastapi import FastAPI, status, BackgroundTasks, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json


app = FastAPI()


COLORS = ['white', 'black', 'red', 'blue', 'purple']


class Color(BaseModel):
    color: str


def write_log_mock(message: str):
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../tmp/log_mock.txt')), mode='a') as log:
        log.write(message)


@app.get('/get_surname/{name}')
async def get_user_surname(name, background_tasks: BackgroundTasks, request: Request):
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../tmp/save.json')), 'r') as file:
        surname_data = json.load(file)
    if surname := surname_data.get(name):
        message = f"{status.HTTP_200_OK}, {request.headers}, {await request.body()}, {surname} \n"
        background_tasks.add_task(write_log_mock, message)
        return surname
    else:
        content = f'Surname for user "{name}" not found'
        message = f"{status.HTTP_404_NOT_FOUND}, {request.headers}, {await request.body()}, {content} \n"
        background_tasks.add_task(write_log_mock, message)
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=content)


@app.put('/update_user_fav_color/{name}')
async def update_user_fav_color(name: str, color: Color, background_tasks: BackgroundTasks, request: Request):
    if color.color in COLORS:
        content = {name: color.color}
        message = f"{status.HTTP_200_OK}, {request.headers}, {await request.body()}, {content} \n"
        background_tasks.add_task(write_log_mock, message)
        return content
    else:
        content = f'Color {color.color} not acceptable'
        message = f"{status.HTTP_400_BAD_REQUEST}, {request.headers}, {await request.body()}, {content} \n"
        background_tasks.add_task(write_log_mock, message)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)


@app.delete('/delete_user_age/{name}')
async def delete_user_age(name: str, background_tasks: BackgroundTasks, request: Request):
    content = f"User {name}'s age was deleted"
    message = f"{status.HTTP_202_ACCEPTED}, {request.headers}, {await request.body()}, {content} \n"
    background_tasks.add_task(write_log_mock, message)
    return content


if __name__ == "__main__":
    host = os.environ.get('APP_HOST', '127.0.0.1')
    port = os.environ.get('APP_PORT', '8082')

    uvicorn.run(app, host=host, port=port)
