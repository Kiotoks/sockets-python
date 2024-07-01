import socket
import threading

HOST = "localhost"  # Dirección del servidor
PORT = 8000  # Puerto del servidor

clientes = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea un socket TCP
server.bind((HOST, PORT))  # Asocia el socket a la dirección y puerto
server.listen(5)  # Pone el socket en modo escucha
print("[SERVIDOR] Servidor iniciado")

productos = [{"nombre": "cocacola", "precio": 12, "q": 0 }, {"nombre": "jorgito", "precio": 6, "q": 0 }, {"nombre": "ayudin", "precio": 4, "q": 0 }, {"nombre": "play5", "precio": 1594467, "q": 0 },]
carrito = []
total = 0
salir = False
metodoPago = 0
carritotxt = ""

def atender_cliente(cliente):
    global productos
    global total
    global salir
    global metodoPago
    totalPropio = 0 
    global carrito
    global carritotxt
    texto = ""
    while True:
        try:
            # Recibe el mensaje del cliente
            if not texto:
                texto = f"Elija el producto para añadir al carrito (O elija 0 para terminar compra)"
                for i in range(len(productos)):
                   producto = productos[i]
                   texto += ( "\n" + str(i+1) + "- " +  producto["nombre"] + " : $" + str(producto["precio"]))
            
            cliente.sendall(texto.encode("utf-8"))
            numero = int(cliente.recv(1024).decode("utf-8"))

            if numero == 0 or salir:
                if salir:
                    cliente.sendall("Otro cliente cerro la compra".encode("utf-8"))
                else:
                    salir = True
                    cliente.sendall(carritotxt.encode("utf-8"))
                    cliente.sendall("Elija como va a pagar \n1- Dividir equitativamente \n2 Pagar solo lo agregado".encode("utf-8"))
                    metodoPago = int(cliente.recv(1024).decode("utf-8"))
                
                if metodoPago == 1:
                   final = total/len(clientes)
                else: 
                    final = totalPropio 

                cliente.sendall(f"\nTotal: {final} \n Cuanto pagas:".encode("utf-8"))
                numero = int(cliente.recv(1024).decode("utf-8"))

                if total > numero:
                    cliente.sendall(f"No es suficiente para pagar el total del carrito".encode("utf-8"))
                else:
                    cliente.sendall(f"El vuelto es {numero - total}".encode("utf-8"))

                break
            else:
                total += productos[numero - 1]["precio"]
                totalPropio += productos[numero - 1]["precio"]
                carrito.append(numero - 1)
                print(carrito) 
                producto = productos[numero - 1]
                carritotxt += ( "\n" + str(len(carrito))+ "- " + producto["nombre"] + " : $" + str(producto["precio"]))
                cliente.sendall(carritotxt.encode("utf-8"))
                cliente.sendall(f"\nTotal: {total}".encode("utf-8"))
                
        except Exception as e:
            # Si hay un error, cierra la conexión con el cliente
            print(e)
            cliente.close()
            for i in range(0, len(clientes)):
                if cliente == clientes[i]:
                    clientes.pop(i)

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
