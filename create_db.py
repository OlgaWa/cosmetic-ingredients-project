import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()


my_db = mysql.connector.connect(
  host="localhost",
  user=os.environ["USER"],
  password=os.environ["DB_PASSWORD"])

cursor = my_db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS cos_ing_project")
