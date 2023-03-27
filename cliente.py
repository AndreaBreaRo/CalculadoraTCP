import socket
import sys

def extraer(data):

    data = data.replace(" ", "") # elimina espacios en blanco de la operacion
    pos_operador = -1
    # Busca la posicion del operador 
    for i, c in enumerate(data):
        if c in "+-*/%!":
            pos_operador = i
            break
    
    tipo = 0
    longitud = 0
    operador = data[pos_operador]
     # Codificacion de la operacion y los numeros en formato TLV
    if operador == '+':
        tipo = 1
        longitud = 2
    elif operador == '-':
        tipo = 2
        longitud = 2
    elif operador == '*':
        tipo = 3
        longitud = 2
    elif operador == '/':
        tipo = 4
        longitud = 2
    elif operador == '%':
        tipo = 5
    elif operador == '!':
        tipo = 6
        longitud = 1

    if operador == -1:
        print("Operador no encontrado, o operacion introducida invalida")
    elif longitud == 1:  # Extraer operadores en caso de !
        operando1 = int(data[:pos_operador])
        operando2 = 0
        operador = data[pos_operador]
        return operando1, operando2, tipo, longitud   
    else:
        operando1 = int(data[:pos_operador])
        operando2 = int(data[pos_operador+1:])
        operador = data[pos_operador]
        return operando1,operando2, tipo, longitud 

# COMIENZO DE PROGRAMA 
if len(sys.argv) != 3:
    print("ERROR: Argumentos de entrada incorrectos, ejemplo:")
    print("python tcp1cli.py 127.0.0.1 12345")
    sys.exit()

HOST = sys.argv[1] # Direccion IP del servidor
PORT = int(sys.argv[2]) # Puerto del servidor

# Crear un socket de tipo TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Tiempo de espera para establecer conexion
    s.settimeout(15)
    try:
        s.connect((HOST, PORT))
    except socket.timeout:
        print("La conexion ha tardado demasiado tiempo en establecerse. Saliendo...")
        sys.exit()
    except ConnectionRefusedError:
        print("El servidor rechazo la conexion.")
        sys.exit()

    while True:
        data = input("Ingrese una operacion aritmetica (ejemplo: 5+3,  5 + 3 o QUIT para salir): ")
        
        if data == "QUIT":
            s.sendall(bytes(data, 'utf-8'))
            break
        
        num1, num2, tipo, longitud = extraer(data)

        # Codificar el mensaje como una secuencia de bytes TLV
        type_bytes = tipo.to_bytes(2, byteorder='big', signed=True)
        length_bytes = longitud.to_bytes(2, byteorder='big', signed=True)
        value1_bytes = num1.to_bytes(1, byteorder='big', signed=True)
        value2_bytes = num2.to_bytes(1, byteorder='big', signed=True)
        
        # Enviar la cadena de texto al servidor
        s.sendall(type_bytes + length_bytes + value1_bytes + value2_bytes)

        # Recibimos la respuesta del servidor
        msg_recived = s.recv(10)
        #result = int.from_bytes(msg_recived[0:2], byteorder='big', signed=True)
        acumulador = int.from_bytes(msg_recived[2:], byteorder='big', signed=True)
        
        # Imprimir la respuesta del servidor
        print(f"Operacion: {data}")
        print(f"Acumulador = {acumulador}")