import socket

HOST = "localhost"  # Dirección del servidor
PORT = 8000  # Puerto del servidor
clientes = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea un socket TCP
server.bind((HOST, PORT))  # Asocia el socket a la dirección y puerto
server.listen(5)  # Pone el socket en modo escucha
print("[SERVIDOR] Servidor iniciado")


try:
    opciones = ["piedra", "papel", "tijera"]
    ganadores = ["tijera", "piedra", "papel"]
    perdedores = ["papel", "tijera", "piedra"]

    cliente1Wins = 0
    cliente2Wins = 0

    # Acepta una conexión entrante del cliente
    cliente1, direccion1 = server.accept()
    cliente1.sendall("Esperando contrincante".encode("utf-8"))
    cliente2, direccion2 = server.accept()
    cliente1.sendall("Contrincante encontrado.".encode("utf-8"))
    cliente2.sendall("Contrincante encontrado.".encode("utf-8"))


    while True:
        cliente1.sendall("Seleccione: piedra, papel, tijera".encode("utf-8"))
        cliente2.sendall("Seleccione: piedra, papel, tijera".encode("utf-8"))
        mensaje1 = cliente1.recv(1024).decode("utf-8")
        mensaje2 = cliente2.recv(1024).decode("utf-8")
        
        if mensaje1 == mensaje2:
            cliente1.sendall("empate".encode("utf-8"))
            cliente2.sendall("empate".encode("utf-8"))
        else: 
            for i in range(0, 3):
                if mensaje1 == opciones[i]:
                    if mensaje2 == ganadores[i]:
                        cliente1.sendall(f"ganaste, el contrincante uso {ganadores[i]}".encode("utf-8"))
                        cliente2.sendall(f"perdiste, el contrincante uso {opciones[i]}".encode("utf-8"))
                        cliente1Wins += 1
                    if mensaje2 == perdedores[i]:
                        cliente2.sendall(f"ganaste, el contrincante uso {opciones[i]}".encode("utf-8"))
                        cliente1.sendall(f"perdiste, el contrincante uso {perdedores[i]}".encode("utf-8"))
                        cliente2Wins += 1

        cliente1.sendall(f"puntaje: {cliente1Wins}-{cliente2Wins}".encode("utf-8"))
        cliente2.sendall(f"puntaje: {cliente1Wins}-{cliente2Wins}".encode("utf-8"))

        if cliente1Wins > 2 or cliente2Wins > 2:
            cliente1.close()
            cliente2.close()
            break

except:
    print("error 1")
