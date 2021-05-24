import pandas as pnd
import os
from dotenv import load_dotenv

load_dotenv()


db_path = os.environ["COS_ING_DB_DIR"]
os.chdir(db_path)
db = os.environ["COS_ING_RAW"]

data_frame = pnd.read_csv(db, skiprows = 9)

print(data_frame.shape)
print(data_frame.head(0))


df = pnd.DataFrame(data_frame, columns=["INCI name",
                                        "Chem/IUPAC Name / Description",
                                        "Function"])

df = df.rename(columns={"Chem/IUPAC Name / Description": "Description"})

df["INCI name"] = df["INCI name"].replace('[\(,\)," "]','', regex=True)
df = df.sort_values("INCI name")

df.to_csv(f"{db_path}/cosing_clean/cosing_main_db.csv")
