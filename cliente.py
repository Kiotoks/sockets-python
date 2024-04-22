import socket
import threading

HOST = "localhost"  # Dirección del servidor
PORT = 8000  # Puerto del servidor

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea un socket TCP
cliente.connect((HOST, PORT))  # Se conecta al servidor

def recibir_mensajes():
    while True:
        try:
            # Recibe mensajes del servidor
            mensaje = cliente.recv(1024).decode("utf-8")
            print(mensaje)
        except:
            # Si hay un error, cierra la conexión con el servidor
            cliente.close()
            print("Conexión con el servidor cerrada.")
            break

# Inicia un hilo para recibir mensajes en segundo plano
hilo_recepcion = threading.Thread(target=recibir_mensajes)
hilo_recepcion.start()

mensaje = input("Ingrese su nombre: ")
cliente.sendall(mensaje.encode("utf-8"))

while True:
    # Pide al usuario que ingrese un mensaje
    mensaje = input("")
    # Envía el mensaje al servidor
    cliente.sendall(mensaje.encode("utf-8"))