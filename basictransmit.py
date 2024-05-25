import socket

def send_message(message, address='127.0.0.1', port=8383):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (address, port))
    sock.close()
if __name__ == "__main__":
    address = '127.0.0.1'
    port = 8383
    
    while True:
        message = input("Enter message to send (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        send_message(message, address, port)
        print(f"Message '{message}' sent to {address}:{port}")
