import os
import sys
from subprocess import Popen, PIPE, TimeoutExpired
from types import SimpleNamespace
import time

from aiohttp import web
import aiohttp_cors
from serverhub_agent.utils.filesystem import TempFileManager

import socket

AGENT_PORT = os.getenv("PORT")
SOCKET_PORT = int(os.getenv("SOCKET"))
TIMEOUT = int(os.getenv("TIMEOUT"))
TESTS_PATH = "/home/student/tests/"

class stdout_wrapper:
    def __init__(self, s):
        self.s = s
    def fileno(self):
        return self.s.fileno()
    def flush(self):
        return self.s.flush()
    def read(self):
        return self.s.read()
    def readall(self):
        self.s.seek(0)
        return self.s.read()
    def readline(self):
        return self.s.readline()
    def write(self, str):
        return self.s.write(str)

sock = socket.socket()
sock.bind(('', SOCKET_PORT))
sock.listen(1)
print("server is run")

conn, addr = sock.accept()
print(f"connected: {addr}")

sys.stdout.flush()

class stdin_wrapper:
    def __init__(self, s):
        self.s = s
    def fileno(self):
        return self.s.fileno()
    def flush(self):
        return self.s.flush()
    def read(self):
        return self.s.read()
    def readall(self):
        self.s.seek(0)
        return self.s.read()
    def readline(self):
        global conn
        data = conn.recv(1024).decode()
        pos = self.s.tell()
        self.s.write(data)
        self.s.seek(pos)
        return self.s.readline()
    def write(self, str):
        return self.s.write(str)

async def run(request: web.Request) -> web.Response:
    global stdin_wrapper
    old_stdin = sys.stdin
    stdin_file = open('stdin.txt', 'w+')
    sys.stdin = stdin_wrapper(stdin_file)

    global stdout_wrapper
    old_stdout = sys.stdout
    stdout_file = open('stdout.txt', 'w+')
    sys.stdout = stdout_wrapper(stdout_file)

    body = await request.json()
    files = [
        SimpleNamespace(name = f["name"], content = f["content"]) for f in body["files"]
    ]
    timeout = False
    return_code = 1
    oom_killed = False

    with TempFileManager(directory = TESTS_PATH, files = files) as manager:
        # вроде бы все ок, но я думаю, проблема в том, что stdin/out не переназначаются
        # в подпроцессе Popen
        # можно посмотреть в сторону asyncio.subprocess и asyncio.create_subprocess_shell()
        with Popen(
            (
                f"chown -R student {manager.directory} "
                f"&& chown -R student /tmp/ "
                f"&& chown -R student /home/student/ "
                f"&& su - student -c \"cd {manager.directory} "
                f"&& python /app/std.py "
                f"&& {body['command']}\" "
            ),
            stdin = sys.stdin,
            stdout = sys.stdout,
            # stdin = PIPE,
            # stdout = PIPE,
            stderr = PIPE,
            text = True,
            shell = True,
            encoding = 'utf-8',
        ) as p:
            try:
                std_out, std_err = p.communicate(
                    # input = '\n'.join(body.get("stdin", [])),
                    timeout = TIMEOUT,
                )
                return_code = p.returncode
            except TimeoutExpired:
                timeout = True
                p.kill()
                std_out, std_err = p.communicate()

    # sys.stdout.flush()
    read = sys.stdout.readall()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    print(read)
    sys.stdout.flush()

    result = {
        "exit_code": return_code,
        "stdout": read,
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