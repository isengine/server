import socket

SOCKET_PORT = int(os.getenv("PORT"))

sock = socket.socket()
sock.bind(('', SOCKET_PORT))
sock.listen(1)
print("server is run")

conn, addr = sock.accept()
print(f"connected: {addr}")

while True:
    # data = conn.recv(1024)
    # print(f"incoming data: {data}")
    # if not data:
    #     print("no incoming data")
    #     break
    data = input()
    conn.sendall(f"{data}".encode())

# conn.close()
# print("connection closed")
