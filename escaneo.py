import os, base64, getpass
from googlesearch import search



def busqueda_google(palabra):
    directorio = directorio + "\\Busquedas"
    os.makedirs(directorio, exist_ok=True)
    palabra = params.busqueda
    resultados = []

    for enlace in search(palabra, sleep_interval=5, num_results=5):
        resultados.append(enlace)

    ruta = directorio + "\\resultados.txt"
    file = open(ruta, "w")

    for cosas in resultados:
        file.write(cosas + "\n")    
    file.close

def encriptado_cesar(mensaje, clave):
    espacios = 1
    while espacios > 0:
        espacios = clave.count(" ")
        if clave.isalpha() == False:
            espacios += 1
    key = len(clave)

    SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'
    translated = ""

    for symbol in mensaje:
        if symbol in SYMBOLS:
            symbolIndex = SYMBOLS.find(symbol)
            translatedIndex = symbolIndex - key

            if translatedIndex >= len(SYMBOLS):
                translatedIndex = translatedIndex - len(SYMBOLS)
            elif translatedIndex < 0:
                translatedIndex = translatedIndex + len(SYMBOLS)

            translated = translated + SYMBOLS[translatedIndex]
        else:
            
            translated = translated + symbol
        
    return translated

def encriptado_trans(mensaje, clave):
    espacios = 1
    while espacios > 0:
        espacios = clave.count(" ")
        if clave.isalpha() == False:
            espacios += 1
    myKey = len(clave)

    ciphertext = encryptMessage(myKey, mensaje)
    
    def encryptMessage(key, message):

        ciphertext = [""] * key
        for column in range(key):
            currentIndex = column

            while currentIndex < len(message):

                ciphertext[column] += message[currentIndex]
                currentIndex += key
        
        return "".join(ciphertext)

    return ciphertext

def encriptado_64(mensaje):
    mensaje_bytes = mensaje.encode("ascii")
    base64_bytes = base64.b64encode(mensaje_bytes)
    return base64_bytes