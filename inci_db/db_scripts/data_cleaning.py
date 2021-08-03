import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv(override=True)


db_path = os.environ["COSING_DB_DIR"]
os.chdir(db_path)
db = os.environ["COSING_RAW"]

TABLE_START = 9
data_frame = pd.read_csv(db, skiprows=TABLE_START, encoding="utf-8")


df = pd.DataFrame(data_frame, columns=["INCI name",
                                       "Chem/IUPAC Name / Description",
                                       "Function"])

df = df.rename(columns={"INCI name": "INCI_name",
                        "Chem/IUPAC Name / Description": "Description"})

df["INCI_name"] = df["INCI_name"].replace("[\(,\)]", "", regex=True)
df["INCI_name"] = df["INCI_name"].str.strip()

df = df.sort_values("INCI_name")

clean_loc = os.environ["COSING_CLEAN_PATH"]

df.to_csv(os.path.join(clean_loc, "cosing_main_db.csv"))
