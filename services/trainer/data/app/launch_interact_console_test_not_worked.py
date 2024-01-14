import os
import sys
from subprocess import Popen, PIPE, TimeoutExpired
from types import SimpleNamespace

from aiohttp import web
import aiohttp_cors
from serverhub_agent.utils.filesystem import TempFileManager

import socket
import code

AGENT_PORT = os.getenv("PORT")
SOCKET_PORT = int(os.getenv("SOCKET"))
TIMEOUT = int(os.getenv("TIMEOUT"))
TESTS_PATH = "/home/student/tests/"

s = socket.socket()
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', SOCKET_PORT))
s.listen(1)
#c = s.accept()[0] # client socket
c, addr = s.accept()

print(f"connected: {addr}")
sys.stdout.flush()

class sw: # socket wrapper
    def __init__(self, s):
        self.s = s
    def read(self, len):
            return self.s.recv(len)
    def write(self, str):
            return self.s.send(str)
    def readline(self):
            return self.read(256) # lazy implementation for quick testing
c = sw(c)
sys.stdin = c
sys.stdout = c
sys.stderr = c
code.interact() # runs the interactive console

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
        p = Popen(
            (
                f"chown -R student {manager.directory} "
                f"&& chown -R student /tmp/ "
                f"&& chown -R student /home/student/ "
                f"&& su - student -c \"cd {manager.directory} "
                f"&& {body['command']}\" "
            ),
            stdin = sys.stdin,
            stdout = sys.stdout,
            stderr = PIPE,
            text = True,
            shell = True,
            encoding = 'utf-8',
        )
        try:
            # read = sys.stdin.read() # считывает все и освобождает буфер
            # read = sys.stdin.readline() # считывает одну строку и освобождает ее из буфера (предыдущую освободил input)
            # sys.stdin.flush()
            # sread = sys.__stdin__.read() # считывает все и освобождает буфер
            # sread = sys.__stdin__.readline() # считывает
            # sys.__stdin__.flush()
            # print(f"stdin: {read}") # read - все
            # print(f"_stdin_: {sread}") # read - ничего, пусто
            # print(f"incoming data: {data}")
            
            std_out, std_err = p.communicate(
                # input = '\n'.join(body.get("stdin", [])),
                timeout = TIMEOUT,
            )
            return_code = p.returncode
            # print(f"stdout: {sys.stdout.getValue()}")
        except TimeoutExpired:
            timeout = True
            p.kill()
            std_out, std_err = p.communicate()

    result = {
        "exit_code": return_code,
        "stdout": std_out,
        "stderr": std_err,
        "oom_killed": oom_killed,
        "timeout": timeout,
        "duration": 0,
    }

    return web.json_response(result)

app = web.Application()
cors = aiohttp_cors.setup(app)

app.router.add_route("POST", "/run", run)

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