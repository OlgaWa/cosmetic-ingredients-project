import pandas as pnd
import os
from dotenv import load_dotenv


load_dotenv()

db_path = os.environ["COSING_DB_DIR"]
os.chdir(db_path)
db = os.environ["COSING_RAW"]

TABLE_START = 9
data_frame = pnd.read_csv(db, skiprows=TABLE_START)


df = pnd.DataFrame(data_frame, columns=["INCI name",
                                        "Chem/IUPAC Name / Description",
                                        "Function"])

df = df.rename(columns={"Chem/IUPAC Name / Description": "Description"})

df["INCI name"] = df["INCI name"].replace('[\(,\)]', '', regex=True)
df["INCI name"] = df["INCI name"].str.strip()

df = df.sort_values("INCI name")

clean_loc = os.environ['COSING_CLEAN_PATH']

df.to_csv(os.path.join(clean_loc, "cosing_main_db.csv"))
