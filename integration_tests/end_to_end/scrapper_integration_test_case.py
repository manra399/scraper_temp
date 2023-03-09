import unittest
from unittest.mock import patch
import sys
import psycopg2

sys.path.insert(0, "..")

import pymsteams

from logger.logger import LoggingFile

sys.path.insert(0, "..")

from readers.postcodes_reader import PostcodeReader
from threads.threader import Threader

from configs.Config import Config

config = Config()
logging_=LoggingFile()


myTeamsMessage = pymsteams.connectorcard(config.get_team_hook_url())


class WebScrapperIntegrationTestCase(unittest.TestCase):

    @patch.object(PostcodeReader, 'get_postcodes')
    def test_get_zoopla_properties(self, postcode_reader):
        logger = logging_.get_logger(self.__class__.__name__)
        postcode_reader.return_value = ['CV32']
        threads = Threader()
        threads.execute()
        conn = psycopg2.connect(config.database_connection())
        cursor2 = conn.cursor()
        actual_properties = cursor2.execute("SELECT * FROM scrapper.images_data")
        if actual_properties <= 1:
            message = 'Scraper Intergration TestCase failed as properties in the output file are not saved.'
            myTeamsMessage.text(message)
            logger.error(message)
            myTeamsMessage.send()


