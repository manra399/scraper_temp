import pandas as pd
import pymsteams

from configs.Config import Config
from exceptions.invalid_file_exception import InvalidFileException
from logger.logger import LoggingFile

config = Config()
logging_ = LoggingFile()
myTeamsMessage = pymsteams.connectorcard(config.get_team_hook_url())

class InputReader:

    def get_input_file_data(self):
        logger = logging_.get_logger(self.__class__.__name__)
        try:
            areas_file = pd.read_csv(config.get_csv_input_path())
            return areas_file['enter_column_name_here'].to_list()
        except Exception as e:
            logger.error(e)
            raise InvalidFileException('Scraper Code CSV file has not been accessed.Check issue manually.Error Code is --')

