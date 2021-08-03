from inci_db.db_utils import CosIng


class IngredientGroup(CosIng):

    def __init__(self, name):
        self.name = name

    def show_ingredients(self):
        names = self._db_find_names()
        desc = self._db_find_desc()

        if not names:
            return f"No search results for {self.name}. " \
                   f"Please try again!"
        elif len(self.name) < 3:
            return "Type at least 3 characters."
        else:
            name_list = [x[0] for x in names]
            desc_list = [x[0] for x in desc]
            zipped = list(zip(name_list, desc_list))
            result = ""

            for y in zipped:
                result = result + f"{y[0]} - {y[1]}\n"

            return result

    def _db_find_names(self):
        my_db = super().db_connect()
        cursor = my_db.cursor()

        cursor.execute("SELECT INCI_name FROM "
                       "ingredient WHERE INCI_name LIKE %s "
                       "or INCI_description LIKE %s",
                       ("%" + self.name + "%", "%" + self.name + "%",))
        names = cursor.fetchall()

        cursor.close()
        my_db.close()

        return names

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
