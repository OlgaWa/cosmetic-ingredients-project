import tabula
import os
from dotenv import load_dotenv

load_dotenv()


db_path = os.environ["COSING_DB_DIR"]
clean_loc = os.environ["COSING_CLEAN_PATH"]

if not os.path.exists(f"{clean_loc}/cosing_abbrev.csv"):
    tabula.convert_into("cosing_raw/COSING_Abbreviations.pdf",
                        f"{clean_loc}/cosing_abbrev.csv",
                        output_format="csv", pages="all")

if not os.path.exists(f"{clean_loc}/cosing_functions.csv"):
    tabula.convert_into("cosing_raw/COSING_functions.pdf",
                        f"{clean_loc}/cosing_functions.csv",
                        output_format="csv", pages="all")
