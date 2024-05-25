import socket
import threading

def handle_client(conn, addr, clients):
    try:
        while True:
            message = conn.recv(1024)
            if not message:
                break
            for client in clients:
                if client != conn:
                    client.sendall(message)
    except Exception as e:
        print(f"Error with client {addr}: {e}")
    finally:
        conn.close()
        clients.remove(conn)
        print(f"Client {addr} disconnected.")
def main():
    host = '0.0.0.0'
    port = 50000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Server listening on {host}:{port}")

    clients = []
    try:
        while True:
            conn, addr = server_socket.accept()
            print(f"Connected by {addr}")
            clients.append(conn)
            threading.Thread(target=handle_client, args=(conn, addr, clients)).start()
    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
