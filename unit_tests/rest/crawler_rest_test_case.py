import unittest
from unittest.mock import patch, MagicMock

from rest.CommonRequest import CommonRequestCall
from rest.WebsiteRequest import WebsiteRequest

crawlerRest = WebsiteRequest()
commonRestAPi = ()

BASE_URL = 'https:mock-uri'


class CommonRestApiTestCase(unittest.TestCase):

    @patch('urllib.request.urlopen')
    def test_rest_happy_path(self, mock_urlopen):
        mock_ = MagicMock()
        mock_.getcode.return_value = 200
        mock_.read.return_value = 'contents'
        mock_urlopen.return_value = mock_
        request_data = crawlerRest.get_properties_of_area(BASE_URL, 'CV1', 2)
        self.assertEqual(request_data, "contents")

    @patch('urllib.request.urlopen')
    def test_rest_handle_500_exception(self, mock_urlopen):
        mock_ = MagicMock()
        mock_.getcode.return_value = 500
        mock_.read.return_value = 'unavailable'
        mock_urlopen.return_value = mock_
        request_data = crawlerRest.get_properties_of_area(BASE_URL, 'CV1', 2)
        self.assertEqual(request_data, "unavailable")
