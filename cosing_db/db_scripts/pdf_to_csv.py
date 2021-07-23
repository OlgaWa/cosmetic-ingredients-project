import tabula
import os
from dotenv import load_dotenv

load_dotenv(override=True)


db_path = os.environ["COSING_DB_DIR"]
clean_loc = os.environ["COSING_CLEAN_PATH"]
raw_loc = os.environ["COSING_RAW_PATH"]

if not os.path.exists(f"{clean_loc}cosing_abbrev.csv"):
    tabula.convert_into(f"{raw_loc}COSING_Abbreviations.pdf",
                        f"{clean_loc}cosing_abbrev.csv",
                        output_format="csv", pages="all")

if not os.path.exists(f"{clean_loc}cosing_functions.csv"):
    tabula.convert_into(f"{raw_loc}COSING_functions.pdf",
                        f"{clean_loc}cosing_functions.csv",
                        output_format="csv", pages="all")
