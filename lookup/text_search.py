from argparse import Namespace
from re import search
from urllib.parse import urlencode, urljoin

from bs4 import BeautifulSoup
from colorama import Fore
from time import sleep
from requests import get, RequestException
from lookup.core import renew_tor_ip, get_tor_session, get_session, get_headers, get_results


class TextSearch:
    @staticmethod
    def search_ahmia(params: Namespace) -> None:
        try:
            text: str = params.search
            url = f"https://ahmia.fi/search/?"
            url_params = {
                'q': text
            }

            url_with_params = url + urlencode(url_params)
            response = get_results(params, url_with_params)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            ahmia_results = [link["href"] for link in soup.find_all("a", href=True) if ".onion" in link["href"]]

            if ahmia_results:
                print(
                    f"{Fore.LIGHTWHITE_EX}[ + ] Found{Fore.LIGHTMAGENTA_EX} {len(ahmia_results)}{Fore.LIGHTWHITE_EX} .onion links on Ahmia for '{Fore.LIGHTMAGENTA_EX}{text}{Fore.LIGHTWHITE_EX}':")
                for result in ahmia_results:
                    if '/search/redirect?search_term=' in result:
                        result = result.split('&redirect_url=')[-1]
                    print(
                        f'{Fore.LIGHTWHITE_EX}    •{Fore.LIGHTGREEN_EX} Link{Fore.LIGHTWHITE_EX} :{Fore.LIGHTMAGENTA_EX} {result}')
                    sleep(0.02)
            else:
                print(f"{Fore.LIGHTWHITE_EX}    •{Fore.LIGHTRED_EX} No .onion links found on Ahmia for '{text}'.")
        except RequestException as e:
            print(f"{Fore.LIGHTWHITE_EX}    •{Fore.LIGHTRED_EX} Failed to retrieve results from Ahmia: {e}")

    @staticmethod
    def doxbin_search(params: Namespace) -> None:
        text: str = params.search
        query = f"{text} site:doxbin.org"
        url = "https://www.google.com/search?"
        url_params = {
            'q': query,
            'hl': 'en',
            'num': 10
        }

        url_with_params = url + urlencode(url_params)

        try:
            response = get_results(params, url_with_params)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('/url?q='):
                    link = href.split('/url?q=')[1].split('&')[0]
                    if 'doxbin.org' in link and not any(
                        sub in link for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                        links.append(link)
                        print(f"{Fore.LIGHTWHITE_EX}    •{Fore.LIGHTGREEN_EX} Link{Fore.LIGHTWHITE_EX} :{Fore.LIGHTMAGENTA_EX} {link}")
                elif 'doxbin.org' in href and href.startswith('http') and not any(
                    sub in href for sub in ['google.com', 'translate.google.com', 'accounts.google.com']):
                    links.append(urljoin(url_with_params, href))
                    print(f"{Fore.LIGHTWHITE_EX}    •{Fore.LIGHTGREEN_EX} Link{Fore.LIGHTWHITE_EX} :{Fore.LIGHTMAGENTA_EX} {urljoin(url_with_params, href)}")
        except RequestException as e:
            print(f"{Fore.LIGHTWHITE_EX}    •{Fore.LIGHTRED_EX} Error : {e}")
