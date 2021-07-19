import os
from dotenv import load_dotenv
import mysql.connector
import pandas as pd

load_dotenv(override=True)


my_db = mysql.connector.connect(
    host="localhost",
    user=os.environ["USER"],
    password=os.environ["DB_PASSWORD"],
    database="cos_ing_project"
)

cursor = my_db.cursor()


class Abbreviation:

    def __init__(self, name):
        self.name = name

    @classmethod
    def create_table(cls, filepath):

        data = pd.read_csv(filepath, encoding="utf-8")
        df = pd.DataFrame(data,
                          columns=["Abbreviation", "Chemical substance"])
        df = df.rename(columns={"Chemical substance": "Chemical_substance"})
        df = df.astype(object).where(pd.notnull(df), None)

        cursor.execute(f"CREATE TABLE {cls.__name__} "
                       "(ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                       "Abbreviation VARCHAR(10), "
                       "Chemical_substance VARCHAR(100) )")

        for row in df.itertuples():
            sql = f"INSERT INTO " \
                  f"{cls.__name__} (Abbreviation, " \
                  f"Chemical_substance) " \
                  f"VALUES (%s, %s)"
            val = (row.Abbreviation, row.Chemical_substance)

            cursor.execute(sql, val)

        my_db.commit()

    def _find_in_fb(self):
        pass

    def get_ingredient(self):
        pass
