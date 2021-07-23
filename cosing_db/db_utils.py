import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv(override=True)


class CosIng:

    my_db = mysql.connector.connect(
        host="localhost",
        user=os.environ["USER"],
        password=os.environ["DB_PASSWORD"],
        database="cos_ing_project"
    )

    cursor = my_db.cursor()
