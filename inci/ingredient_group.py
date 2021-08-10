from inci_db.db_utils import DatabaseConnector


class IngredientGroup(DatabaseConnector):

    def __init__(self, name):
        self.name = name

    def show_ingredients(self):
        """
        Search for cosmetic ingredients that have a name
        or a description containing searched phrase.
        """
        names = self._db_find_names()

        if not names:
            return "No search results. Try again!"
        elif len(self.name) < 3:
            return "Type at least 3 characters. Try again!"
        else:
            result = ""
            for y in names:
                result = result + f"{y[0]}\n"

            return result.split("\n")

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
