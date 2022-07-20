
# A class to handle recipes
class RecipeBook(Table):
    def __init__(self, recipeTable, ingredientTable, database):
        self.ingredientTable = ingredientTable
        super().__init__(recipeTable, database)

    # Lists all the recipes in the database, optionally select one
    def showRecipes(self, get=False):
        if get:
            recipe = chooseFromList(self.showTable(
                columns="name"), "Go Back", inputMessage="Show ingredients for recipe number: ")
            return recipe
        self.showTable()

    # Get all ingredients from a recipe, optionally display them
    def getIngredients(self, recipeName, show=False):
        recipeName = recipeName.lower()
        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        cursor.execute(
            f"SELECT f.id, f.name, i.quantity FROM recipes r LEFT JOIN ingredients i ON r.id = i.recipe_id LEFT JOIN food_db f ON f.id = i.food_id WHERE lower(r.name) = '{recipeName}'")
        results = cursor.fetchall()
        con.close()
        if show:
            print(f"\n  {recipeName} \n")
            for item in results:
                print(f"{item[2]}g of {item[1]}")
        return results
