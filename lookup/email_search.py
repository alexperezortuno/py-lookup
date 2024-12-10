from argparse import Namespace
from urllib.parse import urlencode

from colorama import Fore

from lookup.core import get_headers, get_session, get_results, parse_url, get_results_with_params


class EmailSearch:
    @staticmethod
    def check_spotify_email(params: Namespace) -> None:
        try:
            ret: int = 0
            url = f"https://spclient.wg.spotify.com/signup/public/v1/account?"
            url_params = {
                'validate': 1,
                'email': params.email
            }

            url_with_params = parse_url(url, url_params)
            response = get_results(params, url_with_params)

            while response.status_code != 200 and ret < 10:
                response = get_results(params, url)
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

    @staticmethod
    def check_duolingo_email(params: Namespace) -> None:
        url = "https://www.duolingo.com/2017-06-30/users"
        url_params = {
            'email': params.email
        }

        try:
            ret: int = 0
            response = get_results_with_params(params, url, url_params)

            while response.status_code != 200 and ret < 10:
                response = get_results_with_params(params, url, url_params)
                ret += 1

            if response.status_code == 200:
                text_response = response.text

                if '{"users":[]}' in text_response:
                    print(f"{Fore.LIGHTWHITE_EX}    •{Fore.LIGHTRED_EX} No Duolingo account")
                else:
                    valid = response.json()['users'][0]['username']
                    print(f"{Fore.LIGHTWHITE_EX}    •{Fore.LIGHTGREEN_EX} Duolingo Account Found")

        except Exception as e:
            pass