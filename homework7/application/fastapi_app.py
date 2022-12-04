#!/usr/local/bin python3

import os
import requests
import uvicorn
from fastapi import FastAPI, status, BackgroundTasks, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class User(BaseModel):
    name: str
    surname: str | None = None
    age: int | None = None
    user_id: int | None = None


class Color(BaseModel):
    color: str


app_data = {}
user_id_seq = 1

app = FastAPI()


def write_log(message: str):
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../tmp/log.txt')), mode='a') as log:
        log.write(message)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post('/add_user', status_code=201)
async def create_user(user: User, background_tasks: BackgroundTasks, request: Request):
    global user_id_seq

    if user.name not in app_data:
        app_data[user.name] = user_id_seq
        user_id_seq += 1
        content = {'user_id': app_data[user.name], 'user_name': user.name, 'user_surname': user.surname,
                   'user_age': user.age}
        message = f"{status.HTTP_201_CREATED}, {request.headers}, {await request.body()}, {content} \n"
        background_tasks.add_task(write_log, message)
        return content

    else:
        content = f'User_name {user.name} already exists: id: {app_data[user.name]}'
        message = f"{status.HTTP_400_BAD_REQUEST}, {request.headers}, {await request.body()}, {content} \n"
        background_tasks.add_task(write_log, message)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)


@app.get('/get_user/{name}')
async def get_user_id_by_name(name, background_tasks: BackgroundTasks, request: Request):

    if user_id := app_data.get(name):
        age_host = os.environ['STUB_HOST']
        age_port = os.environ['STUB_PORT']

        age = None
        try:
            age = requests.get(f'http://{age_host}:{age_port}/get_age/{name}').json()
        except Exception as e:
            print(f'Unable to get age from external system:\n{e}')

        surname_host = os.environ['MOCK_HOST']
        surname_port = os.environ['MOCK_PORT']

        surname = None
        try:
            response = requests.get(f'http://{surname_host}:{surname_port}/get_surname/{name}')
            if response.status_code == 200:
                surname = response.json()
        except Exception as e:
            print(f'Unable to get surname from external system:\n{e}')
        print(f'No surname found for user {name}')
        data = {'user_id': user_id,
                'age': age,
                'surname': surname}

        message = f"{status.HTTP_200_OK}, {request.headers}, {await request.body()}, {data} \n"
        background_tasks.add_task(write_log, message)
        return data

    else:
        content = f'User_name {name} not found'
        message = f"{status.HTTP_404_NOT_FOUND}, {request.headers}, {await request.body()}, {content} \n"
        background_tasks.add_task(write_log, message)
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=content)


@app.put('/update_user_fav_color/{name}')
async def update_user_fav_color(name, color: Color, background_tasks: BackgroundTasks, request: Request):
    if user_id := app_data.get(name):
        color_host = os.environ['MOCK_HOST']
        color_port = os.environ['MOCK_PORT']
        color_resp = requests.put(f'http://{color_host}:{color_port}/update_user_fav_color/{name}',
                                  json={'color': color.color})
        if color_resp.status_code == 200:
            data = {
                'user_id': user_id,
                'fav_color': color_resp.json()
            }
            message = f"{status.HTTP_200_OK}, {request.headers}, {await request.body()}, {data} \n"
            background_tasks.add_task(write_log, message)
            return data
        elif color_resp.status_code == 400:
            content = f'Color {color.color} not acceptable'
            message = f"{status.HTTP_400_BAD_REQUEST}, {request.headers}, {await request.body()}, {content} \n"
            background_tasks.add_task(write_log, message)
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
    else:
        content = f'User_name {name} not found'
        message = f"{status.HTTP_404_NOT_FOUND}, {request.headers}, {await request.body()}, {content} \n"
        background_tasks.add_task(write_log, message)
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=content)


@app.delete('/delete_user_age/{name}')
async def delete_user_age(name, background_tasks: BackgroundTasks, request: Request):
    if user_id := app_data.get(name):
        delete_host = os.environ['MOCK_HOST']
        delete_port = os.environ['MOCK_PORT']
        delete_resp = requests.delete(f'http://{delete_host}:{delete_port}/delete_user_age/{name}').json()
        message = f"{status.HTTP_200_OK}, {request.headers}, {await request.body()}\n"
        background_tasks.add_task(write_log, message)
        return delete_resp
    else:
        content = f'User_name {name} not found'
        message = f"{status.HTTP_404_NOT_FOUND}, {request.headers}, {await request.body()}, {content} \n"
        background_tasks.add_task(write_log, message)
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=content)


if __name__ == "__main__":
    host = os.environ.get('APP_HOST', '127.0.0.1')
    port = os.environ.get('APP_PORT', '8083')

    uvicorn.run(app, host=host, port=port)
