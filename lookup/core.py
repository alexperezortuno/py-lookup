# Configurar el proxy Tor
import os
from argparse import Namespace
from typing import Any
from urllib.parse import urlencode

import requests
from fake_useragent import UserAgent
from requests import get
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

def get_results(params: Namespace, url: str) -> requests.Response:
    timeout: int = params.timeout
    is_tor_enabled: bool = params.tor
    if is_tor_enabled:
        session = get_tor_session()
        response = session.get(url, headers=get_headers(), timeout=timeout)
    else:
        response = get(url, headers=get_headers(), timeout=timeout)
    return response

def get_results_with_params(params: Namespace, url: str, data: Any) -> requests.Response:
    timeout: int = params.timeout
    is_tor_enabled: bool = params.tor
    if is_tor_enabled:
        session = get_tor_session()
        response = session.post(url, headers=get_headers(), params=data, timeout=timeout)
    else:
        response = get(url, headers=get_headers(), params=data, timeout=timeout)
    return response

def parse_url(url: str, params: dict) -> str:
    return url + urlencode(params)
