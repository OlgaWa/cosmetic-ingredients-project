import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode
from ingredient import Ingredient
from abbreviation import Abbreviation
from inci_function import INCIFunction
import logging

load_dotenv(override=True)


my_db = mysql.connector.connect(
    host="localhost",
    user=os.environ["USER"],
    password=os.environ["DB_PASSWORD"],
    database="cos_ing_project"
)

cursor = my_db.cursor()

try:
    Ingredient.create_table(
        f"{os.environ['COSING_CLEAN_PATH']}cosing_main_db.csv")
except mysql.connector.errors.ProgrammingError as err:
    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        logging.error(f"Table '{Ingredient.__name__.lower()}' already exists.",
                      exc_info=True)
    else:
        print(err.msg)


try:
    Abbreviation.create_table(
        f"{os.environ['COSING_CLEAN_PATH']}cosing_abbrev.csv")
except mysql.connector.errors.ProgrammingError as err:
    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        logging.error(f"Table '{Abbreviation.__name__.lower()}' already exists.",
                      exc_info=True)
    else:
        print(err.msg)
        
try:
    INCIFunction.create_table(
        f"{os.environ['COSING_CLEAN_PATH']}cosing_functions.csv")
except mysql.connector.errors.ProgrammingError as err:
    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        logging.error(f"Table '{INCIFunction.__name__.lower()}' already exists.",
                      exc_info=True)
    else:
        print(err.msg)

cursor.close()
