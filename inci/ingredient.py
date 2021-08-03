import pandas as pd
from inci_db.db_utils import CosIng


class Ingredient(CosIng):

    def __init__(self, name):
        self.name = name

    @classmethod
    def create_table(cls, filepath):

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
        names = self._db_find_names()

        if not names:
            return f"No search results for {self.name}. " \
                   f"Please try again!"
        elif len(self.name) < 3:
            return "Type at least 3 characters."
        else:
            result = ""
            for y in names:
                result = result + f"{y[0]}\n"

            return result

    def show_description(self):
        try:
            name = self._db_find_one_ingredient()
            desc = self._db_find_desc()[0][0]
            result = f"{name}: {desc}"
            return result
        except (ValueError, IndexError):
            return f"It seems we don't have {self.name} " \
                   f"in our database. Please try again!"

    def show_function(self):
        try:
            name = self._db_find_one_ingredient()
            func = self._db_find_func()
            result = f"{name} - function: {func}"
            return result
        except (ValueError, IndexError):
            return f"It seems we don't have {self.name} " \
                   f"in our database. Please try again!"

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
