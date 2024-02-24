import sqlite3
import hashlib
import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost",9999))
server.listen()

def handlconnect(client):
    client.send("Username: ".encode())
    username = client.recv(1024).decode()

    client.send("Password: ".encode())
    password = client.recv(1024)
    password = hashlib.sha256(password).hexdigest()

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM database WHERE username= ? AND password= ?",(username,password))

    if cur.fetchall():
        client.send("Identification Réussie".encode())
    else:
        client.send("Identification Échouée".encode())

while True:
    client,adress=server.accept()
    threading.Thread(target=handlconnect,args=(client,)).start()