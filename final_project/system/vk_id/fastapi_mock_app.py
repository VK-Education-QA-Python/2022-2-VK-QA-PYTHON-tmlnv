#!/usr/local/bin python3

import random

import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from mysql_client import MysqlClient

app = FastAPI()


@app.get("/vk_id/{username}")
async def get_vk_id(username):
    mysql_client = MysqlClient('vkeducation', 'test_qa', 'qa_test')
    mysql_client.connect()
    user_in_db = mysql_client.execute_query(f'SELECT * FROM test_users WHERE username="{username}";', fetch=True)
    mysql_client.connection.close()
    if len(user_in_db) > 0:
        return {'vk_id': random.randint(1000, 10000)}
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={})


if __name__ == "__main__":
    host = '0.0.0.0'
    port = 8083

    uvicorn.run(app, host=host, port=port)
