import asyncio
import logging
import os
from subprocess import Popen, PIPE, TimeoutExpired
from types import SimpleNamespace
from typing import List

from aiohttp import web
import aiohttp_cors
from serverhub_agent.utils.filesystem import TempFileManager

import sys

from threading import Thread
from queue import Queue, Empty
import time

import socket

AGENT_PORT = os.getenv("PORT")
SOCKET_PORT = int(os.getenv("SOCKET"))
TIMEOUT = int(os.getenv("TIMEOUT"))
TESTS_PATH = "/home/student/tests/"

sock = socket.socket()
sock.bind(('', SOCKET_PORT))
sock.listen(1)
print("server is run")

conn, addr = sock.accept()
print(f"connected: {addr}")

# while True:
#     data = conn.recv(1024)
#     print(f"incoming data: {data}")
#     if not data:
#         print("no incoming data")
#         break
#     conn.send(data)
#     print(f"now: {addr}")

async def run(request: web.Request) -> web.Response:
    body = await request.json()
    files = [
        SimpleNamespace(name = f["name"], content = f["content"]) for f in body["files"]
    ]
    timeout = False
    return_code = 1
    oom_killed = False

    global conn

    with TempFileManager(directory = TESTS_PATH, files = files) as manager:
        proc = Popen(
            (
                f"chown -R student {manager.directory} "
                f"&& chown -R student /tmp/ "
                f"&& chown -R student /home/student/ "
                f"&& su - student -c \"cd {manager.directory} "
                f"&& {body['command']}\" "
            ),
            stdin = PIPE,
            stdout = PIPE,
            stderr = PIPE,
            text = True,
            shell = True,
            encoding = 'utf-8',
        )

        try:
            std_out, std_err = proc.communicate(
                # input = '\n'.join(body.get("stdin", [])),
                # input = '4',
                timeout = TIMEOUT,
            )
            for line in std_out.splitlines():
                print(">>> " + line)
                conn.sendall(f">>> {line}".encode())
                sys.stdout.flush()
            if (std_err):
                print("ERROR: " + std_err)
                conn.sendall(f"ERROR: {std_err}".encode())
                sys.stdout.flush()
            return_code = proc.returncode
            print(f"return_code > {return_code}")

        except TimeoutExpired:
            timeout = True
            proc.kill()
            std_out, std_err = proc.communicate()

    result = {
        "exit_code": return_code,
        "stdout": std_out,
        "stderr": std_err,
        # "stdout": stdout.decode(),
        # "stderr": stderr.decode(),
        "oom_killed": oom_killed,
        "timeout": timeout,
        "duration": 0,
    }

    # conn.close()
    # print("connection closed")

    return web.json_response(result)

app = web.Application()
cors = aiohttp_cors.setup(app)

app.router.add_route("POST", "/run", run)
app.router.add_route("GET", "/", run)

for route in list(app.router.routes()):
    cors.add(route, {
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials = True,
            expose_headers = ("X-Custom-Server-Header",),
            allow_headers = ("X-Requested-With", "Content-Type"),
            max_age = 3600,
        )
    })

web.run_app(
    app,
    host = "0.0.0.0",
    port = AGENT_PORT,
)