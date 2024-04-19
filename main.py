import sys
sys.path.append(r"C:\Users\Dell\Pictures\PIA-CiberSeguridad\Modulos\BeatifullSoup")
from bs_todosenlaces import obtener_enlaces_desde_url

url = input("Ingresa URL: ")
print(obtener_enlaces_desde_url(url))