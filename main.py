from tkinter import *
from tkinter import ttk
import socket
import threading
from PIL import Image, ImageTk
import time
import pyaudio
import wave

client_socket = None
window_focused = False

def message_sound():
    if window_focused == False:
        play_wave('sound.wav')
    else:
        pass

def joinmsg():
    username = username_box.get("1.0", "end-1c").strip()
    text_to_send = str(username) + " has joined the chat."
    client_socket.sendall(text_to_send.encode())

def leavemsg():
    username = username_box.get("1.0", "end-1c").strip()
    text_to_send = str(username) + " has left the chat."
    client_socket.sendall(text_to_send.encode())

def play_wave(filename):
    # Open the wave file
    wf = wave.open(filename, 'rb')

    # Create a PyAudio object
    p = pyaudio.PyAudio()

    # Check for default output device
    if p.get_default_output_device_info() is None:
        print("No default output device available.")
        p.terminate()
        return

    try:
        # Open a stream on the correct format
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        # Read data in chunks
        chunk_size = 1024
        data = wf.readframes(chunk_size)

        # Play the sound by writing the audio data to the stream
        while data:
            stream.write(data)
            data = wf.readframes(chunk_size)

    except Exception as e:
        print(f"Failed to play sound: {e}")

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf.close()

def on_focus_in(event):
    global window_focused
    window_focused = True

def on_focus_out(event):
    global window_focused
    window_focused = False

def receive_messages():
    global client_socket
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                message_sound()
                message_history_box.config(state=NORMAL)
                message_history_box.insert(END, f"\n{message}")
                message_history_box.config(state=DISABLED)
                message_history_box.see(END)  # Scroll to the end
        except Exception as e:
            output_to_box(f"\nError receiving message: {e}\n")
            break

def setup_connection():
    disconnect_silent()
    global client_socket
    server_ip = server_ip_box.get("1.0", "end-1c").strip()
    if server_ip:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, 50000))
            start_thread(receive_messages)
            output_to_box(str("\nConnected to server at " + server_ip + "."))
        except Exception as e:
            output_to_box(f"\nFailed to connect to server: {e}\n")
    else:
        output_to_box("\nPlease enter a valid server IP address.\n")
    file = open("lastused.txt", "w")
    file.write(server_ip_box.get("1.0", "end-1c"))
    file.close()
    file2 = open("lastuser.txt", "w")
    file2.write(username_box.get("1.0", "end-1c"))
    file2.close()
    global socketopen
    socketopen = True
    joinmsg()


def send_text(event=None, message=None):
    username = username_box.get("1.0", "end-1c")
    global client_socket
    if message is None:
        text = text_box.get("1.0", "end-1c").strip()
        usertext = str(username).strip("\n") + ": " + text
    else:
        text = message.strip()
        usertext = str(username).strip("\n") + " " + text
    if text:
        client_socket.sendall(usertext.encode())
        if message is None:
            text_box.delete("1.0", "end")
        message_history_box.config(state=NORMAL)
        message_history_box.insert(END, f"\nYou: {text}")
        message_history_box.config(state=DISABLED)
        message_history_box.see(END)  # Scroll to the end
    if event:
        return "break"

def disconnect():
    global client_socket
    if client_socket:
        global socketopen
        if socketopen == True:
            leavemsg()
            client_socket.close()
            output_to_box("\nDisconnected from server.\n")
            socketopen = False
        else:
            output_to_box("\nNo open server connections were found.\n")

def disconnect_silent():
    global client_socket
    if client_socket:
        global socketopen
        if socketopen == True:
            client_socket.close()
            socketopen = False
        else:
            pass

def on_closing():
    leavemsg()
    global client_socket
    if client_socket:
        client_socket.close()
    root.destroy()

def start_thread(func_name):
    thread = threading.Thread(target=func_name, daemon=True)
    thread.start()

def output_to_box(toprint):
    message_history_box.config(state=NORMAL)
    message_history_box.insert(END, toprint)
    message_history_box.config(state=DISABLED)
    message_history_box.see(END)

root = Tk()
root.geometry("750x450")
root.title("BedlessChat Release 1.0.2")
root.configure(background='teal')
root.bind("<FocusIn>", on_focus_in)
root.bind("<FocusOut>", on_focus_out)

server_ip_label = Label(root, text="Server IP:", bg='teal')
server_ip_label.grid(row=0, column=0, sticky='sw', padx=10, pady=10)

server_ip_box = Text(root, height=1, width=15, bg='orange')
server_ip_box.grid(row=1, column=0, sticky='w', padx=10)

username_box_label = Label(root, text="Username", bg='teal')
username_box_label.grid(row=0, column=0, sticky='nw', pady=20, padx=10)

username_box = Text(root, height=1, width=15, bg='green')
username_box.grid(row=0, column=0, sticky='nw', padx=10)

lastuser = open("lastuser.txt", "r")
username_box.insert("1.0", lastuser.readlines()[0])
lastuser.close()

file = open("lastused.txt", "r")
lastused = file.readlines()[0]
file.close()
server_ip_box.insert("1.0", lastused)

image = Image.open("bedless.png").rotate(-90, expand=True).resize((54, 346))
photo = ImageTk.PhotoImage(image)
label = Label(root, image=photo, bg='teal')
label.image = photo
label.grid(row=0, column=1, sticky='ne')

connect_button = ttk.Button(root, text="Connect", command=setup_connection, style='LimeGreen.TButton')
connect_button.grid(row=2, column=0, sticky='w', padx=10, pady=10)

text_box = Text(root, height=1.5, width=60, bg='light blue')
text_box.grid(row=2, column=0, sticky='se')
text_box.bind("<Return>", send_text)

message_history_box = Text(root, height=35, width=60, bg='gray')
message_history_box.grid(row=0, column=0, sticky='ne')
message_history_box.config(state=DISABLED)

button = ttk.Button(root, text="Send", command=send_text, style='LimeGreen.TButton')
button.grid(row=2, column=1, sticky='se')

disconnectbutton = ttk.Button(root, text="Disconnect", command=disconnect, style='LimeGreen.TButton')
disconnectbutton.grid(row=0, column=0, sticky='sw', padx=10, pady=40)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

style = ttk.Style()
style.configure('LimeGreen.TButton', padding=(0, 8), background='lime green')

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()

