from lxml import etree
import json
from datetime import datetime

from logger.logger import LoggingFile
from configs.Config import Config

config = Config()


logging_ = LoggingFile()

class DictWriterTransformer:
    @staticmethod
    def dict_writer(in_data,conn):
        try:
            dtree = etree.HTML(in_data.encode("ascii",'replace'))
        except Exception as e:
            print('issues in creating ascii encoding',e)
        try:
            json_data = json.loads(dtree.xpath("//script[@id='__NEXT_DATA__']/text()")[0].replace('\u2032','').replace('\u2019','').replace('\u2022','').replace('\u2013','').replace('\xa3','').replace('\u201c',''))
        except Exception as e:
            try:
                json_data = json.loads(dtree.xpath("//script[@id='__NEXT_DATA__']/text()")[0])
            except Exception as e:
                print('JSON DAta is not being rendered from the website URL in main Properties writer', e)
                return None
        try:
            cursor2 = conn.cursor()
        except Exception as e:
            print('exception at creating connection in writing properties', e)
        dict_ = {}
        dict_['last_update']=datetime.today().strftime('%d-%m-%Y')
        try:
            dict_['listingid'] = json_data['props']['pageProps']['listingDetails']['listingId'].strip()
        except:
            dict_['listingid'] = None
        try:
            dict_['PublishedOn'] = json_data['props']['pageProps']['listingDetails']['priceHistory']['firstPublished']['firstPublishedDate']
        except:
            try:
                dict_['PublishedOn'] = json_data['props']['pageProps']['listingDetails']['publishedOn'].split('T')[0]
            except:
                dict_['PublishedOn'] = None
        try:
            dict_['BranchID'] = str(json_data['props']['pageProps']['listingDetails']['adTargeting']['branchId'])
        except:
            dict_['BranchID'] = None
        try:
            dict_['displayaddress'] = json_data['props']['pageProps']['listingDetails']['displayAddress'].strip()
        except:
            dict_['displayaddress'] = None
        try:
            dict_['regionname'] =json_data['props']['pageProps']['listingDetails']['adTargeting']['regionName'].strip()
        except:
            dict_['regionname'] = None
        try:
            dict_['Postalcode'] = json_data['props']['pageProps']['listingDetails']['adTargeting']['outcode'].strip()+' '+json_data['props']['pageProps']['listingDetails']['adTargeting']['incode'].strip()
        except:
            dict_['Postalcode'] = None
        try:
            dict_['postalArea'] =json_data['props']['pageProps']['listingDetails']['adTargeting']['postalArea'].strip()
        except:
            dict_['postalArea'] = None
        try:
            dict_['listingcondition'] = json_data['props']['pageProps']['listingDetails']['adTargeting']['listingCondition'].strip()
        except:
            dict_['listingcondition'] = None
        try:
            dict_['listingcategory'] = json_data['props']['pageProps']['listingDetails']['adTargeting']['section'].strip()
        except:
            dict_['listingcategory'] = None
        try:
            dict_['price'] = json_data['props']['pageProps']['listingDetails']['pricing']['label'].replace(' ','').replace(',','').replace('£','').replace('?','').strip()
        except:
            dict_['price'] = None

        try:
            dict_['Lat'] = str(json_data['props']['pageProps']['listingDetails']['location']['coordinates']['latitude'])
        except:
            dict_['Lat'] = None
        try:
            dict_['Long'] = str(json_data['props']['pageProps']['listingDetails']['location']['coordinates']['longitude'])
        except:
            dict_['Long']=None
        try:
            dict_['companyID'] = str(json_data['props']['pageProps']['listingDetails']['adTargeting']['companyId'])
        except:
            dict_['companyID']=None
        try:
            dict_['section'] = json_data['props']['pageProps']['listingDetails']['adTargeting']['section']
        except:
            dict_['section']= None
        try:
            dict_['Active_Status'] = None
        except:
            dict_['Active_Status'] = None
        try:
            dict_['property_type'] = json_data['props']['pageProps']['listingDetails']['category']
        except:
            dict_['property_type'] = None
        try:
            dict_['numBaths'] = json_data['props']['pageProps']['listingDetails']['adTargeting']['numBaths']
        except:
            dict_['numBaths'] = None
        try:
            dict_['numBeds'] = json_data['props']['pageProps']['listingDetails']['adTargeting']['numBeds']
        except:
            dict_['numBeds'] = None
        try:
            dict_['sizeSqFt'] = json_data['props']['pageProps']['listingDetails']['analyticsTaxonomy']['sizeSqFeet']
        except:
            dict_['sizeSqFt'] = None
        try:
            dict_['furnishedstate'] = json_data['props']['pageProps']['listingDetails']['features']['flags']['furnishedState']['label']
        except:
            dict_['furnishedstate'] = None
        try:
            dict_['isretirementhome'] = json_data['props']['pageProps']['listingDetails']['adTargeting']['isRetirementHome']
        except:
            dict_['isretirementhome'] = None
        try:
            dict_['issharedownership'] = json_data['props']['pageProps']['listingDetails']['adTargeting']['isSharedOwnership']
        except:
            dict_['issharedownership'] = None
        try:
            dict_['student_friendly'] = json_data['props']['pageProps']['listingDetails']['features']['flags']['studentFriendly']
        except:
            dict_['student_friendly'] = None
        try:
            if type(json_data['props']['pageProps']['listingDetails']['features']['flags']['tenure'])==dict:
                raise Exception
            else:
                dict_['tenure'] = json_data['props']['pageProps']['listingDetails']['features']['flags']['tenure']
        except:
            try:
                dict_['tenure'] = json_data['props']['pageProps']['listingDetails']['features']['flags']['tenure']['name']
            except:
                dict_['tenure'] = None
        try:
            if type(json_data['props']['pageProps']['listingDetails']['epc']['pdf'])==list:
                raise Exception
            if type(json_data['props']['pageProps']['listingDetails']['epc']['pdf'])==dict:
                raise Exception
            dict_['EPC_pdf'] = json_data['props']['pageProps']['listingDetails']['epc']['pdf']
        except:
            try:
                dict_['EPC_pdf'] = json_data['props']['pageProps']['listingDetails']['epc']['pdf'][0]['original']
            except:
                dict_['EPC_pdf'] = None
        try:
            dict_['metatitle'] = json_data['props']['pageProps']['listingDetails']['metaTitle'].strip()
        except:
            dict_['metatitle'] = None
        try:
            dict_['meta_description'] = json_data['props']['pageProps']['listingDetails']['metaDescription'].strip()
        except:
            dict_['meta_description'] = None
        try:
            dict_['propertyHighlight'] = json_data['props']['pageProps']['listingDetails']['adTargeting']['propertyHighlight']
        except:
            dict_['propertyHighlight'] = None
        try:
            dict_['detailed_description'] = json_data['props']['pageProps']['listingDetails']['detailedDescription'].strip()
        except:
            dict_['detailed_description'] = None
        try:
            dict_['numLivingRoom'] = json_data['props']['pageProps']['listingDetails']['counts']['numLivingRooms']
        except:
            dict_['numLivingRoom'] = None
        try:
            dict_['price_perfloorareaunit'] = int(json_data['props']['pageProps']['listingDetails']['pricing']['pricePerFloorAreaUnit'])
        except:
            try:
                dict_['price_perfloorareaunit'] = int(json_data['props']['pageProps']['listingDetails']['pricing']['pricePerFloorAreaUnit']['internalValue'])
            except:
                dict_['price_perfloorareaunit'] = None
        try:
            if type(json_data['props']['pageProps']['listingDetails']['epc']['image'])==list:
                raise Exception
            else:
                dict_['EPC_image'] = json_data['props']['pageProps']['listingDetails']['epc']['image']
        except:
            try:
                dict_['EPC_image'] = 'https://lc.zoocdn.com/'+json_data['props']['pageProps']['listingDetails']['epc']['image'][0]['filename']
            except:
                dict_['EPC_image'] = None
        try:
            if type(json_data['props']['pageProps']['listingDetails']['floorPlan']['image'])==list:
                raise Exception
            else:
                dict_['Floor_plan_image'] = json_data['props']['pageProps']['listingDetails']['floorPlan']['image']
        except:
            try:
                dict_['Floor_plan_image'] = 'https://lc.zoocdn.com/' +str(json_data['props']['pageProps']['listingDetails']['floorPlan']['image'][0]['filename'])
            except:
                dict_['Floor_plan_image'] = None
        try:
            dict_['Floor_plan_pdf'] = json_data['props']['pageProps']['listingDetails']['floorPlan']['pdf'][0]['original']
        except:
            dict_['Floor_plan_pdf'] = None
        try:
            dict_['added_date'] = json_data['props']['pageProps']['listingDetails']['priceHistory']['firstPublished']['firstPublishedDate'].strip()
        except:
            dict_['added_date'] = None
        try:
            dict_['availablefrom_date'] = json_data['props']['pageProps']['listingDetails']['features']['flags']['availableFromDate']
        except:
            dict_['availablefrom_date'] = None
        try:
            dict_['title'] = json_data['props']['pageProps']['listingDetails']['metaTitle'].strip()
        except:
            dict_['title'] = None
        try:
            dict_['URL'] = 'https://www.zoopla.co.uk' + json_data['props']['pageProps']['listingDetails']['listingUris']['detail']
        except:
            dict_['URL'] = None
        try:
            dict_['Features'] = '-- '.join([i for i in json_data['props']['pageProps']['listingDetails']['features']['bullets']])
        except:
            dict_['Features'] = None
        try:
            dict_['Highlights'] = ','.join([i['label'] for i in json_data['props']['pageProps']['listingDetails']['features']['highlights']])
        except:
            dict_['Highlights'] = None
        try:
            dict_['countrycode'] = json_data['props']['pageProps']['listingDetails']['adTargeting']['countryCode']
        except:
            dict_['countrycode'] = None
        try:
            dict_['currencyCode'] = json_data['props']['pageProps']['listingDetails']['adTargeting']['currencyCode']
        except:
            dict_['currencyCode'] = None
        try:
            dict_['updated_date'] = None
        except:
            dict_['updated_date'] = None
        try:
            dict_['is_inserted'] = 'updated'
            cursor2.execute(
                'UPDATE scrapper.zoopla_properties SET last_update=%(last_update)s, listingid=%(listingid)s, PublishedOn=%(PublishedOn)s, BranchID=%(BranchID)s, displayaddress=%(displayaddress)s, regionname=%(regionname)s, Postalcode=%(Postalcode)s, postalArea=%(postalArea)s, listingcondition=%(listingcondition)s, listingcategory=%(listingcategory)s, price=%(price)s, Lat=%(Lat)s, Long=%(Long)s, companyID=%(companyID)s, section=%(section)s, Active_Status=%(Active_Status)s, property_type=%(property_type)s, numBaths=%(numBaths)s, numBeds=%(numBeds)s, sizeSqFt=%(sizeSqFt)s, furnishedstate=%(furnishedstate)s, isretirementhome=%(isretirementhome)s, issharedownership=%(issharedownership)s, student_friendly=%(student_friendly)s, tenure=%(tenure)s, EPC_pdf=%(EPC_pdf)s, metatitle=%(metatitle)s, meta_description=%(meta_description)s, propertyHighlight=%(propertyHighlight)s, detailed_description=%(detailed_description)s, numLivingRoom=%(numLivingRoom)s, price_perfloorareaunit=%(price_perfloorareaunit)s, EPC_image=%(EPC_image)s, Floor_plan_image=%(Floor_plan_image)s, Floor_plan_pdf=%(Floor_plan_pdf)s, added_date=%(added_date)s, availablefrom_date=%(availablefrom_date)s, title=%(title)s, URL=%(URL)s, Features=%(Features)s, Highlights=%(Highlights)s, countrycode=%(countrycode)s, currencyCode=%(currencyCode)s, updated_date=%(updated_date)s, is_inserted=%(is_inserted)s  where listingid=%(listingid)s',
                dict_)
            if cursor2.rowcount == 0:
                dict_['is_inserted'] = 'inserted'
                cursor2.execute(
                    "INSERT INTO scrapper.zoopla_properties (last_update,listingid,PublishedOn,BranchID,displayaddress,regionname,Postalcode,postalArea,listingcondition,listingcategory,price,Lat,Long,companyID,section,Active_Status,property_type,numBaths,numBeds,sizeSqFt,furnishedstate,isretirementhome,issharedownership,student_friendly,tenure,EPC_pdf,metatitle,meta_description,propertyHighlight,detailed_description,numLivingRoom,price_perfloorareaunit,EPC_image,Floor_plan_image,Floor_plan_pdf,added_date,availablefrom_date,title,URL,Features,Highlights,countrycode,currencyCode,updated_date,is_inserted) "
                    "VALUES( %(last_update)s, %(listingid)s, %(PublishedOn)s, %(BranchID)s, %(displayaddress)s, %(regionname)s, %(Postalcode)s, %(postalArea)s, %(listingcondition)s, %(listingcategory)s, %(price)s, %(Lat)s, %(Long)s, %(companyID)s, %(section)s, %(Active_Status)s, %(property_type)s, %(numBaths)s, %(numBeds)s, %(sizeSqFt)s, %(furnishedstate)s, %(isretirementhome)s, %(issharedownership)s, %(student_friendly)s, %(tenure)s, %(EPC_pdf)s, %(metatitle)s, %(meta_description)s, %(propertyHighlight)s, %(detailed_description)s, %(numLivingRoom)s, %(price_perfloorareaunit)s, %(EPC_image)s, %(Floor_plan_image)s, %(Floor_plan_pdf)s, %(added_date)s, %(availablefrom_date)s, %(title)s, %(URL)s, %(Features)s, %(Highlights)s, %(countrycode)s, %(currencyCode)s, %(updated_date)s, %(is_inserted)s)",
                    dict_
                )
            conn.commit()
        except Exception as e:
            try:
                conn.commit()
            except:
                try:
                    cursor2.execute("rollback")
                except:
                    print('Exception at writing data to the transformer',e)
                    pass
