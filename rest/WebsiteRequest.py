import time

from logger.logger import LoggingFile
from rest.CommonRequest import CommonRequestCall

logging_ = LoggingFile()

class WebsiteRequest:
    # ---------------------HITTING THE FIRST PAGE OF A PARTICULAR POSTCODE WITH RETRIES IN CASE OF FAILURES---------
    def get_properties_of_area(self, url):
        logger = logging_.get_logger(self.__class__.__name__)
        common_request_call = CommonRequestCall()
        for i in range(8):
            try:
                request_data = common_request_call.rest_call_using_request(url.replace(' ',''))
            except:
                time.sleep(1)
                continue
            if request_data['status_code']!=200:
                time.sleep(1)
                continue
            else:
                return request_data['data']
                break
            if i_==7:
                return ''
