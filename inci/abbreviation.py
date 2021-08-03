import pandas as pd
from inci_db.db_utils import CosIng


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

    def show_ingredient(self):
        try:
            ingredient = self._db_find_ingredient()
            return ingredient
        except (ValueError, IndexError):
            return f"It seems we don't have {self.name} " \
                   f"in our database. Please try again!"

    def show_abbrev_in(self):
        abbrevs = self._db_find_abbrevs()
        subs = self._db_find_substances()

        if not subs or not self.name:
            return f"No search results for {self.name}. " \
                   f"Please try again!"
        else:
            similar_subs = [x[0] for x in subs]
            similar_abbrevs = [x[0] for x in abbrevs]
            zipped = list(zip(similar_abbrevs, similar_subs))
            result = ""

            for y in zipped:
                result = result + f"{y[0]} - {y[1]}\n"

            return result

    def _db_find_ingredient(self):
        my_db = super().db_connect()
        cursor = my_db.cursor()

        cursor.execute("SELECT chemical_substance FROM "
                       "abbreviation WHERE substance_abbrev=%s",
                       (self.name,))
        ingredient = cursor.fetchall()[0][0]

        cursor.close()
        my_db.close()

        return ingredient

    def _db_find_abbrevs(self):
        my_db = super().db_connect()
        cursor = my_db.cursor()

        cursor.execute("SELECT substance_abbrev FROM "
                       "abbreviation WHERE substance_abbrev LIKE %s",
                       ("%" + self.name + "%",))
        abbrevs = cursor.fetchall()

        cursor.close()
        my_db.close()

        return abbrevs

    def _db_find_substances(self):
        my_db = super().db_connect()
        cursor = my_db.cursor()

        cursor.execute("SELECT chemical_substance FROM "
                       "abbreviation WHERE substance_abbrev LIKE %s",
                       ("%" + self.name + "%",))
        subs = cursor.fetchall()

        cursor.close()
        my_db.close()

        return subs
