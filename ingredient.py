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


class Ingredient:

    def __init__(self, name):
        self.name = name

    @classmethod
    def create_table(cls, filepath):

        data = pd.read_csv(filepath, encoding="utf-8")
        df = pd.DataFrame(data,
                          columns=["INCI_name", "Description", "Function"])
        df = df.astype(object).where(pd.notnull(df), None)

        cursor.execute(f"CREATE TABLE {cls.__name__} "
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

            cursor.execute(sql, val)

        my_db.commit()

    def _find_in_db(self):
        pass

    def get_description(self):
        pass

    def get_function(self):
        pass

    def get_similar(self):
        pass
