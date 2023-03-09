import pandas
import unittest
import pandas as pd
from unittest.mock import patch
from readers.postcodes_reader import InputReader
from exceptions.invalid_file_exception import InvalidFileException

postcode_reader = InputReader()


class PostcodeReaderTestCase(unittest.TestCase):

    @patch.object(pandas, 'read_csv')
    def test_happy_path(self, pandas):
        data = [['CV1'], ['CV2']]
        df = pd.DataFrame(data, columns=['Enter_column_name_here'])
        pandas.return_value = df
        property_data = postcode_reader.get_input_file_data()
        self.assertEqual(property_data, ['CV1', 'CV2'])

    @patch.object(pandas, 'read_csv')
    def test_should_return_empty_district_list_when_postcode_reader_called(self, pandas):
        df = pd.DataFrame([['']], columns=['Enter_column_name_here'])
        pandas.return_value = df
        property_data = postcode_reader.get_input_file_data()
        self.assertEqual(property_data, [''])

    @patch.object(pandas, 'read_csv')
    def test_should_throw_exception_when_postcode_reader_called(self, pandas):
        df = pd.DataFrame([['']])
        pandas.return_value = df
        try:
            postcode_reader.get_input_file_data()
        except InvalidFileException as e:
            self.assertEqual(e.message, 'Input CSV file has not been accessed.Check issue manually.Error Code is --')

