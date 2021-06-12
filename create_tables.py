import os
from dotenv import load_dotenv
import mysql.connector
from ingredients import Ingredient, Abbreviation, Function

load_dotenv()


my_db = mysql.connector.connect(
    host="localhost",
    user=os.environ["USER"],
    password=os.environ["DB_PASSWORD"],
    database="cos_ing_project"
)

cursor = my_db.cursor()


Ingredient.create_table(f"{os.environ['COSING_CLEAN_PATH']}cosing_main_db.csv")
Abbreviation.create_table(f"{os.environ['COSING_CLEAN_PATH']}cosing_abbrev.csv")
Function.create_table(f"{os.environ['COSING_CLEAN_PATH']}cosing_functions.csv")

cursor.close()
