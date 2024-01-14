import asyncio
import logging
import os
import subprocess
from types import SimpleNamespace
from typing import List

from aiohttp import web
import aiohttp_cors
from serverhub_agent.utils.filesystem import TempFileManager

import sys

AGENT_PORT = os.getenv("PORT")
TIMEOUT = int(os.getenv("TIMEOUT"))
TESTS_PATH = "/home/student/tests/"

async def run(request: web.Request) -> web.Response:
    body = await request.json()
    files = [
        SimpleNamespace(name=f["name"], content=f["content"]) for f in body["files"]
    ]
    timeout = False
    return_code = 1
    oom_killed = False
    
    async with run_lock:
        with TempFileManager(directory = TESTS_PATH, files = files) as manager:
            with subprocess.Popen(
                (
                    f"chown -R student {manager.directory} "
                    f"&& chown -R student /tmp/ "
                    f"&& chown -R student /home/student/ "
                    f"&& su - student -c \"cd {manager.directory} "
                    f"&& {body['command']}\" "
                ),
                stdin = subprocess.PIPE, 
                stdout = subprocess.PIPE, 
                stderr = subprocess.PIPE,
                text = True,
                shell = True,
                encoding = 'utf-8',
            ) as proc:
                try:
                    # proc.stdin.write('1')
                    proc.stdin.write('4')
                    # proc.stdin.flush()
                    # proc.wait()
                    # proc.wait()
                    std_out, std_err = proc.communicate(
                        # input = '\n'.join(body.get("stdin", [])),
                        # input = '6',
                        timeout = TIMEOUT,
                    )
                    for line in std_out.splitlines():
                        print(">>> " + line)
                        sys.stdout.flush()
                    # print(f"stdout {std_out}")
                    return_code = proc.returncode
                except subprocess.TimeoutExpired:
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

    return web.json_response(result)

app = web.Application()
cors = aiohttp_cors.setup(app)

resource = cors.add(app.router.add_resource("/run"))
route = cors.add(
    resource.add_route("POST", run), {
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials = True,
            expose_headers = ("X-Custom-Server-Header",),
            allow_headers = ("X-Requested-With", "Content-Type"),
            max_age = 3600,
        )
    })

run_lock = asyncio.Lock()
logging.basicConfig(level=logging.DEBUG)

web.run_app(
    app,
    host="0.0.0.0",
    port=AGENT_PORT,
)