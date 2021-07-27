import pandas as pd
from cosing_db.db_utils import CosIng


class INCIFunction(CosIng):

    def __init__(self, name):
        self.name = name

    @classmethod
    def create_table(cls, filepath):

        my_db = super().db_connect()
        cursor = my_db.cursor()

        table_name = cls.__name__.lower()

        data = pd.read_csv(filepath, encoding="utf-8")
        df = pd.DataFrame(data, columns=["Name", "Description"])
        df = df.astype(object).where(pd.notnull(df), None)

        cursor.execute(f"CREATE TABLE {table_name} "
                       "(ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                       "name VARCHAR(50), description VARCHAR(1000) )")

        for row in df.itertuples():
            sql = f"INSERT INTO " \
                  f"{table_name} (name, description) " \
                  f"VALUES (%s, %s)"
            val = (row.Name, row.Description)

            cursor.execute(sql, val)

        my_db.commit()
        cursor.close()
        my_db.close()

    def show_info(self):
        inci_names = self._db_find_name()
        inci_func = self._db_find_func()

        if not inci_func:
            return f"It seems we don't have function '{self.name}' " \
                   f"in our database. Please try again!"
        else:
            all_func = [x[0] for x in inci_func]
            all_names = [x[0] for x in inci_names]
            zipped = list(zip(all_names, all_func))
            result = ""

            for y in zipped:
                result = result + f"{y[0]}: {y[1]}\n"

            return result

    def _db_find_name(self):
        my_db = super().db_connect()
        cursor = my_db.cursor()

        cursor.execute("SELECT name FROM "
                       "incifunction WHERE name LIKE %s",
                       ("%" + self.name + "%",))
        inci_names = cursor.fetchall()

        cursor.close()
        my_db.close()

        return inci_names

    def _db_find_func(self):
        my_db = super().db_connect()
        cursor = my_db.cursor()

        cursor.execute("SELECT description FROM "
                       "incifunction WHERE name LIKE %s",
                       ("%" + self.name + "%",))
        inci_func = cursor.fetchall()

        cursor.close()
        my_db.close()

        return inci_func
