# Configurar el proxy Tor
import os

import requests
from fake_useragent import UserAgent
from stem.control import Controller


def get_tor_session():
    session = requests.Session()
    session.proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050',
    }
    return session


# Obtener nueva identidad en Tor
def renew_tor_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(
            password=os.getenv('TOR_PWD'))  # Cambia 'tu_password_de_tor' por la configuración de tu Tor
        controller.signal('NEWNYM')


def get_headers() -> dict:
    ua = UserAgent()
    return {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'close',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Referer': 'https://www.google.com',
    }


def get_session():
    renew_tor_ip()  # Cambiar la IP antes de cada búsqueda (opcional)
    return get_tor_session()
