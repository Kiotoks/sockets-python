import socket
import threading

HOST = "localhost"  # Dirección del servidor
PORT = 8000  # Puerto del servidor

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea un socket TCP
cliente.connect((HOST, PORT))  # Se conecta al servidor

conexionEstablecida = True

def recibir_mensajes():
    while True:
        try:
            # Recibe mensajes del servidor
            mensaje = cliente.recv(1024).decode("utf-8")
            print(mensaje + "\n")
        except:
            # Si hay un error, cierra la conexión con el servidor
            cliente.close()
            global conexionEstablecida 
            conexionEstablecida = False
            print("Conexión con el servidor cerrada.")
            return

# Inicia un hilo para recibir mensajes en segundo plano
hilo_recepcion = threading.Thread(target=recibir_mensajes)
hilo_recepcion.start()

while conexionEstablecida:
    # Pide al usuario que ingrese un mensaje
    mensaje = input("")
    # Envía el mensaje al servidor
    cliente.sendall(mensaje.encode("utf-8"))