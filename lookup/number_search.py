# Reverse phone number lookup
import re
from argparse import Namespace

import phonenumbers
from colorama import Fore
from phonenumbers import timezone
from phonenumbers import carrier
from phonenumbers import geocoder


class NumberSearch:
    def __init__(self):
        self.prv_op = ''

    def number_lookup(self, params: Namespace):
        phone_number: str = params.number
        self.prv_op = ''  # Resetting previous output

        # Country code check
        try:
            # Phone number format: (+Countrycode)xxxxxxxxxx
            phone_number_details = phonenumbers.parse(phone_number)
        except phonenumbers.phonenumberutil.NumberParseException:
            print(f'    > Missing Country Code! (Example: +91, +44, +1)')
            return False

        # extract country_code & only_number from "Country Code: xx National Number: xxxxxxxxxx"
        country_code = str(phone_number_details).split('Country Code:', 1)[1].split('National Number:', 1)[0].strip()
        only_number = str(phone_number_details).split('Country Code:', 1)[1].split('National Number:', 1)[1].strip()

        # Validating a phone number
        valid = phonenumbers.is_valid_number(phone_number_details)

        # Checking possibility of a number
        possible = phonenumbers.is_possible_number(phone_number_details)

        if valid and possible:
            # Creating a phone number variable for country
            counrty_number = phonenumbers.parse(phone_number, 'CH')

            # Gives mobile number's location (Region)
            region_code = phonenumbers.region_code_for_number(phone_number_details)

            # Gives mobile number's location (Country)
            country = geocoder.description_for_number(counrty_number, 'en')

            # Creating a phone number variable for service provider
            service_number = phonenumbers.parse(phone_number, 'RO')

            # Gives mobile number's service provider (Airtel, Idea, Jio)
            service_provider = carrier.name_for_number(service_number, 'en')

            # Gives mobile number's timezone
            timezone_details_unfiltered = str(timezone.time_zones_for_number(phone_number_details))
            timezone_details = timezone_details_unfiltered.replace('[', '').replace(']', '').replace("'", '').replace(
                '(',
                '').replace(
                ')', '').replace(',', '').replace(' ', '')

            # RFC3966 Format
            r_format = phonenumbers.format_number(phone_number_details, phonenumbers.PhoneNumberFormat.RFC3966).replace(
                'tel:', '')

            # Reconfiguring variables
            possible = str(possible) + ' ' * int(30 - len(str(possible)))
            valid = str(valid) + ' ' * int(30 - len(str(valid)))
            country_code = str(country_code) + ' ' * int(30 - len(str(country_code)))
            country = str(country) + ' ' * int(30 - len(str(country)))
            region_code = str(region_code) + ' ' * int(30 - len(str(region_code)))
            service_provider = str(service_provider) + ' ' * int(30 - len(str(service_provider)))
            timezone_details = str(timezone_details) + ' ' * int(30 - len(str(timezone_details)))
            phone_number = str(phone_number) + ' ' * int(30 - len(str(phone_number)))
            only_number = str(only_number) + ' ' * int(30 - len(str(only_number)))
            r_format = str(r_format) + ' ' * int(30 - len(str(r_format)))

            # Printing information
            final_output = f'''
        ┌──────────────────────────────────────────────────────┐
        | Scanned Phone Number: {Fore.LIGHTWHITE_EX}{phone_number} |
        |------------------------------------------------------|
        | {Fore.WHITE}INFORMATION         | {Fore.WHITE}DESCRIPTION                    |
        |------------------------------------------------------|
        | {Fore.WHITE}Posible             | {Fore.LIGHTWHITE_EX}{possible} |
        | {Fore.WHITE}Valid               | {Fore.LIGHTWHITE_EX}{valid} |
        |------------------------------------------------------|
        | {Fore.WHITE}Country Code        | {Fore.LIGHTWHITE_EX}{country_code} |
        | {Fore.WHITE}Country             | {Fore.LIGHTWHITE_EX}{country} |
        | {Fore.WHITE}Region Code         | {Fore.LIGHTWHITE_EX}{region_code} |
        | {Fore.WHITE}Service Provider    | {Fore.LIGHTWHITE_EX}{service_provider} |
        | {Fore.WHITE}Timezone            | {Fore.LIGHTWHITE_EX}{timezone_details} |
        |------------------------------------------------------|
        | {Fore.WHITE}International Format| {Fore.LIGHTWHITE_EX}{phone_number} |
        | {Fore.WHITE}National Format     | {Fore.LIGHTWHITE_EX}{only_number} |
        | {Fore.WHITE}RFC3966 Format      | {Fore.LIGHTWHITE_EX}{r_format} |
        └──────────────────────────────────────────────────────┘
            '''
            print(final_output)
            self.prv_op += final_output + '\n'

            # Online free lookup services
            online_free_lookup = f'''
        {Fore.YELLOW}[+] Searching for {Fore.LIGHTCYAN_EX}{phone_number.strip()}{Fore.YELLOW} on various platforms:
    
        {Fore.GREEN}> {Fore.WHITE}https://www.ipqualityscore.com/reverse-phone-number-lookup/lookup/{region_code.strip()}/{only_number.strip()}
        {Fore.GREEN}> {Fore.WHITE}https://www.truecaller.com/search/{region_code.strip().lower()}/{only_number.strip()}
        '''
            print(online_free_lookup)
            self.prv_op += online_free_lookup + '\n'

            # Google Dork Query to find more information about the number
            google_dork_queries = f'''
        {Fore.YELLOW}[+] Search engine lookup:
    
        {Fore.GREEN}> {Fore.WHITE}https://www.google.com/search?q={only_number.strip()}
        {Fore.GREEN}> {Fore.WHITE}https://www.google.com/search?q={phone_number.strip()}
        {Fore.GREEN}> {Fore.WHITE}https://www.bing.com/search?q={only_number.strip()}
        {Fore.GREEN}> {Fore.WHITE}https://www.bing.com/search?q={phone_number.strip()}
        {Fore.GREEN}> {Fore.WHITE}https://duckduckgo.com/?q={only_number.strip()}
        {Fore.GREEN}> {Fore.WHITE}https://duckduckgo.com/?q={phone_number.strip()}
        '''
            print(google_dork_queries)
            self.prv_op += google_dork_queries + '\n'

            # Scanning social media platforms
            social_media_platforms = f'''
        [+] Scanning social media platforms:
    
        {Fore.GREEN}> {Fore.WHITE}https://www.facebook.com/search/top?q={only_number.strip()}
        {Fore.GREEN}> {Fore.WHITE}https://www.facebook.com/search/top?q={phone_number.strip()}
        {Fore.GREEN}> {Fore.WHITE}https://www.instagram.com/{only_number.strip()}
        {Fore.GREEN}> {Fore.WHITE}https://www.instagram.com/{phone_number.strip()}
        {Fore.GREEN}> {Fore.WHITE}https://www.twitter.com/{only_number.strip()}
        {Fore.GREEN}> {Fore.WHITE}https://www.twitter.com/{phone_number.strip()}
        {Fore.GREEN}> {Fore.WHITE}https://www.linkedin.com/search/results/all/?keywords={only_number.strip()}
        {Fore.GREEN}> {Fore.WHITE}https://www.linkedin.com/search/results/all/?keywords={phone_number.strip()}
        {Fore.GREEN}> {Fore.WHITE}https://www.pinterest.com/search/pins/?q={only_number.strip()}
        {Fore.GREEN}> {Fore.WHITE}https://www.pinterest.com/search/pins/?q={phone_number.strip()}
        {Fore.GREEN}> {Fore.WHITE}https://www.tumblr.com/search/{only_number.strip()}
        {Fore.GREEN}> {Fore.WHITE}https://www.tumblr.com/search/{phone_number.strip()}
        {Fore.GREEN}> {Fore.WHITE}https://www.youtube.com/results?search_query={only_number.strip()}
        {Fore.GREEN}> {Fore.WHITE}https://www.youtube.com/results?search_query={phone_number.strip()}
        '''
            print(social_media_platforms)
            self.prv_op += social_media_platforms + '\n'
            return True

        else:
            # Reconfiguring variables
            possible = str(possible) + ' ' * int(30 - len(str(possible)))
            valid = str(valid) + ' ' * int(30 - len(str(valid)))
            phone_number = str(phone_number) + ' ' * int(30 - len(str(phone_number)))

            final_output = f'''
        ┌──────────────────────────────────────────────────────┐
        | Scanned Phone Number: {Fore.LIGHTWHITE_EX}{phone_number} |
        |------------------------------------------------------|
        | INFORMATION         | DESCRIPTION                    |
        |------------------------------------------------------|
        | {Fore.WHITE}Possible            | {Fore.LIGHTWHITE_EX}{possible} |
        | {Fore.WHITE}Valid               | {Fore.LIGHTWHITE_EX}{valid} |
        └──────────────────────────────────────────────────────┘
            '''
            print(final_output)
            self.prv_op += final_output + '\n'
            return False
