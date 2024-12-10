from time import sleep

from colorama import Fore
from jaraco.functools import retry
from requests import get

from lookup.core import get_headers, get_session


class EmailSearch:
    @staticmethod
    def check_spotify_email(target: str):
        try:
            ret: int = 0
            url = f"https://spclient.wg.spotify.com/signup/public/v1/account?validate=1&email={target}"
            session = get_session()
            response = session.get(url, headers=get_headers())

            while response.status_code != 200 and ret < 10:
                session = get_session()
                response = session.get(url, headers=get_headers())
                ret += 1

            if response.status_code == 200:
                result = response.json()

                if result.get('status') == 20:
                    print(f"{Fore.LIGHTWHITE_EX}    •{Fore.LIGHTGREEN_EX} Spotify Account Found")
                else:
                    print(f"{Fore.LIGHTWHITE_EX}    •{Fore.LIGHTRED_EX} No Spotify account")
            else:
                print(f"{Fore.LIGHTWHITE_EX}    •{Fore.LIGHTRED_EX} No Spotify account")
        except Exception as e:
            print(f"{Fore.LIGHTWHITE_EX}    •{Fore.LIGHTRED_EX} Failed to retrieve results from spotify: {e}")
