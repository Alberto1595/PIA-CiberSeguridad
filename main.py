from bs_todosenlaces import obtener_enlaces_desde_url
from whoiscopy import whois
from sho import s


def webscrapping():
    url = input("Ingresa URL: ")
    print(obtener_enlaces_desde_url(url))