import os
from dotenv import load_dotenv
import mysql.connector
import pandas as pd

load_dotenv()


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
