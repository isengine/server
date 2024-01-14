import os
import sys
import socket

SOCKET_PORT = 3990

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

old_stdin = sys.stdin
stdin_file = open('stdin.txt', 'w+')
sys.stdin = stdin_wrapper(stdin_file)

old_stdout = sys.stdout
stdout_file = open('stdout.txt', 'w+')
sys.stdout = stdout_wrapper(stdout_file)
