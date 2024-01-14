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

sock = socket.socket()
sock.bind(('', SOCKET_PORT))
sock.listen(1)
print("server is run")

conn, addr = sock.accept()
print(f"connected: {addr}")

old_stdout = sys.stdout
sys.stdout = open('log.txt', 'w')
# old_stdin = sys.stdin
# sys.stdin = open(r"in.txt", "r")

while True:
    data = conn.recv(1024)
    print("incoming data!")

    # sys.stdout - стандартный системный поток вывода
    # sys.stdout.write() выводит (записывает) в этот поток (то же, что print())
    # по-умолчанию этот поток направлен в консоль sys.__stdout__
    # но его можно переназначить, например в файл
    # > sys.stdout = open('log.txt', 'w')
    # или в сокет
    
    # sys.stdin - стандартный системный поток ввода
    # по-умолчанию этот поток направлен в консоль sys.__stdin__
    # но его можно переназначить, например в файл
    # > sys.stdin = open(r'in.txt', 'r')
    # или в сокет

    # обычно потоки накапливают данные во внутреннем буфере
    # метод flush() очищает внутренний буфер и перемещает данные из потока в назначение
    # обычно используется только для выходного потока

    # для входного потока используются методы read() и readline()
    # эти методы читают все данные, которые пришли из входного потока
    # и на момент вызова метода уже находятся в буфере
    # почти , только эти методы не блокируют выполнение программы
    # метод read() читает все данные и очищает весь буфер
    # метод readline() читает только одну строку и очищает ее из буфера
    # почти то же, что input(), только в input(prompt) можно передать строку,
    # которая запишется в sys.stdout (в консоль или куда он перенаправлен)


    sys.stdout.write(data.decode())
    sys.stdout.flush()
    sys.__stdout__.write(data.decode()) # выводит только в консоль
    sys.__stdout__.flush()
    line = input("input data:")
    print(line)
    print("stdin data!")
    # read = sys.stdin.read() # считывает все и освобождает буфер
    read = sys.stdin.readline() # считывает одну строку и освобождает ее из буфера (предыдущую освободил input)
    # sys.stdin.flush()
    # sread = sys.__stdin__.read() # считывает все и освобождает буфер
    # sread = sys.__stdin__.readline() # считывает
    # sys.__stdin__.flush()
    print(f"stdin: {read}") # read - все
    # print(f"_stdin_: {sread}") # read - ничего, пусто
    # print(f"incoming data: {data}")
    sys.stdout.flush()
    sys.__stdout__.flush()

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
            stdin = sys.stdin,
            stdout = sys.stdout,
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
                # print(f"stdout: {sys.stdout.getValue()}")
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