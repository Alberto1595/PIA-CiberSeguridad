import os
import requests

API_KEY = '500b866fba509079ee212b5dc19802629088f5a4574110a4180d6322aeffe458'

def URL_report(url):
    url = 'https://www.virustotal.com/vtapi/v2/url/report'
    params = {'apikey': API_KEY, 'resource': url}
    response = requests.get(url, params=params)
    return response.json()

def url_report_write(json_file):
    if 'scans' not in json_file:
        print("No se pudo obtener el escaneo de la URL.")
        return

    if not os.path.exists("./report"):
        os.makedirs("./report")

    report_url = open("C:\\Users\\Dell\\Documents\\checar\\scan_url_report.txt", "w") #cambiar la ruta del codigo

    
    file_info = "URL: " + json_file['url'] +"\n"
    scan_date = "Fecha del escaneo: " + json_file['scan_date'] +"\n"
    number_positive = "Escaneos positivos: " + str(json_file['positives']) + "\n"
    total_scan = "Total de escaneos: " + str(json_file['total']) + "\n\n"

    report_url.write(file_info + scan_date + number_positive + total_scan)

    for antivirus, result in json_file['scans'].items():
        detected = "SÍ" if result['detected'] else "NO"
        malware_details = result['result'] if result['result'] else "Ninguno"
        line = f"{antivirus}: Malware detectado: {detected} | Detalles del malware: {malware_details}\n"
        report_url.write(line)

    report_url.close()

def url_scan():
    print("Ingresa la URL:")
    url = input()
    url_report_write(URL_report(url))

url_scan()

