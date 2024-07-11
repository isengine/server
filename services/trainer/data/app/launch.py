import asyncio
import logging
import os
import subprocess
import psutil
import gc
# import resource
from types import SimpleNamespace
from aiohttp import web
import aiohttp_cors
from serverhub_agent.utils.filesystem import TempFileManager

AGENT_PORT = int(os.getenv("PORT"))
TIMEOUT = int(os.getenv("TIMEOUT"))
TESTS_PATH = "/home/student/tests/"

# def set_memory_limit(max_memory_mb):
#     soft, hard = resource.getrlimit(resource.RLIMIT_AS)
#     resource.setrlimit(resource.RLIMIT_AS, (max_memory_mb * 1024 * 1024, hard))

# def set_memory_limit(max_memory_mb):
#     soft_limit = max_memory_mb * 1024 * 1024  # в байтах
#     hard_limit = soft_limit
#     
#     resource_limits = (soft_limit, hard_limit)
#     
#     # Установка ограничения на использование памяти
#     psutil.Process().rlimit(psutil.RLIMIT_AS, resource_limits)

def check_memory_limit(max_memory_mb):
    process = psutil.Process()
    memory_info = process.memory_info()
    if memory_info.rss > max_memory_mb * 1024 * 1024:
        raise MemoryError(f"Process exceeded memory limit of {max_memory_mb} MB")

def kill(proc):
    pid = proc.pid
    process = psutil.Process(pid)
    for p in process.children(recursive=True):
        try:
            p.terminate()
            p.wait()
        finally:
            del p

async def run(request: web.Request) -> web.Response:
    max_memory_mb = 100
    # set_memory_limit(max_memory_mb)
    
    body = await request.json()
    files = [
        SimpleNamespace(name=f["name"], content=f["content"]) for f in body["files"]
    ]
    stdin = body.get("stdin", [])
    
    std_out = f""
    std_err = f"timeout {TIMEOUT} sec"
    exit_code = 0
    limits_error = 0
    
    run_lock = asyncio.Lock()
    
    async with run_lock:
        with TempFileManager(directory=TESTS_PATH, files=files) as manager:
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
                preexec_fn = os.setsid
            )
            
            try:
                check_memory_limit(max_memory_mb)
                
                for input in stdin:
                    proc.stdin.write(str(input) + '\n')
                std_out, std_err = proc.communicate(
                    timeout = TIMEOUT,
                    # input = '\n'.join(body.get("stdin", [])),
                )
                proc.stdout.close()
                exit_code = proc.returncode
            except MemoryError as e:
                kill(proc)
                exit_code = 1
                std_err = f"{e}"
            except asyncio.TimeoutError:
                kill(proc)
                exit_code = 1
            except Exception as e:
                subprocess.call("exit 1", shell = True)
                exit_code = 1
                # kill(proc, TIMEOUT)
                std_err = f"{e}"
        
        proc.terminate()
        proc.kill()
        proc.wait()
        
    result = {
        "exit_code": exit_code,
        "stdin": len(stdin),
        "stdout": std_out.strip(),
        "stderr": std_err,
        "duration": 0,
    }
    
    del stdin
    del std_out
    del std_err
    gc.collect()
    
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
            # max_age = 3600,
        )
    })

# logging.basicConfig(level=logging.DEBUG)

web.run_app(
    app,
    host="0.0.0.0",
    port=AGENT_PORT,
)
