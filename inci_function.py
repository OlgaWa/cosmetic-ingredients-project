import pandas as pd
from cosing_db.db_utils import CosIng


class INCIFunction(CosIng):

    def __init__(self, name):
        self.name = name

    @classmethod
    def create_table(cls, filepath):

        data = pd.read_csv(filepath, encoding="utf-8")
        df = pd.DataFrame(data, columns=["Name", "Description"])
        df = df.astype(object).where(pd.notnull(df), None)

        cls.cursor.execute(f"CREATE TABLE {cls.__name__} "
                           "(ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                           "Name VARCHAR(50), Description VARCHAR(1000) )")

        for row in df.itertuples():
            sql = f"INSERT INTO " \
                  f"{cls.__name__} (Name, Description) " \
                  f"VALUES (%s, %s)"
            val = (row.Name, row.Description)

            cls.cursor.execute(sql, val)

        cls.my_db.commit()
        cls.cursor.close()
        cls.my_db.close()

    def _find_in_db(self):
        pass

    def show_info(self):
        pass
