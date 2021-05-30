import tabula
import os
from dotenv import load_dotenv

load_dotenv()


# Create folder for the clean data.
db_path = os.environ["COS_ING_DB_DIR"]
clean_loc = f"{db_path}/cosing_clean"

# Convert two files in PDF to CSV.
if not os.path.exists(f"{clean_loc}/cosing_abbrev.csv"):
    tabula.convert_into("cosing_raw/COSING_Abbreviations.pdf",
                        f"{clean_loc}/cosing_abbrev.csv",
                        output_format="csv", pages="all")

if not os.path.exists(f"{clean_loc}/cosing_functions.csv"):
    tabula.convert_into("cosing_raw/COSING_functions.pdf",
                        f"{clean_loc}/cosing_functions.csv",
                        output_format="csv", pages="all")
