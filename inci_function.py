import pandas as pd
from cosing_db.db_utils import CosIng


class INCIFunction(CosIng):

    def __init__(self, name):
        self.name = name

    @classmethod
    def create_table(cls, filepath):

        my_db = super().db_connect()
        cursor = my_db.cursor()

        table_name = cls.__name__.lower()

        data = pd.read_csv(filepath, encoding="utf-8")
        df = pd.DataFrame(data, columns=["Name", "Description"])
        df = df.astype(object).where(pd.notnull(df), None)

        cursor.execute(f"CREATE TABLE {table_name} "
                       "(ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                       "name VARCHAR(50), description VARCHAR(1000) )")

        for row in df.itertuples():
            sql = f"INSERT INTO " \
                  f"{table_name} (name, description) " \
                  f"VALUES (%s, %s)"
            val = (row.Name, row.Description)

            cursor.execute(sql, val)

        my_db.commit()
        cursor.close()
        my_db.close()

    def _find_in_db(self):
        pass

    def show_info(self):
        pass
