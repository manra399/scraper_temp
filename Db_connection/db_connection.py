import psycopg2

from configs.Config import Config

config = Config()


class Db_connection:
    def db_cursor(self):
        try:
            conn = psycopg2.connect(config.database_connection())
            cursor_var=conn.cursor()
        except:
            pass
        return {'cursor_var': cursor_var, 'conn_var': conn}
        # return cursor_var
