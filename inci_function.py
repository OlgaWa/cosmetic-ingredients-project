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


class INCIFunction:

    def __init__(self, name):
        self.name = name

    @classmethod
    def create_table(cls, filepath):

        data = pd.read_csv(filepath, encoding="utf-8")
        df = pd.DataFrame(data, columns=["Name", "Description"])
        df = df.astype(object).where(pd.notnull(df), None)

        cursor.execute(f"CREATE TABLE {cls.__name__} "
                       "(ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                       "Name VARCHAR(50), Description VARCHAR(1000) )")

        for row in df.itertuples():
            sql = f"INSERT INTO " \
                  f"{cls.__name__} (Name, Description) " \
                  f"VALUES (%s, %s)"
            val = (row.Name, row.Description)

            cursor.execute(sql, val)

        my_db.commit()

    def _find_in_db(self):
        pass

    def show_info(self):
        pass
