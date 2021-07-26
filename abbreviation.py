import pandas as pd
from cosing_db.db_utils import CosIng


class Abbreviation(CosIng):

    def __init__(self, name):
        self.name = name

    @classmethod
    def create_table(cls, filepath):

        my_db = super().db_connect()
        cursor = my_db.cursor()

        table_name = cls.__name__.lower()

        data = pd.read_csv(filepath, encoding="utf-8")
        df = pd.DataFrame(data,
                          columns=["Abbreviation", "Chemical substance"])
        df = df.rename(columns={"Chemical substance": "Chemical_substance"})
        df = df.astype(object).where(pd.notnull(df), None)

        cursor.execute(f"CREATE TABLE {table_name} "
                       "(ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                       "substance_abbrev VARCHAR(10), "
                       "chemical_substance VARCHAR(100) )")

        for row in df.itertuples():
            sql = f"INSERT INTO " \
                  f"{table_name} (substance_abbrev, " \
                  f"chemical_substance) " \
                  f"VALUES (%s, %s)"
            val = (row.Abbreviation, row.Chemical_substance)

            cursor.execute(sql, val)

        my_db.commit()
        cursor.close()
        my_db.close()

    def _find_in_db(self):
        pass

    def get_ingredient(self):
        pass
