from tkinter import *
from tkinter import ttk
import socket
import threading
from PIL import Image, ImageTk
import time

client_socket = None

def receive_messages():
    global client_socket
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                history = str(message_history_box.get("1.0", "end-1c")) + f"{message}\n"
                message_history_box.config(state=NORMAL)
                message_history_box.delete("1.0", "end")
                message_history_box.insert("1.0", history)
                message_history_box.config(state=DISABLED)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def setup_connection():
    global client_socket
    server_ip = server_ip_box.get("1.0", "end-1c").strip()
    if server_ip:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, 50000))
            start_thread(receive_messages)
            print("Connected to server at", server_ip)
        except Exception as e:
            print(f"Failed to connect to server: {e}")
    else:
        print("Please enter a valid server IP address.")
    file = open("lastused.txt", "w")
    file.write(server_ip_box.get("1.0", "end-1c"))
    file.close()
    file2 = open("lastuser.txt", "w")
    file2.write(username_box.get("1.0", "end-1c"))
    file2.close()

def send_text(event=None):
    username = username_box.get("1.0", "end-1c")
    global client_socket
    text = text_box.get("1.0", "end-1c").strip()
    usertext = str(username) + ": " + text
    if text:
        client_socket.sendall(usertext.encode())
        text_box.delete("1.0", "end")
        history = str(message_history_box.get("1.0", "end-1c")) + f"\nYou: {text}\n"
        message_history_box.config(state=NORMAL)
        message_history_box.delete("1.0", "end")
        message_history_box.insert("1.0", history)
        message_history_box.config(state=DISABLED)
        time.sleep(0.1)
    if event:
        return "break"

def on_closing():
    global client_socket
    if client_socket:
        client_socket.close()
    root.destroy()

def start_thread(func_name):
    thread = threading.Thread(target=func_name, daemon=True)
    thread.start()

root = Tk()
root.geometry("750x450")
root.title("BedlessChat Alpha 9")
root.configure(background='teal')

server_ip_label = Label(root, text="Server IP:", bg='teal')
server_ip_label.grid(row=0, column=0, sticky='sw', padx=10, pady=10)

server_ip_box = Text(root, height=1, width=15)
server_ip_box.grid(row=1, column=0, sticky='w', padx=10)

username_box_label = Label(root, text="Username", bg='teal')
username_box_label.grid(row=0, column=0, sticky='nw', pady=20, padx=10)

username_box = Text(root, height=1, width=15)
username_box.grid(row=0, column=0, sticky='nw', padx=10)

lastuser = open("lastuser.txt", "r")
username_box.insert("1.0", lastuser.readlines()[0])
lastuser.close()

file = open("lastused.txt", "r")
lastused = file.readlines()[0]
file.close()
server_ip_box.insert("1.0", lastused)

image = Image.open("bedless.png").rotate(-90, expand=True).resize((54, 346), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(image)
label = Label(root, image=photo, bg='teal')
label.image = photo
label.grid(row=0, column=1, sticky='ne')

connect_button = ttk.Button(root, text="Connect", command=setup_connection, style='LimeGreen.TButton')
connect_button.grid(row=2, column=0, sticky='w', padx=10, pady=10)

text_box = Text(root, height=1.5, width=50)
text_box.grid(row=1, column=0, sticky='se')
text_box.bind("<Return>", send_text)

message_history_box = Text(root, height=20, width=50)
message_history_box.grid(row=0, column=0, sticky='ne')
message_history_box.config(state=DISABLED)

button = ttk.Button(root, text="Send", command=send_text, style='LimeGreen.TButton')
button.grid(row=1, column=1, sticky='se')

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

style = ttk.Style()
style.configure('LimeGreen.TButton', padding=(0, 8), background='lime green')

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
