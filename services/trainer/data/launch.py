import asyncio
import logging
import os
import subprocess
from types import SimpleNamespace
from typing import List

from aiohttp import web
from serverhub_agent.utils.filesystem import TempFileManager

AGENT_PORT = os.getenv("PORT")
TIMEOUT = int(os.getenv("TIMEOUT"))
TESTS_PATH = "/home/student/tests/"

async def run(request: web.Request) -> web.Response:
    body = await request.json()
    files = [
        SimpleNamespace(name=f["name"], content=f["content"]) for f in body["files"]
    ]
    stdin = body.get("stdin", [])
    timeout = False
    # stdout = b""
    # stderr = b""
    return_code = 1
    oom_killed = False

    async with run_lock:
        with TempFileManager(directory=TESTS_PATH, files=files) as manager:
            try:
                proc = subprocess.Popen(
                    (
                        f"chown -R student {manager.directory} "
                        f"&& chown -R student /tmp/ "
                        f"&& chown -R student /home/student/ "
                        f"&& su - student -c \"cd {manager.directory} && {body['command']}\" "
                    ),
                    stdin = subprocess.PIPE, 
                    stdout = subprocess.PIPE, 
                    stderr = subprocess.PIPE,
                    text = True,
                    shell = True,
                )
                for input in stdin:
                    proc.stdin.write(str(input) + '\n')
                std_out, std_err = proc.communicate(
                    input = 'data_to_write',
                    timeout = TIMEOUT,
                )
                return_code = proc.returncode

                # proc = subprocess.run(
                #     (
                #         f"chown -R student {manager.directory} "
                #         f"&& chown -R student /tmp/ "
                #         f"&& chown -R student /home/student/ "
                #         f"&& su - student -c \"cd {manager.directory} && {body['command']}\" "
                #     ),
                #     capture_output=True,
                #     timeout=TIMEOUT,
                #     shell=True,
                # )
                # stdout = proc.stdout
                # stderr = proc.stderr
                # return_code = proc.returncode
            except subprocess.TimeoutExpired:
                timeout = True

    result = {
        "exit_code": return_code,
        "stdin": len(stdin),
        "stdout": std_out.strip(),
        "stderr": std_err,
        # "stdout": stdout.decode(),
        # "stderr": stderr.decode(),
        "oom_killed": oom_killed,
        "timeout": timeout,
        "duration": 0,
    }

    return web.json_response(result)

def setup_routes(app: web.Application) -> None:
    app.router.add_post("/run/", run)

app = web.Application()
run_lock = asyncio.Lock()
setup_routes(app)
logging.basicConfig(level=logging.DEBUG)

web.run_app(
    app,
    host="0.0.0.0",
    port=AGENT_PORT,
)