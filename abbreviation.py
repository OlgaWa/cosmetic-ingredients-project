import pandas as pd
from cosing_db.db_utils import CosIng


class Abbreviation(CosIng):

    def __init__(self, name):
        self.name = name

    @classmethod
    def create_table(cls, filepath):

        data = pd.read_csv(filepath, encoding="utf-8")
        df = pd.DataFrame(data,
                          columns=["Abbreviation", "Chemical substance"])
        df = df.rename(columns={"Chemical substance": "Chemical_substance"})
        df = df.astype(object).where(pd.notnull(df), None)

        cls.cursor.execute(f"CREATE TABLE {cls.__name__} "
                           "(ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                           "Abbreviation VARCHAR(10), "
                           "Chemical_substance VARCHAR(100) )")

        for row in df.itertuples():
            sql = f"INSERT INTO " \
                  f"{cls.__name__} (Abbreviation, " \
                  f"Chemical_substance) " \
                  f"VALUES (%s, %s)"
            val = (row.Abbreviation, row.Chemical_substance)

            cls.cursor.execute(sql, val)

        cls.my_db.commit()
        cls.cursor.close()
        cls.my_db.close()

    def _find_in_db(self):
        pass

    def get_ingredient(self):
        pass
