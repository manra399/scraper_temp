import concurrent.futures
from crawlers.zoopla_web_crawler import ZooplaWebCrawler
from readers.postcodes_reader import InputReader

class Threader:

    def execute(self):
        crawler = ZooplaWebCrawler()
        input_list_reader = InputReader()
        postcodes = input_list_reader.get_input_file_data()
        print('Total Number of Input List Items-', len(postcodes))
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for each in executor.map(crawler.district_extractor, postcodes):
                pass