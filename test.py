import unittest

from PyQt6.QtWidgets import QFileDialog

from HTTPrequest import HTTPrequest
from UI import check_api_key
from shodan import Shodan, APIError

# API Key no válida
apikey = "myapi"

# API Key válida
apikeyvalid = "Y0lQVErgyVSD60dg6HosPpU0fidW8dmq"
query = "tag:iot" #filtro no válido para API Key

url_attack = 'http://42.159.198.157:8081'


class Test(unittest.TestCase):
    def test_apikey(self):
        self.assertFalse(check_api_key(apikey))

    def test_shodan(self):
        shodan_browser = Shodan(apikeyvalid)
        with self.assertRaises(APIError):
            shodan_browser.search(query)

    def test_request(self):
        http_request = HTTPrequest()
        request = {'method': 'get', 'url': url_attack}
        response, result = http_request.request(request)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
