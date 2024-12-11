from argparse import Namespace

import bs4
from colorama import Fore

from lookup.core import get_results, check_connection, get_results_with_webdriver


class UsernameSearch:
    @staticmethod
    def username_lookup(params: Namespace):
        # Checking internet connection
        print(f'{Fore.YELLOW}    [+] Verifying internet connection...{Fore.RESET}')
        prv_op: str = ''
        username: str = params.username
        if not check_connection(params):
            print(f'{Fore.RED}    > Internet connection not available!{Fore.RESET}')
            return False

        # Information gathering about the username
        print(f'{Fore.YELLOW}    [+] Grathering information about {Fore.CYAN}{username}...{Fore.RESET}')
        prv_op += f'    {Fore.LIGHTWHITE_EX}[#] Reverse username lookup for {Fore.CYAN}{username}{Fore.RESET} \n\n'

        # Validating username (no spaces)
        if ' ' in username:
            print(f'{Fore.RED}    > Invalid username!{Fore.RESET}')
            return False

        # https://www.idcrawl.com/u/<username>
        try:
            # requesting the url
            if params.webdriver:
                response = get_results_with_webdriver(params, f'https://www.idcrawl.com/u/{username}')
            else:
                response = get_results(params, f'https://www.idcrawl.com/u/{username}')

            if params.webdriver:
                soup = bs4.BeautifulSoup(response, 'html.parser')
            else:
                soup = bs4.BeautifulSoup(response.text, 'html.parser')

            # Extracting data
            # save information in a dictionary
            info_dict = {}

            # Main infomation to extract
            #   gl-page-content col-md-8 col-sm-12 col-xs-12 (main class div)
            #   gl-accordion-item > h2 tag (key of info_dict)
            #   panel-collapse > gl-job-position-company > h3 (link -a and text) & p (value of info_dict)
            # extract h2 and h3 tags in dictionary (h2 as key and h3 as value)

            # class = "gl-page-content col-md-8 col-sm-12 col-xs-12"
            soup = soup.find('div', {'class': 'gl-page-content col-md-8 col-sm-12 col-xs-12'})

            # save h2 and h3 tags in dictionary (h2 as key and h3 as value)
            if soup is None:
                print(f'{Fore.RED}    > No information found!{Fore.RESET}')
                return False
            for h2 in soup.find_all('h2'):
                try:
                    # if there is `Not Taken` text inside the same div as h2 then skip it !!NEED_TO_FIX_IT!!
                    if 'Not Taken' in h2.findNext('p').text:
                        continue
                    # if in `panel-heading-info` there is `Email Addresses` or `Secret Profiles` text then skip it
                    if 'Email Addresses' in h2 or 'Secret Profiles' in h2:
                        continue
                    # saving h2 and h3 tags in dictionary
                    info_dict[str(h2).split('</i>')[1].split('</h2>')[0]] = h2.findNext('h3').text
                except:
                    pass

            if info_dict:
                final_output = f'''
            ┌──────────────────────────────────────────────────────┐
            | Scanned Username: {Fore.LIGHTWHITE_EX}{username + ' ' * int(34 - len(str(username)))}{Fore.RESET} |
            |------------------------------------------------------|
            | INFORMATION         | DESCRIPTION                    |
            |------------------------------------------------------|'''

                for site, username in info_dict.items():
                    site = str(site) + ' ' * int(19 - len(str(site)))
                    username = str(username) + ' ' * int(30 - len(str(username)))
                    final_output += f'''\n    | {Fore.LIGHTWHITE_EX}{site}{Fore.RESET} | {username} |'''

                final_output += f'''\n    └──────────────────────────────────────────────────────┘'''

                print(final_output)
                prv_op += final_output + '\n'
                return True

            else:
                final_output = f'''
            ┌──────────────────────────────────────────────────────┐
            | Scanned Username: {Fore.LIGHTWHITE_EX}{username + ' ' * int(34 - len(str(username)))}{Fore.RESET} |
            |------------------------------------------------------|
            | INFORMATION         | DESCRIPTION                    |
            |------------------------------------------------------|
            | {Fore.RED}Failed to Fetch information from server!{Fore.RESET}             |
            └──────────────────────────────────────────────────────┘
                '''
                print(final_output)
                prv_op += final_output + '\n'
                return False
        except Exception as e:
            print(e)
