import sqlite3
from helpers import chooseFromList


# A table handler class
class Table:
    # Takes table name and database name
    def __init__(self, tableName, database):
        self.tableName = tableName
        self.database = database

    # Returns a list with all or just selected columns from a table
    def showTable(self, columns="*"):
        con = sqlite3.connect(self.database)
        cursor = con.cursor()
        cursor.execute(f"SELECT {columns} FROM {self.tableName}")
        table = cursor.fetchall()
        output = []
        for items in table:
            print(*items)
            for item in items:
                output.append(item)
        con.close()
        return output

    # Gets either all or just selected columns associated with an item or choice from similar items
    def getItem(self, name, searchCol, column="*", similar=False):
        con = sqlite3.connect(self.database)
        cursor = con.cursor()
        if similar:
            cursor.execute(
                f"SELECT {column} FROM {self.tableName} WHERE {searchCol} LIKE'%{name}%'"
            )
            row = cursor.fetchall()
        else:
            cursor.execute(
                f"SELECT {column} FROM {self.tableName} WHERE {searchCol} = '{name}'"
            )
            row = cursor.fetchone()
        con.close
        return row

    # Inserts a row to a table taking a dictionary of keys and values as input
    def addRow(self, **values):
        con = sqlite3.connect(self.database)
        cursor = con.cursor()
        keys = ", ".join(values.keys())
        values = str(list(values.values())).strip("[]")
        cursor.execute(f"INSERT INTO {self.tableName} ({keys}) VALUES ({values})")
        con.commit()
        con.close()

    # Changes the value of one or many cells in the table based on a condition
    def changeCell(self, newValue, condition, column):
        con = sqlite3.connect(self.database)
        cursor = con.cursor()
        cursor.execute(
            f"UPDATE {self.tableName} SET {column} = '{newValue}' WHERE {condition}"
        )
        con.commit()
        con.close()

    # Check if a matching or similar item existis in a table
    def isInTable(self, searchCol, searchVal, showColumn="*", similar=False):
        con = sqlite3.connect(self.database)
        cursor = con.cursor()
        if similar:
            cursor.execute(
                f"SELECT {showColumn} FROM {self.tableName} WHERE lower({searchCol}) LIKE '%{searchVal}%'"
            )
            ingredients = cursor.fetchall()
        else:
            cursor.execute(
                f"SELECT {showColumn} FROM {self.tableName} WHERE lower({searchCol}) = '{searchVal}'"
            )
            ingredients = cursor.fetchone()
        con.close()
        if ingredients:
            return True
        else:
            return False



# A class to deal with user's current stock of ingredients
class Stock(Table):
    def __init__(self, table, database):
        super().__init__(table, database)

    # Returns a list of ingredients available, optionally choose an ingredient, or print the recipe, or search for specific ingredient
    def getStock(self, item=False, show=False, get=False):
        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        if get:
            cursor.execute(
                f"SELECT name, stock_amount FROM foods_table WHERE stock_amount > 0"
            )
            results = cursor.fetchall()
            items = []
            names = []
            for result in results:
                items.append(f"{result[1]}g of {result[0]}")
                names.append(result[0])
            choice = chooseFromList(
                items,
                "Go back",
                inputMessage="Show nutrients for ingredient number: ",
                title="\nAvailable stock items\n",
                returnIndex=True,
            )
            names.append("Go back")
            return names[choice]
        if item:
            cursor.execute(
                f"SELECT name, stock_amount FROM foods_table WHERE name LIKE '%{item}%' AND stock_amount > 0 "
            )
            results = cursor.fetchall()
        else:
            cursor.execute(
                f"SELECT name, stock_amount FROM foods_table WHERE stock_amount > 0"
            )
            results = cursor.fetchall()
        con.close()
        if show:
            for i in results:
                print(f"{i[0]}, {i[1]}g")
        return results

        # Get a string containing ingredient's nutritional values

    def getNutrition(self, name):
        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        cursor.execute(
            f"SELECT name, kcal, proteins, fats, carbs stock_amount FROM foods_table WHERE name = '{name}'"
        )
        fname, energy, proteins, fats, carbs = cursor.fetchone()
        con.close()
        return f"100g of {fname} has {energy} calories\n{proteins}g of proteins {carbs}g of carbs and {fats}g of fats"


# A class to handle recipes
class RecipeBook(Table):
    def __init__(self, recipeTable, ingredientTable, database):
        self.ingredientTable = ingredientTable
        super().__init__(recipeTable, database)

    # Lists all the recipes in the database, optionally select one
    def getRecipe(self):
        recipe = chooseFromList(
            self.showTable(columns="name"),
            "Go Back",
            inputMessage="Show ingredients for recipe number: ",
        )
        return recipe

    # Get all ingredients from a recipe, optionally display them
    def getIngredients(self, recipeName, show=False):
        recipeName = recipeName.lower()
        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        cursor.execute(
            f"SELECT f.id, f.name, i.quantity FROM recipes r LEFT JOIN ingredients i ON r.id = i.recipe_id LEFT JOIN foods_table f ON f.id = i.food_id WHERE lower(r.name) = '{recipeName}'"
        )
        results = cursor.fetchall()
        con.close()
        if show:
            print(f"\n  {recipeName} \n")
            for item in results:
                print(f"{item[2]}g of {item[1]}")
        return results
