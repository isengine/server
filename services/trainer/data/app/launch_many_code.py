import os
import sys
from subprocess import Popen, PIPE, TimeoutExpired
from types import SimpleNamespace
import io

from aiohttp import web
import aiohttp_cors
from serverhub_agent.utils.filesystem import TempFileManager

from threading import Thread

import socket

AGENT_PORT = os.getenv("PORT")
SOCKET_PORT = int(os.getenv("SOCKET"))
# TIMEOUT = int(os.getenv("TIMEOUT"))
TIMEOUT = 60
TESTS_PATH = "/home/student/tests/"

# sock = socket.socket()
# sock.bind(('', SOCKET_PORT))
# sock.listen(1)
# conn = sock.accept()
# print("socket connection is ready")

async def run(request: web.Request) -> web.Response:
    body = await request.json()
    files = [
        SimpleNamespace(name = f["name"], content = f["content"]) for f in body["files"]
    ]
    timeout = False
    return_code = 1
    oom_killed = False

    # global conn

    with TempFileManager(directory = TESTS_PATH, files = files) as manager:
        with Popen(
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
        ) as proc:

            # line = proc.stdout.readline()
            # print(f">>> {line}")
            # sys.stdout.flush()

            # line = io.BytesIO(sys.stdout)
            # print(f"::: {line}")
            # sys.stdout.flush()

            proc.stdin.write("1\n")
            sys.stdout.flush()

            proc.stdin.write("2\n")
            sys.stdout.flush()

            # with open(sys.stdout, 'r') as f2:
            #     lines = f2.read()
            #     print(f"lines")
            # sys.stdout.flush()

            # while True:
            #     if (proc.poll() != None):
            #         break
            #     line = proc.stdout.readline()
            #     pline = f">>> {line}"
            #     print(pline)
            #     try:
            #         conn.sendall(pline.encode())
            #     except:
            #         pass
            #     proc.stdout.flush()
            #     # try:
            #     #     data = conn.recv(1024).decode()
            #     #     proc.stdin.write(data)
            #     # except:
            #     #     pass
            #     # proc.stdout.flush()

            # proc.stdout.flush()
            # if proc.poll() == None:
            #     print(f"--> nopoll")
            # else:
            #     print(f"--> poll {proc.poll()}")
            # proc.stdout.flush()

            try:
                std_out, std_err = proc.communicate(
                    # input = '\n'.join(body.get("stdin", [])),
                    # input = '4',
                    timeout = TIMEOUT,
                )

                # if proc.poll() == None:
                #     print(f"x-> nopoll")
                # else:
                #     print(f"x-> poll {proc.poll()}")

                # for line in std_out.splitlines():
                #     print(">>> " + line)
                #     try:
                #         conn.sendall(f">>> {line}".encode())
                #     except:
                #         pass
                #     sys.stdout.flush()

                for line in std_out.splitlines():
                    print(">>> " + line)
                    sys.stdout.flush()

                if (std_err):
                    print("ERROR: " + std_err)
                    # try:
                    #     conn.sendall(f"ERROR: {std_err}".encode())
                    # except:
                    #     pass
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