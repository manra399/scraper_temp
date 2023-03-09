from configs.Config import Config
from exceptions.csv_exporter_exception import CsvExporterException
from exceptions.invalid_file_exception import InvalidPostcodeException
from exceptions.proxy_exception import ProxyException
from logger.logger import LoggingFile
from threads.threader import Threader
import pymsteams


logging_ = LoggingFile()

config = Config()

myTeamsMessage = pymsteams.connectorcard(config.get_team_hook_url())


class Main:
    def execute_main(self):
        logger = logging_.get_logger(self.__class__.__name__)

        message = 'Zoopla Web Scraper Crawler STARTED'
        logger.info(message)
        threader = Threader()
        try:
            threader.execute()
        except InvalidPostcodeException | CsvExporterException | ProxyException as e:
            message = e.message
            logger.error(message)

        myTeamsMessage.text(message)
        myTeamsMessage.send()

        finish_message = 'Zoopla Web Scraper Crawler FINISHED'
        logger.info(finish_message)

        myTeamsMessage.text(finish_message)
        myTeamsMessage.send()


if __name__ == '__main__':
    main = Main()
    main.execute_main()
