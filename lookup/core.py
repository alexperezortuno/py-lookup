# Configurar el proxy Tor
import os
from argparse import Namespace
import random
from typing import Any
from urllib.parse import urlencode

import requests
from fake_useragent import UserAgent
from requests import get
from stem.control import Controller

from prompt_toolkit import prompt  # pip install prompt_toolkit
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

# ------------------------ Global variables ------------------------ #
try:
    session = PromptSession(history=FileHistory('./.ph0mber_history'))
except:
    session = PromptSession(history=InMemoryHistory())
available_commands = ['change', 'check', 'clear', 'dns', 'dork', 'email', 'exit', 'exp', 'hash', 'help', 'info', 'ip',
                      'mac', 'number', 'quit', 'save', 'shell', 'username', 'whois']
full_cmd = ''
silent_mode = False


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


def check_connection(params: Namespace):
    # Checking internet connection
    urls = ['https://google.com', 'https://bing.com']
    try:
        if params.tor:
            session = get_tor_session()
            session.get(random.choice(urls), timeout=params.timeout)
        else:
            requests.get(random.choice(urls), timeout=10)
        return True
    except:
        return False


def printit(text, center='', line_up=False, line_down=False, space_up=False, space_down=False, coledt=[0, 0, 0],
            normaltxt_start='', normaltxt_end='', hide=False, verbose_mode=False, input_mode=False):
    if not hide or verbose_mode:
        # get terminal width
        width = os.get_terminal_size().columns

        # printing text
        if space_up: print()
        if line_up: print('⸺' * width)

        print(normaltxt_start, end='')

        new_width = int((width - len(text)) / 2)
        print(center * new_width, end='')
        print(f'\33[{coledt[0]};{coledt[1]};{coledt[2]}m', end='')
        # if input_mode: input_var = input(text)
        if input_mode:
            input_var = session.prompt(ANSI(text), auto_suggest=AutoSuggestFromHistory(),
                                       completer=WordCompleter(available_commands))
        else:
            print(str(text), end='')
        print('\033[0m', end='')
        print(center * new_width)

        print(normaltxt_end, end='')

        if line_down: print('⸺' * width)
        if space_down: print()

        if input_mode: return input_var
