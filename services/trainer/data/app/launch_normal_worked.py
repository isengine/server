import os
from subprocess import Popen, PIPE, TimeoutExpired
from types import SimpleNamespace

from aiohttp import web
import aiohttp_cors
from serverhub_agent.utils.filesystem import TempFileManager

AGENT_PORT = os.getenv("PORT")
TIMEOUT = int(os.getenv("TIMEOUT"))
TESTS_PATH = "/home/student/tests/"

async def run(request: web.Request) -> web.Response:
    body = await request.json()
    files = [
        SimpleNamespace(name = f["name"], content = f["content"]) for f in body["files"]
    ]
    timeout = False
    return_code = 1
    oom_killed = False

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
            try:
                std_out, std_err = proc.communicate(
                    input = '\n'.join(body.get("stdin", [])),
                    timeout = TIMEOUT,
                )
                return_code = proc.returncode
            except TimeoutExpired:
                timeout = True
                proc.kill()
                std_out, std_err = proc.communicate()

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