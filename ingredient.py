import pandas as pd
from cosing_db.db_utils import CosIng


class Ingredient(CosIng):

    def __init__(self, name):
        self.name = name

    @classmethod
    def create_table(cls, filepath):

        data = pd.read_csv(filepath, encoding="utf-8")
        df = pd.DataFrame(data,
                          columns=["INCI_name", "Description", "Function"])
        df = df.astype(object).where(pd.notnull(df), None)

        cls.cursor.execute(f"CREATE TABLE {cls.__name__} "
                           "(ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                           "INCI_name VARCHAR(5000), "
                           "INCI_description VARCHAR(5000), "
                           "INCI_function VARCHAR(500) )")

        for row in df.itertuples():
            sql = f"INSERT INTO " \
                  f"{cls.__name__} (INCI_name, " \
                  f"INCI_description, INCI_function) " \
                  f"VALUES (%s, %s, %s)"
            val = (row.INCI_name, row.Description, row.Function)

            cls.cursor.execute(sql, val)

        cls.my_db.commit()
        cls.cursor.close()
        cls.my_db.close()

    def _find_in_db(self):
        pass

    def get_description(self):
        pass

    def get_function(self):
        pass

    def get_similar(self):
        pass
