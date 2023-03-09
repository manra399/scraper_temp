import unittest
from unittest.mock import patch
from crawlers.zoopla_web_crawler import ZooplaWebCrawler
from rest.WebsiteRequest import ZooplaRequest
from configs.Config import Config

zoopla_rest = ZooplaRequest()
zooplaWebCrawler = ZooplaWebCrawler()

config = Config()

zoopla_url = config.get_zoopla_url()

property_csv = []
images_csv = []


class ZooplaWebCrawlerTestCase(unittest.TestCase):

    @patch.object(ZooplaRequest,'get_properties_of_area')
    def test_get_property_csv(self, zoopla_rest):
        zoopla_rest.return_value ='string case HTML'
        csvs = zooplaWebCrawler.district_extractor('AB10')
        self.assertEqual(csvs,None)