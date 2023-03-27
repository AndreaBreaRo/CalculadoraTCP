import socket
import sys

if len(sys.argv) != 2:
    print("ERROR: Argumentos de entrada incorrectos, ejemplo:")
    print("python tcp1ser.py 12345")
    sys.exit()

HOST = ''  # Acepta conexiones desde cualquier direccion IP
PORT = int(sys.argv[1]) # Puerto del servidor

# Crear un socket de tipo TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    # Vincular el socket al puerto y direccion IP especificados
    s.bind((HOST, PORT))
    
    # Esperar por conexiones entrantes
    s.listen(1)
    print(f"Servidor escuchando en el puerto {PORT}...")
    
    # Aceptar la primera conexion entrante
    conn, addr = s.accept()
    print(f"Conexion establecida con {addr}")
    accumulator = 0
    print(f"Acumulador inicializado en {accumulator}.")

    while True:
        # Recibir los datos del cliente
        message = conn.recv(6)

        if message == b'QUIT':
            print("El cliente ha cerrado la conexion.")
            conn.close()
            print(f"Servidor escuchando en el puerto {PORT}...")
            # Volver a esperar por conexiones entrantes
            conn, addr = s.accept()
            print(f"Conexion establecida con {addr}")
            continue

        # Comprobar si el cliente ha cerrado la conexion
        if not message:
            break
                
        # Interpretar el mensaje recibido
        type = int.from_bytes(message[0:2], byteorder='big', signed=True)
        length = int.from_bytes(message[2:4], byteorder='big', signed=True)
        value1 = int.from_bytes(message[4:5], byteorder='big', signed=True)
        value2 = int.from_bytes(message[5:6], byteorder='big', signed=True)

        # Calculamos el resultado de la operacion solicitada
        result = None
        if type == 1:
            result = value1 + value2
            accumulator += result
            print(f"Suma recibida: {value1} + {value2} = {result}. Acumulador actual: {accumulator}.")
        elif type == 2:
            result = value1 - value2
            accumulator += result
            print(f"Resta recibida: {value1} - {value2} = {result}. Acumulador actual: {accumulator}.")
        elif type == 3:
            result = value1 * value2
            accumulator += result
            print(f"Multiplicacion recibida: {value1} * {value2} = {result}. Acumulador actual: {accumulator}.")
        elif type == 4:
            result = value1 // value2
            accumulator += result
            print(f"Division recibida: {value1} // {value2} = {result}. Acumulador actual: {accumulator}.")
        elif type == 5:
            result = value1 % value2
            accumulator += result
            print(f"Modulo recibido: {value1} % {value2} = {result}. Acumulador actual: {accumulator}.")
        elif type == 6:
            result = 1
            for i in range(1, value1 + 1):
                result *= i
            accumulator += result
            print(f"Factorial recibido: {value1}! = {result}. Acumulador actual: {accumulator}.")

        # Convertimos los datos en bytes por Big-Endian con signo
        acumulator_bytes = accumulator.to_bytes(8, byteorder='big', signed=True)
        response_bytes = [16, 8] + list(acumulator_bytes)
        print(response_bytes) 
        conn.sendall(bytes(response_bytes))