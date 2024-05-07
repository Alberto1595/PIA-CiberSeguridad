import os
try:
    #Importa las librerias necesarias para el funcionamiento del script 
    from googlesearch import search
    import base64, requests, logging, argparse, nmap
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    from bs4 import BeautifulSoup
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet
    from datetime import datetime
    from PyPDF2 import PdfFileReader

except ImportError:
    #Si hay un error al importar descarga las librerias marcadas por el archivo requirements.txt
    os.system("pip install -r requirements.txt")
    exit()

from Modulos import Funciones
"""
def envio_mensaje(sid, token, remitente, destinatario):
    msg = "El scrip se finalizo"
    message = twilioCli.messages.create(to= destinatario,
                                        from_ = remitente,
                                        body = msg)
"""   
#Le da formato al archivo logging para mantener un monitoreo a los errores
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    filename="logging.log")
logger = logging.getLogger(__name__)

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
fecha = datetime.now()
formato = formato = fecha.strftime("%d, %m, %Y, %R")

#Definicion de variables
parser = argparse.ArgumentParser(description="Modulos disponibles. \n"
                                 "encriptado. \n"
                                 "busqueda. \n"
                                 "metadatos pdf. \n"
                                 "request url. \n", formatter_class=argparse.RawTextHelpFormatter)
valor = False
#Seleccion de funcion
subparsers = parser.add_subparsers(dest="module", help="Funcion a ejecutar", required=True)

#Busqueda en Google
parser_busqueda = subparsers.add_parser("busqueda", help="Busqueda de google")
parser_busqueda.add_argument("-b", dest="palabra", help="Palabra a buscar", required=valor)

#Encriptado
parser_encriptado = subparsers.add_parser("encriptado", help="Encriptado \n"
                                          "Ejemplo de uso: \n"
                                          "py main.py -tipo Tipo de cifrado -m Mensaje -clave clave de cifrado(Opcional)")
parser_encriptado.add_argument("-tipo", dest="tipo", help="Tipo de cifrado", required=valor)
parser_encriptado.add_argument("-m", dest="mensaje", help="Mensaje a cifrar", required=valor)
parser_encriptado.add_argument("-clave", dest="clave", help="Palabra clave para cifrar", default="TILIN")

#bs_todos los enlaces
parser_url = subparsers.add_parser("url", help="Obtener requests de todos los url")
parser_url.add_argument("-url", dest="url", help="Url a pedir request")

#Escaneo
parser_escaneo = subparsers.add_parser("escaneo", help="Escaneo de puertos")
parser_escaneo.add_argument("-p1", dest="puerto1", help="Puerto inicial a escanear", default="10")
parser_escaneo.add_argument("-p2", dest="puerto2", help="Puerto final a escanear", default="30")
parser_escaneo.add_argument("-objetivo", dest="objetivo", help="IP a escanear")

#metadatos PDF
meta_pdf = subparsers.add_parser("metapdf", help="Obtencion de metadatos de un pdf")
meta_pdf.add_argument("-pdf", dest="rutapdf", help="Ruta del pdf a analizar")


params = parser.parse_args()

if __name__ == "__main__":

    try:
        module_to_run = params.module
        

        if module_to_run == "encriptado":
            
            if params.tipo == "1":
                result_encriptado = Funciones.encriptado_cesar(params.mensaje, str(params.clave))
                directorio = os.getcwd()
                directorio = directorio + "\\encriptadoC"
                os.makedirs(directorio, exist_ok=True)
                ruta = directorio + "\\cesar.txt"
                file = open(ruta, "w")
                file.write(result_encriptado)
                file.close
                exit()
            
            elif params.tipo == "2":
                result_encriptado = Funciones.encriptado_trans(params.mensaje, str(params.clave))
                directorio = os.getcwd()
                directorio = directorio + "\\encriptadoT"
                os.makedirs(directorio, exist_ok=True)
                ruta = directorio + "\\trans.txt"
                file = open(ruta, "w")
                file.write(result_encriptado)
                file.close

            elif params.tipo == "3":
                result_encriptado = Funciones.encriptado_64(params.mensaje)
                directorio = os.getcwd()
                directorio = directorio + "\\encriptado64"
                os.makedirs(directorio, exist_ok=True)
                ruta = directorio + "\\base64.txt"
                file = open(ruta, "w")
                file.write(result_encriptado)
                file.close
            
            else:
                tipo = params.tipo
                logger.error(f'Tipo de encriptado no reconocido: {tipo}')
                print(f"ipo de encriptado no reconocido: {tipo}")

        elif module_to_run == "busqueda":

            Funciones.busqueda_google(params.palabra)

        elif module_to_run == "url":

            Funciones.obtener_enlaces_desde_url(params.url)

        elif module_to_run == "escaneo":
            start = int(params.puerto1)
            end = int(params.puerto2)
            Funciones.scanning(start, end, params.objetivo)

        elif module_to_run == "metadatospdf":

            lista = Funciones.metadatos_pdf(params.rutapdf)
            directorio = os.getcwd()
            directorio = directorio + "\\Metadatospdf"
            os.makedirs(directorio, exist_ok=True)
            ruta = directorio + "\\metadatos.txt"
            file = open(ruta, "w")
            for elemento in lista:
                file.write(elemento)
                file.write("\n")
            file.close
        
        else:
            
            logger.error(f'Modulo no reconocido: {module_to_run}')
            print(f'Modulo no reconocido: {module_to_run}')
            

    except argparse.ArgumentError as e:
        logger.error(f'Error en los argumentos: {e}')
        print(f'Error en los argumentos: {e}')
    
    except Exception as e:
        logger.error(f'Error durante la ejecucion: {e}')
        

         

