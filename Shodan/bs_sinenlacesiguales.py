from bs4 import BeautifulSoup
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def obtener_enlaces_desde_url(url):
    try:
        
        if not (url.startswith("http://") or url.startswith("https://")):
            url = "http://" + url

        r = requests.get(url, verify=False)
        r.raise_for_status()  

        
        soup = BeautifulSoup(r.text, 'html.parser')
        enlaces_unicos = set()

        for link in soup.find_all('a'):
            href = link.get('href')
            # Excluir los enlaces que comienzan con "tel:" y las redes sociales
            if href is not None and not href.startswith("tel:") and \
               "facebook.com" not in href and "twitter.com" not in href:
                enlaces_unicos.add(href)

        
        for enlace in enlaces_unicos:
            print(enlace)

    except requests.exceptions.RequestException as e:
        print("Error al realizar la solicitud HTTP:", e)

    except Exception as e:
        print("Ocurrió un error inesperado:", e)

# URL a verificar
url = "www.fcfm.uanl.mx"


obtener_enlaces_desde_url(url)
