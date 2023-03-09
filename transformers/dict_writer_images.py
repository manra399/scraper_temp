from lxml import etree
import json
from datetime import datetime

from logger.logger import LoggingFile
from configs.Config import Config

config = Config()


logging_ = LoggingFile()

class DictWriterImages:
    @staticmethod
    def dict_writer_images(in_data,conn):
        dtree = etree.HTML(in_data)
        try:
            cursor2 = conn.cursor()

        except Exception as e:
            print('exception at creating connection inside Images writing', e)
        try:
            json_data = json.loads(dtree.xpath("//script[@id='__NEXT_DATA__']/text()")[0])
        except Exception as e:
            print('JSON DAta is not being rendered from the website URL Error in Images Writer', e)
            return None
        i = 0
        try:
            for ii in json_data['props']['pageProps']['listingDetails']['propertyImage']:
                i = i+1
                dict_ = {}
                dict_['last_update'] = datetime.today().strftime('%Y-%m-%d')
                try:
                    dict_['Photo_media'] = ii['__typename']
                except:
                    dict_['Photo_media'] = None
                try:
                    dict_['Image_URL'] = 'https://lc.zoocdn.com/'+ii['filename']
                except:
                    dict_['Image_URL'] = None
                try:
                    dict_['Image_Caption'] = ii['caption']
                except:
                    dict_['Image_Caption'] = None
                try:
                    dict_['PropertyID'] = json_data['props']['pageProps']['listingDetails']['listingId']
                except:
                    dict_['PropertyID'] = None
                try:
                    dict_['Image_count'] = str(i)
                except:
                    dict_['Image_count'] = None
                dict_['is_inserted'] = 'updated'
                try:
                    cursor2.execute('UPDATE scrapper.zoopla_images SET last_update=%(last_update)s, Photo_media=%(Photo_media)s, Image_URL=%(Image_URL)s, Image_Caption=%(Image_Caption)s, PropertyID=%(PropertyID)s, Image_count=%(Image_count)s, is_inserted=%(is_inserted)s where PropertyID=%(PropertyID)s and Image_count=%(Image_count)s',dict_)
                    if cursor2.rowcount == 0:
                        dict_['is_inserted'] = 'inserted'
                        cursor2.execute(
                            "INSERT INTO scrapper.zoopla_images (last_update,Photo_media,Image_URL,Image_Caption,PropertyID,Image_count,is_inserted) "
                            "VALUES( %(last_update)s, %(Photo_media)s, %(Image_URL)s, %(Image_Caption)s, %(PropertyID)s, %(Image_count)s, %(is_inserted)s)", dict_
                        )
                    conn.commit()
                except Exception as e:
                    try:
                        conn.commit()
                    except:
                        try:
                            cursor2.execute("rollback")
                        except:
                            print('Exception in writing images data',e)
                            pass
        except:
            return None
