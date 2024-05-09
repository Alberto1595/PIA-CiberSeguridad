import os

from googlesearch import search
import base64, requests, nmap, subprocess, pickle
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

        lista_url = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href is not None and href.strip() != '':
                lista_url.append(href)
        return lista_url

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

def url_vt(url, API_KEY):
    def url_report(url):
        url_scan = "https://virustotal.com/vtapi/v2/url/report"
        vparams = {"apikey": API_KEY, "resource": url}
        response = requests.get(url_scan, params=vparams)
        return response.json()
    
    def url_report_write(json_file, url):
        if json_file["response_code"] != 1:
            exit()
        
        directorio = os.getcwd()
        directorio = directorio + "\\ReporteVT"
        os.makedirs(directorio, exist_ok=True)
        ruta = directorio + "\\reporteVT.txt"
        report_url = open(ruta, "w")

        file_info = "URL" + url + "\n"
        scan_date = "Fecha del escaneo: " + json_file["scan_date"] + "\n"
        number_positive = "Escaneos positivos: " + str(json_file["positives"]) + "\n"
        total_scan = "Total de escaneos: " + str(json_file["total"]) + "\n\n"

        report_url.write(file_info + scan_date + number_positive + total_scan)

        if "scans" in json_file:
            for antivirus, result in json_file["scans"].items():
                detected = "SI" if result["detected"] else "NO"
                malware_details = result["result"] if result["result"] else "Ninguno"
                line = f"{antivirus}: Malware detectado: {detected} | Detalles del malware: {malware_details} \n"
                report_url.write(line)
        else:
            report_url.write("El archivo aún no ha sido analizado por todos los motores de antivirus.\n")
        
        report_url.close()

    def url_scan(x):
        url_report_write(url_report(x), url)

    url_scan(url)

def obt_hash(basefile, objetivo, tmpfile):

    
    try:
        directorio = os.getcwd()
        directorio += "\Hash"
        os.makedirs(directorio, exist_ok=True)
        with open(os.path.join(directorio, tmpfile), "w") as file:
            file.write("")
        temporalfile = "Hash\\" + tmpfile

        contenido = """param(
            [string]$TargetFolder="c:\windows\system32\drivers\",
            [string]$ResultFile="baseline.txt"
        )

        Get-ChildItem $TargetFolder | Get-FileHash | Select-Object -Property Hash, Path | Format-Table -HideTableHeaders | Out-File $ResultFile -Encoding ascii
        """
        with open(os.path.join(directorio, "HashAcquire.ps1"), "w") as file:
            file.write(contenido)
        
        command = "powershell -ExecutionPolicy ByPass -File Hash\HashAcquire.ps1 -TargetFolder \""+ objetivo + "\" -ResultFile \"" + temporalfile +"\""

        powerShellResult = subprocess.run(command, stdout=subprocess.PIPE)
        
        if powerShellResult.stderr == None:
        
            baseDict = {}

            with open(os.paht.join(directorio,tmpfile), "r") as inFile:
                for eachLine in inFile:
                    lineList = eachLine.split()
                    if len(lineList) == 2:
                        hashValue = lineList[0]
                        fileName = lineList[1]
                        baseDict[hashValue] = fileName
                    else:
                        continue

            with open(os.path.join(directorio, basefile), "wb") as outFile:
                pickle.dump(baseDict, outFile)
                
        
        else:
            pass
    
    except Exception:
        pass



