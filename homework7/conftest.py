import os
import signal
import subprocess
import time
from copy import copy

import pytest
import requests
from requests.exceptions import ConnectionError as ConErr

import settings


@pytest.fixture(scope='session')
def repo_root_fix():
    repo_root_fix = os.path.abspath(os.path.join(__file__, os.pardir))
    return repo_root_fix


repo_root = os.path.abspath(os.path.join(__file__, os.pardir))


def wait_ready(host, port):
    started = False
    st = time.time()
    while time.time() - st <= 10:
        try:
            time.sleep(2)
            requests.get(f'http://{host}:{port}')
            started = True
            break
        except (ConnectionError, ConErr):
            pass

    if not started:
        raise RuntimeError('App did not start in 10s!')


def pytest_configure(config):
    def make_temp(server):
        file_stderr = os.path.join(repo_root, 'tmp', f'{server}_stderr.txt')
        file_stdout = os.path.join(repo_root, 'tmp', f'{server}_stdout.txt')
        os.makedirs(os.path.dirname(file_stderr), exist_ok=True)
        os.makedirs(os.path.dirname(file_stdout), exist_ok=True)
        stderr = open(file_stderr, 'w+')
        stdout = open(file_stdout, 'w+')
        return stderr, stdout

    def make_env(server_settings_host, server_settings_port):
        env = copy(os.environ)
        env.update({'APP_HOST': server_settings_host, 'APP_PORT': server_settings_port})
        return env

    if not hasattr(config, 'workerinput'):

        # fastapi app configuration

        app_path = os.path.join(repo_root, 'application', 'fastapi_app.py')

        env = make_env(server_settings_host=settings.APP_HOST, server_settings_port=settings.APP_PORT)
        env.update({'STUB_HOST': settings.STUB_HOST, 'STUB_PORT': settings.STUB_PORT})
        env.update({'MOCK_HOST': settings.MOCK_HOST, 'MOCK_PORT': settings.MOCK_PORT})

        app_stderr, app_stdout = make_temp('app')

        app_proc = subprocess.Popen(['python3', app_path],
                                    stderr=app_stderr, stdout=app_stdout, env=env
                                    )
        config.app_proc = app_proc
        config.app_stderr = app_stderr
        config.app_stdout = app_stdout
        wait_ready(settings.APP_HOST, settings.APP_PORT)

        # fastapi stub configuration

        stub_path = os.path.join(repo_root, 'stub', 'fastapi_stub.py')

        env = make_env(server_settings_host=settings.STUB_HOST, server_settings_port=settings.STUB_PORT)
        stub_stderr, stub_stdout = make_temp('stub')

        stub_proc = subprocess.Popen(['python3', stub_path],
                                     stderr=stub_stderr, stdout=stub_stdout, env=env
                                     )
        config.stub_proc = stub_proc
        config.stub_stderr = stub_stderr
        config.stub_stdout = stub_stdout
        wait_ready(settings.STUB_HOST, settings.STUB_PORT)

        # fastapi mock configuration

        mock_path = os.path.join(repo_root, 'mock', 'fastapi_mock.py')

        env = make_env(server_settings_host=settings.MOCK_HOST, server_settings_port=settings.MOCK_PORT)
        mock_stderr, mock_stdout = make_temp('mock')

        mock_proc = subprocess.Popen(['python3', mock_path],
                                     stderr=mock_stderr, stdout=mock_stdout, env=env
                                     )
        config.mock_proc = mock_proc
        config.mock_stderr = mock_stderr
        config.mock_stdout = mock_stdout
        wait_ready(settings.MOCK_HOST, settings.MOCK_PORT)


def pytest_unconfigure(config):
    config.app_proc.send_signal(signal.SIGINT)
    exit_code = config.app_proc.wait()
    config.app_stderr.close()
    config.app_stdout.close()
    assert exit_code == 0

    config.stub_proc.send_signal(signal.SIGINT)
    exit_code = config.stub_proc.wait()
    config.stub_stderr.close()
    config.stub_stdout.close()
    assert exit_code == 0

    config.mock_proc.send_signal(signal.SIGINT)
    exit_code = config.mock_proc.wait()
    config.mock_stderr.close()
    config.mock_stdout.close()
    assert exit_code == 0

    if os.path.exists(os.path.join(repo_root, 'tmp', 'save.json')):
        os.remove(os.path.join(repo_root, 'tmp', 'save.json'))
    else:
        print("The file save.json does not exist")
