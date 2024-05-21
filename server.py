from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

FORMAT = "utf-8"
HOST = "localhost"
PORT = 53000
BUFSIZE = 1024
ADDRESS = (HOST, PORT)

clients = {}


def close_client(client, msg, name):
    print(msg)
    client.close()
    del clients[client]
    broadcast(bytes("%s ha abbandonato la chat." % name, FORMAT))

def client_manager(client,client_address):
    try:
        name = client.recv(BUFSIZE).decode(FORMAT)
        if name == "{close}":
            print("%s:%s si è disconnesso." % client_address)
            client.close()
            return
    except ConnectionResetError:
        close_client(client, ("%s:%s si è disconnesso per un problema di connesione." % client_address), name)
    
    msg = "%s si è unito all chat!" % name
    broadcast(bytes(msg, FORMAT))
    clients[client] = name
    
    while True:
        try:
            msg = client.recv(BUFSIZE)
            if msg == bytes("{close}", FORMAT):
                close_client(client, ("%s:%s si è disconnesso." % client_address), name)
                break
            broadcast(msg, name+": ")
        except ConnectionResetError:
            close_client(client, ("%s:%s si è disconnesso per un problema di connesione." % client_address), name)
            break


def server_manager():
    SERVER.bind(ADDRESS)
    SERVER.listen(5)
    print("In attesa di connessioni...")
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s si è connesso." % client_address)
        client.send(bytes("Benvenuto in chatroom! Inserisci il tuo nome!",FORMAT))
        Thread(target=client_manager, args=(client,client_address)).start()

def broadcast(msg, prefisso=""):
    for utente in clients:
        utente.send(bytes(prefisso, FORMAT)+msg)
    
if __name__ == "__main__":
    SERVER = socket(AF_INET, SOCK_STREAM)
    ACCEPT_THREAD = Thread(target=server_manager)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()