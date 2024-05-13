import socket
import threading
import time

HOST = "localhost"  # Dirección del servidor
PORT = 8000  # Puerto del servidor

clientes = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea un socket TCP
server.bind((HOST, PORT))  # Asocia el socket a la dirección y puerto
server.listen(5)  # Pone el socket en modo escucha
print("[SERVIDOR] Servidor iniciado")


def enviarMensaje(mensaje, cliente):
    try:
        for otro_cliente in clientes:
            if otro_cliente != cliente:
                otro_cliente.sendall(mensaje.encode("utf-8"))
    except:
        print("error")

def atender_cliente(cliente):
    while True:
        try:
            # Recibe el mensaje del cliente
            mensaje = cliente.recv(1024).decode("utf-8")
            print(f"[CLIENTE {nombre}] {mensaje}")
        except:
            # Si hay un error, cierra la conexión con el cliente
            cliente.close()
            for i in range(0, len(clientes)):
                if cliente == clientes[i]:
                    clientes.pop(i)

            enviarMensaje(f"[{nombre} se ha desconectado]", cliente)
            print(f"[CLIENTE {nombre} desconectado]")
            break

while True:
    try:
        # Acepta una conexión entrante del cliente
        cliente, direccion = server.accept()
        print(f"[CONEXIÓN] Cliente conectado desde {direccion}")

        clientes.append(cliente)

        # Crea un hilo para atender al cliente
        hilo_cliente = threading.Thread(target=atender_cliente, args=(cliente,))
        hilo_cliente.start()
    except:
        print("error 1")
