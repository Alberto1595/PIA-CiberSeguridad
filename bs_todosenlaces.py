from bs4 import BeautifulSoup
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

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


