import pandas as pd
from cosing_db.db_utils import CosIng


class Abbreviation(CosIng):

    def __init__(self, name):
        self.name = name

    @classmethod
    def create_table(cls, filepath):

        my_db = super().db_connect()
        cursor = my_db.cursor()

        table_name = cls.__name__.lower()

        data = pd.read_csv(filepath, encoding="utf-8")
        df = pd.DataFrame(data,
                          columns=["Abbreviation", "Chemical substance"])
        df = df.rename(columns={"Chemical substance": "Chemical_substance"})
        df = df.astype(object).where(pd.notnull(df), None)

        cursor.execute(f"CREATE TABLE {table_name} "
                       "(ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                       "substance_abbrev VARCHAR(10), "
                       "chemical_substance VARCHAR(100) )")

        for row in df.itertuples():
            sql = f"INSERT INTO " \
                  f"{table_name} (substance_abbrev, " \
                  f"chemical_substance) " \
                  f"VALUES (%s, %s)"
            val = (row.Abbreviation, row.Chemical_substance)

            cursor.execute(sql, val)

        my_db.commit()
        cursor.close()
        my_db.close()

    def get_ingredient(self):
        my_db = super().db_connect()
        cursor = my_db.cursor()

        try:
            cursor.execute("SELECT chemical_substance FROM "
                           "abbreviation WHERE substance_abbrev=%s",
                           (self.name,))
            ingredient = cursor.fetchall()[0][0]

            cursor.close()
            my_db.close()

            return ingredient

        except (ValueError, IndexError):
            cursor.close()
            my_db.close()

            return f"It seems we don't have {self.name} " \
                   f"in our database. Please try again!"

    def get_abbrev_in(self):
        my_db = super().db_connect()
        cursor = my_db.cursor()

        try:
            cursor.execute("SELECT chemical_substance FROM "
                           "abbreviation WHERE substance_abbrev LIKE %s",
                           ("%" + self.name + "%",))
            result = cursor.fetchall()
            cursor.execute("SELECT substance_abbrev FROM "
                           "abbreviation WHERE substance_abbrev LIKE %s",
                           ("%" + self.name + "%",))
            abbrevs = cursor.fetchall()

            cursor.close()
            my_db.close()

            if not result:
                cursor.close()
                my_db.close()

                return f"No search results for {self.name}. " \
                       f"Please try again!"
            else:
                similar = [x[0] for x in result]
                similar_abbrevs = [x[0] for x in abbrevs]
                zipped = list(zip(similar_abbrevs, similar))
                result = ""

                for y in zipped:
                    result = result + f"{y[0]} - {y[1]}\n"

                cursor.close()
                my_db.close()

                return result

        except (ValueError, IndexError):
            cursor.close()
            my_db.close()

            return f"No search results for {self.name}. " \
                   f"Please try again!"
