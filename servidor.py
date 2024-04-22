import socket
import threading

HOST = "localhost"  # Dirección del servidor
PORT = 8000  # Puerto del servidor

clientes = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea un socket TCP
server.bind((HOST, PORT))  # Asocia el socket a la dirección y puerto
server.listen(5)  # Pone el socket en modo escucha
print("[SERVIDOR] Servidor iniciado")
def atender_cliente(cliente):
    nombre = cliente.recv(1024).decode("utf-8")
    print(f"[CLIENTE {nombre}]")
    respuesta = f"Tu nombre es {nombre}"
    cliente.sendall(respuesta.encode("utf-8"))
    while True:
        try:
            # Recibe el mensaje del cliente
            mensaje = cliente.recv(1024).decode("utf-8")
            print(f"[CLIENTE {nombre}] {mensaje}")

            for otro_cliente in clientes:
                if otro_cliente != cliente:
                    otro_cliente.sendall(f"[{nombre}] {mensaje}".encode("utf-8"))
        except:
            # Si hay un error, cierra la conexión con el cliente
            cliente.close()
            print(f"[CLIENTE {nombre} desconectado]")
            break

while True:
    # Acepta una conexión entrante del cliente
    cliente, direccion = server.accept()
    print(f"[CONEXIÓN] Cliente conectado desde {direccion}")

    clientes.append(cliente)

    # Crea un hilo para atender al cliente
    hilo_cliente = threading.Thread(target=atender_cliente, args=(cliente,))
    hilo_cliente.start()
