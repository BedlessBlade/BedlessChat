import socket
address = '127.0.0.1'
port = 8383
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((address, port))
print(f"Listening for messages on {address}:{port}...")
while True:
    data, addr = sock.recvfrom(1024)
    print(f"Received message from {addr}: {data.decode()}")
