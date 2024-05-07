import os

from googlesearch import search
import base64, requests, nmap
from bs4 import BeautifulSoup
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from PyPDF2 import PdfReader



#Funcion de busqueda en google
def busqueda_google(palabra):
    directorio = os.getcwd()
    directorio = directorio + "\\Busquedas"
    os.makedirs(directorio, exist_ok=True)
    resultados = []

    for enlace in search(palabra, tld="com", num=5, stop=5, pause=5):
        resultados.append(enlace)

    ruta = directorio + "\\resultados.txt"
    file = open(ruta, "w")

    for cosas in resultados:
        file.write(cosas + "\n")    
    file.close

#Funcion de encriptado cesar
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

#Funcion de encriptado de transposicion
def encriptado_trans(mensaje, clave):
    def encryptMessage(key, message):
        ciphertext = [""] * key

        for column in range(key):
            currentIndex = column

            while currentIndex < len(message):
                ciphertext[column] += message[currentIndex]

                currentIndex += key
        return "".join(ciphertext)
    
    espacios = 1
    while espacios > 0:
        espacios = clave.count(" ")
        if clave.isalpha() == False:
            espacios += 1
        myKey = len(clave)

        ciphertext = encryptMessage(myKey, mensaje)
        ciphertext = ciphertext + " |"
    return ciphertext

#Funcion de encriptado base64
def encriptado_64(mensaje):
    mensaje_bytes = mensaje.encode("ascii")
    base64_bytes = base64.b64encode(mensaje_bytes)
    base64_message = base64_bytes.decode("ascii")
    return str(base64_bytes)

#Requests
def obtener_enlaces_desde_url(url):
    
    try:
        
        if not (url.startswith("http://") or url.startswith("https://")):
            url = "http://" + url

        
        r = requests.get(url, verify=False)
        r.raise_for_status()  # Lanzar una excepción si hay un error en la solicitud

        
        soup = BeautifulSoup(r.text, 'html.parser')

        
        for link in soup.find_all('a'):
            href = link.get('href')
            if href is not None and href.strip() != '':
                print(href)

    except requests.exceptions.RequestException as e:
        print("Error al realizar la solicitud HTTP:", e)

    except Exception as e:
        print("Ocurrió un error inesperado:", e)


def scanning(begin, end, target):
    def create_pdf(data, title):
        title_style = getSampleStyleSheet()["Title"]
        title_paragraph = Paragraph(title, title_style)
        directorio_pdf = os.getcwd()
        folder_path = directorio_pdf + "\\Reporte pdf"
        os.makedirs(folder_path, exist_ok=True)

        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)])

        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        pdf_filename = os.path.join(folder_path, f"Resultados_de_escaneo_{timestamp}.pdf")
        pdf = SimpleDocTemplate(pdf_filename, pagesize=letter)
        table = Table(data)

        table.setStyle(style)

        content = [title_paragraph, table]

        pdf.build(content)
    scanner = nmap.PortScanner()
    results = [["Puerto", "Estado"]]
    

    for i in range(begin, end + 1):
        res = scanner.scan(target, str(i))
        state = res["scan"][target]["tcp"][i]["state"]
        results.append([f'Port {i}', state])
    title = f"Resultados del escaneo de puertos {target}"
    create_pdf(results, title)
    
    

def metadatos_pdf(pdf):
    pdfFileObj = open(pdf, "rb")
    pdf = PdfReader(pdfFileObj)
    resultados = []
    paginas = str("Paginas: " + str(len(pdf.pages)))
    resultados.append(paginas)
    titulo = str("Titulo: " + str(pdf.metadata.title))
    resultados.append(titulo)
    primera_hoja = pdf.pages[0]
    contenido = primera_hoja.extract_text()
    resultados.append(contenido)
    return resultados


