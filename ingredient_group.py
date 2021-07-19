import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv(override=True)


my_db = mysql.connector.connect(
    host="localhost",
    user=os.environ["USER"],
    password=os.environ["DB_PASSWORD"],
    database="cos_ing_project"
)

cursor = my_db.cursor()


class IngredientGroup:

    def __init__(self, name):
        self.name = name

    def _find_in_db(self):
        pass

    def show_ingredients(self):
        pass
