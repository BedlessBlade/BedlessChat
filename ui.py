from tkinter import *
from tkinter import ttk
import socket
import threading
from PIL import Image, ImageTk
import time

address = '10.35.55.230'
port = 8383
issending = False

def receive_messages():
    while True:
        if not issending:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(("0.0.0.0", port))
            data, addr = sock.recvfrom(1024)
            message = data.decode()
            if message:
                history = str(message_history_box.get("1.0", "end-1c")) + f"{addr[0]}: {message}\n"
                message_history_box.config(state=NORMAL)
                message_history_box.delete("1.0", "end")
                message_history_box.insert("1.0", history)
                message_history_box.config(state=DISABLED)

def start_thread(func_name):
    thread = threading.Thread(target=func_name, daemon=True)
    thread.start()

def message_send(message, destination, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (destination, port))
    sock.close()

def send_text():
    global issending
    issending = True
    text = text_box.get("1.0", "end-1c").strip()
    if text:
        message_send(text, address, port)
        text_box.delete("1.0", "end")
        history = str(message_history_box.get("1.0", "end-1c")) + f"\nYou: {text}\n"
        message_history_box.config(state=NORMAL)
        message_history_box.delete("1.0", "end")
        message_history_box.insert("1.0", history)
        message_history_box.config(state=DISABLED)
        time.sleep(0.1)
    issending = False

def addresscheck():
    global address
    while True:
        address = address_box.get("1.0", "end-1c").strip()

root = Tk()
root.geometry("750x400")
root.title("BedlessChat Alpha 9")
root.configure(background='teal')

address_box = Text(root, height=1, width=15)
address_box.grid(row=0, column=0, sticky='nw')
address_box.insert("1.0", address)

text_box = Text(root, height=1.5, width=50)
text_box.grid(row=1, column=0, sticky='se')

start_thread(receive_messages)
start_thread(addresscheck)

image = Image.open("bedless.png").rotate(-90, expand=True).resize((54, 346), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(image)
label = Label(root, image=photo, bg='teal')
label.image = photo
label.grid(row=0, column=1, sticky='ne')

message_history_box = Text(root, height=20, width=50)
message_history_box.grid(row=0, column=0, sticky='ne')
message_history_box.config(state=DISABLED)

button = ttk.Button(root, text="Send", command=send_text, style='LimeGreen.TButton')
button.grid(row=1, column=1, sticky='se')

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

style = ttk.Style()
style.configure('LimeGreen.TButton', padding=(0, 8), background='lime green')

root.mainloop()

