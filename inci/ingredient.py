import pandas as pd
from inci_db.db_utils import DatabaseConnector


class Ingredient(DatabaseConnector):

    def __init__(self, name):
        self.name = name

    @classmethod
    def create_table(cls, filepath):
        """
        Create a table in the database from csv file
        with all the cosmetic ingredients.
        """
        my_db = super().db_connect()
        cursor = my_db.cursor()

        table_name = cls.__name__.lower()

        data = pd.read_csv(filepath, encoding="utf-8")
        df = pd.DataFrame(data,
                          columns=["INCI_name", "Description", "Function"])
        df = df.astype(object).where(pd.notnull(df), None)

        cursor.execute(f"CREATE TABLE {table_name} "
                       "(ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                       "INCI_name VARCHAR(5000), "
                       "INCI_description VARCHAR(5000), "
                       "INCI_function VARCHAR(500) )")

        for row in df.itertuples():
            sql = f"INSERT INTO " \
                  f"{table_name} (INCI_name, " \
                  f"INCI_description, INCI_function) " \
                  f"VALUES (%s, %s, %s)"
            val = (row.INCI_name, row.Description, row.Function)

            cursor.execute(sql, val)

        my_db.commit()
        cursor.close()
        my_db.close()

    def show_ingredients(self):
        """
        Search for cosmetic ingredients that have
        a name containing searched phrase.
        """
        names = self._db_find_names()

        if not names:
            return f"No search results for {self.name}. " \
                   f"Go to the main page or try searching below!"
        elif len(self.name) < 3:
            return "Type at least 3 characters.\n" \
                   "Go to the main page or try searching below!"
        else:
            result = ""
            for y in names:
                result = result + f"{y[0]}\n"

            return result

    def show_description(self):
        """
        Search for a cosmetic ingredient with
        a given name and for its description.
        """
        try:
            name = self._db_find_one_ingredient()
            desc = self._db_find_desc()[0][0]
            result = f"{name}: \n{desc}"
            return result.split("\n")
        except (ValueError, IndexError):
            return f"It seems we don't have this ingredient " \
                   f"in our database. Try again!"

    def show_function(self):
        """
        Search for a cosmetic ingredient with
        a given name and for its function.
        """
        try:
            func = self._db_find_func()
            result = f"FUNCTION: \n{func}"
            return result.split("\n")
        except (ValueError, IndexError):
            return ""

    def _db_find_one_ingredient(self):
        my_db = super().db_connect()
        cursor = my_db.cursor()

        cursor.execute("SELECT INCI_name FROM "
                       "ingredient WHERE INCI_name=%s",
                       (self.name,))
        ingredient = cursor.fetchall()[0][0]

        cursor.close()
        my_db.close()

        return ingredient

    def _db_find_names(self):
        my_db = super().db_connect()
        cursor = my_db.cursor()

        cursor.execute("SELECT INCI_name FROM "
                       "ingredient WHERE INCI_name LIKE %s ",
                       ("%" + self.name + "%",))
        names = cursor.fetchall()

        cursor.close()
        my_db.close()

        return names

    def _db_find_func(self):
        my_db = super().db_connect()
        cursor = my_db.cursor()

        cursor.execute("SELECT INCI_function FROM "
                       "ingredient WHERE INCI_name=%s",
                       (self.name,))
        func = cursor.fetchall()[0][0]

        cursor.close()
        my_db.close()

        return func

    def _db_find_desc(self):
        my_db = super().db_connect()
        cursor = my_db.cursor()

        cursor.execute("SELECT INCI_description FROM "
                       "ingredient WHERE INCI_name LIKE %s "
                       "or INCI_description LIKE %s",
                       ("%" + self.name + "%", "%" + self.name + "%",))
        desc = cursor.fetchall()

        cursor.close()
        my_db.close()

        return desc
