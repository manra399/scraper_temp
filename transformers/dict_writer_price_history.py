import psycopg2
from lxml import etree
import json
import os
import requests
import time
from datetime import datetime

from logger.logger import LoggingFile
from configs.Config import Config

config = Config()

logging_ = LoggingFile()

class DictWriterPrices:
    @staticmethod
    def dict_writer_prices(in_data,conn):
        dtree = etree.HTML(in_data)
        try:
            proxies_pool = {
                    'http': 'http://'+os.environ['PROXY_USERNAME']+':'+os.environ['PROXY_PASSWORD']+'@'+os.environ['PROXY_API']+':'+os.environ['PROXY_PORT'],
                'https': 'http://'+os.environ['PROXY_USERNAME']+':'+os.environ['PROXY_PASSWORD']+'@'+os.environ['PROXY_API']+':'+os.environ['PROXY_PORT']
            }

        except Exception as e:

            print('issues at buidling proxy with environmental variables of proxies credentials',e)

        try:
            json_data = json.loads(dtree.xpath("//script[@id='__NEXT_DATA__']/text()")[0])
        except Exception as e:
            print('JSON DAta is not being rendered from the website URL in Prices History writer', e)
            return None

        headers_price = {
            'authority': 'api-graphql-lambda.prod.zoopla.co.uk',
            'method': 'POST',
            'path': '/graphql',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'content-length': '943',
            'content-type': 'application/json',
            'origin': 'https://www.zoopla.co.uk',
            'referer': 'https://www.zoopla.co.uk/',
            'x-api-key': '3Vzj2wUfaP3euLsV4NV9h3UAVUR3BoWd5clv9Dvu'
        }

        def Request_hit(listing_id_here):
            data_ = '{"operationName":"ListingHistory","variables":{"listingId":59737025},"query":"query ListingHistory($listingId: Int\u0021) {\\n  listingDetails(id: $listingId) {\\n    ... on ListingData {\\n      priceHistory {\\n        ...History\\n        __typename\\n      }\\n      viewCount {\\n        ...ViewCount\\n        __typename\\n      }\\n      __typename\\n    }\\n    ... on ListingResultError {\\n      errorCode\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\\nfragment History on PriceHistory {\\n  firstPublished {\\n    firstPublishedDate\\n    priceLabel\\n    __typename\\n  }\\n  lastSale {\\n    date\\n    newBuild\\n    price\\n    priceLabel\\n    recentlySold\\n    __typename\\n  }\\n  priceChanges {\\n    isMinorChange\\n    isPriceDrop\\n    isPriceIncrease\\n    percentageChangeLabel\\n    priceChangeDate\\n    priceChangeLabel\\n    priceLabel\\n    __typename\\n  }\\n  __typename\\n}\\n\\nfragment ViewCount on ViewCount {\\n  viewCount30day\\n  __typename\\n}\\n"}'
            sd_data = data_.replace('59737025',listing_id_here)
            fix_url = 'https://api-graphql-lambda.prod.zoopla.co.uk/graphql'
            try:
                response = requests.post(fix_url, headers=headers_price,data = sd_data, proxies=proxies_pool,timeout=5)
                if response.status_code != 200:
                    raise Exception
            except Exception as e:
                try:
                    response = requests.post(fix_url, headers=headers_price,data = sd_data, proxies=proxies_pool, timeout=5)
                    if response.status_code != 200:
                        raise Exception
                except Exception as e:
                    try:
                        response = requests.post(fix_url, headers=headers_price,data = sd_data, proxies=proxies_pool, timeout=5)
                        if response.status_code != 200:
                            raise Exception
                    except Exception as e:
                        time.sleep(1)
                        try:
                            response = requests.post(fix_url, headers=headers_price,data = sd_data, proxies=proxies_pool, timeout=5)
                            if response.status_code != 200:
                                raise Exception
                        except Exception as e:
                            print('Exception in hitting Request on this URL  ', e)
                            return None
            print(response.status_code)
            return response


        try:
            json_prices_data = json.loads(Request_hit(str(json_data['props']['pageProps']['listingDetails']['listingId'].strip())).text)
        except:
            return None
        inside_prices_list = []
        try:
            inside_prices_list.append(json_prices_data['data']['listingDetails']['priceHistory']['firstPublished'])
        except:
            pass
        try:
            inside_prices_list.append(json_prices_data['data']['listingDetails']['priceHistory']['lastSale'])
        except:
            pass
        try:
            for each_price_change in json_prices_data['data']['listingDetails']['priceHistory']['priceChanges']:
                inside_prices_list.append(each_price_change)
        except:
            pass
        if len(inside_prices_list)!=0:
            try:
                cursor2 = conn.cursor()
            except Exception as e:
                print('exception at creating connection in PRices history', e)
            for prices_to_write in inside_prices_list:
                dict_ = {}
                dict_['last_update'] = datetime.today().strftime('%Y-%m-%d')
                try:
                    dict_['price_history'] = prices_to_write['priceLabel'].replace('\xa3','').strip()
                except:
                    break
                try:
                    dict_['firstpublishedDate'] = prices_to_write['firstPublishedDate'].replace('\xa3','').strip()
                except:
                    try:
                        dict_['firstpublishedDate'] = prices_to_write['date'].replace('\xa3', '').strip()
                    except:
                        try:
                            dict_['firstpublishedDate'] = prices_to_write['priceChangeDate'].replace('\xa3', '').strip()
                        except:
                            dict_['firstpublishedDate'] = None
                try:
                    dict_['PropertyID'] = json_data['props']['pageProps']['listingDetails']['listingId'].strip()
                except:
                    dict_['PropertyID'] = None
                try:
                    dict_['is_inserted'] = 'updated'
                    cursor2.execute(
                        'UPDATE scrapper.zoopla_prices_history SET last_update=%(last_update)s, price_history=%(price_history)s, firstpublishedDate=%(firstpublishedDate)s, PropertyID=%(PropertyID)s, is_inserted=%(is_inserted)s where PropertyID=%(PropertyID)s and price_history=%(price_history)s',
                        dict_)
                    if cursor2.rowcount == 0:
                        dict_['is_inserted'] = 'inserted'
                        cursor2.execute(
                            "INSERT INTO scrapper.zoopla_prices_history (last_update,price_history,firstpublishedDate,PropertyID,is_inserted) "
                            "VALUES( %(last_update)s, %(price_history)s, %(firstpublishedDate)s, %(PropertyID)s,%(is_inserted)s)", dict_
                        )
                    conn.commit()

                except Exception as e:
                    try:
                        conn.commit()
                    except:
                        try:
                            cursor2.execute("rollback")
                        except:
                            print('Exception in writing data to the DB price history',e)
                            pass

