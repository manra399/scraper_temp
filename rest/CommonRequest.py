import os
import requests
import time
from configs.Config import Config

config = Config()


class CommonRequestCall:

    def rest_call_using_request(self, req):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        }
        try:
            proxies_pool = {
                    'http': 'http://'+os.environ['PROXY_USERNAME']+':'+os.environ['PROXY_PASSWORD']+'@'+os.environ['PROXY_API']+':'+os.environ['PROXY_PORT'],
                'https': 'http://'+os.environ['PROXY_USERNAME']+':'+os.environ['PROXY_PASSWORD']+'@'+os.environ['PROXY_API']+':'+os.environ['PROXY_PORT']
            }

        except Exception as e:

            print('issues at building proxy with environmental variables of proxies credentials',e)
        try:
            r = requests.get(req,proxies = proxies_pool,timeout=5)
        except Exception as e:
            time.sleep(1)
            try:
                r = requests.get(req,proxies = proxies_pool, timeout=5)
            except Exception as e:
                try:
                    r = requests.get(req,proxies = proxies_pool, timeout=5)
                except Exception as e:
                    try:
                        r = requests.get(req,proxies = proxies_pool, timeout=5)
                    except Exception as e:
                        time.sleep(2)
                        try:
                            r = requests.get(req, proxies=proxies_pool, timeout=5)
                        except Exception as e:
                            time.sleep(2)
                            print(e)
                            try:
                                r = requests.get(req, proxies=proxies_pool, timeout=5)
                            except Exception as e:
                                time.sleep(1)
                                try:
                                    r = requests.get(req, proxies=proxies_pool, timeout=5,verify=False)
                                except Exception as e:
                                    print('Level 6 retry didnt work', e)
        return {'status_code': r.status_code, 'data': r.text}
