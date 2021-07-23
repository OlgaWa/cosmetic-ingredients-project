from cosing_db.db_utils import CosIng


class IngredientGroup(CosIng):

    def __init__(self, name):
        self.name = name

    def _find_in_db(self):
        pass

    def show_ingredients(self):
        pass
