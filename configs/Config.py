import configparser

config = configparser.ConfigParser()


class Config:

    def __init__(self):
        if not config.read('configs/resources/main/config.ini'):
             config.read('../../configs/resources/other/config.ini')


    def get_txt_output_path(self):
        return  config['LOG_PATHS']['TXT_OUTPUT_PATH']

    def get_csv_input_path(self):
        return config['CVS_PATHS']['CSV_INPUT_PATH']

    def get_team_hook_url(self):
        return config['TEAMS']['TEAMS_HOOK_URL']

    def get_zoopla_url(self):
        return config['ZOOPLA']['ZOOPLA_URL']

    def database_connection(self):
        return config['DBConn']['DB']
