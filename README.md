# Ejercicio de sockets con python

Testeo de sockets en python haciendo diferentes versiones de un simple programa de mensajeria

# Explicacion del codigo del cliente

El codigo del cliente inicia intentando conectarse al servidor. Una vez establedida la conexion, crea el hilo para recibir mensajes del servidor. De esta forma se pueden recibir mensajes del servidor en cualquier momento.  Luego, entra al bucle principal. En este le pide que ingrese un mensaje para luego mandarselo a servidor.  

Este codigo de cliente puede ser reutilizado con cualquier servidor

```python

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

```

# Explicacion del codigo del servidor 

## Inicio de ejecucion:

El inicio de la ejecucion es identico en todas las versiones del codigo.

```python
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
```

El codigo del servidor inicia importando las librerias de socket y threading.
La libreria de sockets permite la comunicacion de diferentes procesos a travez del protocolo tcp/ip 
La libreria de threading permite la ejecucion pararlela de diferentes funciones del codigo.
La lista de clientes es usada posteriormente para mantener una conexion de multiples clientes y comunicancion entre ellos
La variable server va a representar el socket abierto por el servidor donde luego se establecera en la ip HOST y puerto PORT y se pondra en modo de escucha
Se envia un simple mensaje indicando el inicio de la ejecucion del servidor

## Comunicacion entre clientes por servidor
En esta version del codigo, multiples clientes pueden conectarse a un mismo servidor para poder comunicarse entre si. 

### Bucle principal:

```python
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
```

En el bucle principal el servidor escanea el socket hasta que detecta un intento de conexion de un cliente. Una vez detectada automaticamente la acepta, añade su cliente a la lista de clientes y crea un hilo para este. 

### Hilo de cliente:

```python
    def atender_cliente(cliente):
        nombre = cliente.recv(1024).decode("utf-8")
        print(f"[CLIENTE {nombre} conectado]")
        respuesta = f"Tu nombre es {nombre}"
        cliente.sendall(respuesta.encode("utf-8"))
        enviarMensaje(f"[{nombre} se ha conectado]", cliente)
        while True:
            try:
                # Recibe el mensaje del cliente
                mensaje = cliente.recv(1024).decode("utf-8")
                print(f"[CLIENTE {nombre}] {mensaje}")
                enviarMensaje(f"[{nombre}] {mensaje}", cliente)
            except:
                # Si hay un error, cierra la conexión con el cliente
                cliente.close()
                for i in range(0, len(clientes)):
                    if cliente == clientes[i]:
                        clientes.pop(i)

                enviarMensaje(f"[{nombre} se ha desconectado]", cliente)
                print(f"[CLIENTE {nombre} desconectado]")
                break
```

Cada vez que un cliente se conecta se crea una nueva instancia de este hilo.
Al iniciarse el hilo cliente escucha por el nombre del cliente. Este sera el que se ussara para comunicar al resto de clientes el dueño del mensaje.
Al recibir el nombre se notifica a todo el resto de los clientes la conexion y el nombre del nuevo cliente.

### Bucle del cliente:
El bucle del cliente consiste en la ecucha de cualquier mensaje enviado por este seguido por el envio de este a todos los otros clientes.
Cuando el cliente cierra la conexion con el servidor se detecta una exepcion, se comunica a todos los clientes la desconexion y cierra la conexion con el cliente.

## Bitacora
En esta version del codigo, un solo cliente puede enviar mensajes infinitos hacia el servidor sin necesitar respuesta de este. El servidor se remite a mostrar los mensajes por pantalla.

### Bucle principal:
El servidor escucha por un mensaje del cliente para luego imprimirlos en pantalla.

```python
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
```

## Mensaje por turnos
En esta version del codigo, el servidor y el cliente se turnan para enviarse mensajes el uno al otro 
El servidor escucha por un mensaje del cliente. Recien cuando se recibe se pide un mensaje para enviar al cliente

```python
    def atender_cliente(cliente):
        while True:
            try:
                # Recibe el mensaje del cliente
                mensaje = cliente.recv(1024).decode("utf-8")
                print(f"[CLIENTE {nombre}] {mensaje}")
                mensaje = str(input("ingrese mensaje para el cliente"))
                enviarMensaje(f"[{nombre}] {mensaje}", cliente)
            except:
                # Si hay un error, cierra la conexión con el cliente
                cliente.close()
                for i in range(0, len(clientes)):
                    if cliente == clientes[i]:
                        clientes.pop(i)

                enviarMensaje(f"[{nombre} se ha desconectado]", cliente)
                print(f"[CLIENTE {nombre} desconectado]")
                break
```
