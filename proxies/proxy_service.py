from urllib import request
import pymsteams
from exceptions.proxy_exception import ProxyException
from logger.logger import LoggingFile

logging_=LoggingFile()
myTeamsMessage = pymsteams.connectorcard("Enter_your_teams_url_here")

class ProxyService:
    def embed_proxies(self):
        logger = logging_.get_logger(self.__class__.__name__)
        try:
            proxies_pool = {
                'http': 'http://uSER-dc-us:password@url:port',
                'https': 'http://uSER-dc-us:password@url:port'
            }
            proxy_support = request.ProxyHandler(proxies_pool)
            opener = request.build_opener(proxy_support)
            request.install_opener(opener)
        except Exception as e:
            logger.error(e)
            raise ProxyException(e.message)
