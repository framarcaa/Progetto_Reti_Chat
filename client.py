from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tkt

FORMAT = "utf-8"
SERVER = "localhost"
PORT = 53000
BUFSIZE = 1024
ADDRESS = (SERVER, PORT)
SERVER_OFFLINE = "Attualmente il server è offline"
CLOSING = "{close}"

running = True
username = ""

def send(message):
    try:
        client_socket.send(bytes(message, FORMAT))
    except:
        if message != CLOSING:
            main_text.insert(tkt.END, SERVER_OFFLINE)

def main_pack():
    main_frame.pack(expand=True, fill="both")

def receive():
    while running:
        try:
            message = client_socket.recv(BUFSIZE).decode(FORMAT)
            main_text.insert(tkt.END, message)
        except ConnectionResetError:
            print("Connessione al server interrotta.")
            break
        except Exception:
            pass

def enter(event=None):
    message = main_entry.get()
    main_entry.delete(0, tkt.END)
    send(message)

def on_close():
    global running
    running = False
    send(CLOSING)
    print("Chiusura dell'applicazione.")
    window.destroy()

def start_connection():
    global client_socket
    client_socket = socket(AF_INET, SOCK_STREAM)
    while running:
        try:
            client_socket.connect(ADDRESS)
        except Exception:
            print(SERVER_OFFLINE)
        else:
            send(username)
            print("Connessione al server stabilita.")
            rec = Thread(target=receive)
            rec.start()
            rec.join()

            client_socket = socket(AF_INET, SOCK_STREAM)

def sign_in(event=None):
    global username
    username = main_entry.get()
    if username:
        send(username)
        main_label.config(text=username)
        main_entry.delete(0, tkt.END)
        main_entry.unbind("<Return>")
        main_button.config(command=enter, text="Enter")
        main_entry.bind("<Return>", enter)

if __name__ == "__main__":
    client_socket = ""

    # window creation
    window = tkt.Tk()
    window.geometry("600x450")
    window.title("Chat")

    # main configuration
    main_frame = tkt.Frame(window, background="purple")
    main_label = tkt.Label(main_frame, font=("Consolas", 20), foreground="white", background="purple")
    main_text = tkt.Listbox(main_frame, font=("Consolas", 15))
    main_entry = tkt.Entry(main_frame, font=("Consolas", 15), relief="raised", borderwidth=10)
    main_button = tkt.Button(main_frame, font=("Consolas", 20), relief="raised", borderwidth=10, text="Sign-in", foreground="white", background="purple", command=sign_in)

    main_frame.pack(expand=True, fill="both")
    main_label.pack()
    main_text.pack(expand=True, fill="both")
    main_entry.pack(side="left", expand=True, fill="x", padx=5)
    main_button.pack(side="right")

    main_entry.bind("<Return>", sign_in)

    # window loop start
    Thread(target=start_connection).start()
    window.protocol("WM_DELETE_WINDOW", on_close)
    window.mainloop()
