import os
import sys
from subprocess import Popen, PIPE, TimeoutExpired
from types import SimpleNamespace

from aiohttp import web
import aiohttp_cors
from serverhub_agent.utils.filesystem import TempFileManager

import socket

AGENT_PORT = os.getenv("PORT")
SOCKET_PORT = int(os.getenv("SOCKET"))
TIMEOUT = int(os.getenv("TIMEOUT"))
TESTS_PATH = "/home/student/tests/"

old_stdout = sys.stdout
sys.stdout = open('log.txt', 'w')

# r, w = os.pipe()
# stdinr, stdinw = os.fdopen(r, 'rb'), os.fdopen(w, 'wb')

# fd = os.open("in.txt", os.O_RDWR|os.O_CREAT)
# new_stdin = os.fdopen(fd, 'w+')
# old_stdin = sys.stdin
# sys.stdin = new_stdin

# stdinf = open('in.txt', 'wb+')
# stdinf = os.open("in.txt", 'wb+')
stdinw = open('in.txt', 'w+')
# stdinr = open('in.txt', 'r+')

old_stdin = sys.stdin
sys.stdin = stdinw

sock = socket.socket()
sock.bind(('', SOCKET_PORT))
sock.listen(1)
print("server is run")

conn, addr = sock.accept()
print(f"connected: {addr}")

# old_stdin = sys.stdin
# sys.stdin = open(r"in.txt", "r")

sys.stdout.flush()

while True:
    data = conn.recv(1024).decode()
    print("incoming data!")

    sys.stdout.write(data)
    print("stdin:")

    pos = sys.stdin.tell()
    sys.stdin.write(data)
    sys.stdin.seek(pos)

    line = input("input data:")
    print(line)

    # read = sys.stdin.readline()
    # print(f"read data: {read}")

    sys.stdout.flush()

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