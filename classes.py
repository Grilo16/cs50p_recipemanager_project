import sqlite3
from helpers import chooseFromList


# A table handler class
class Table:
    # Takes table name and database name
    def __init__(self, tableName, dbFileName):
        self.tableName = tableName
        self.dbFileName = dbFileName
        with sqlite3.connect(self.dbFileName) as dataBase:
            self.dataBase = dataBase
            self.cursor = dataBase.cursor()
        
    # Returns a list with all or just selected columns from a table
    def showTable(self, columns="*"):        
        self.cursor.execute(f"SELECT {columns} FROM {self.tableName}")
        table = self.cursor.fetchall()
        output = []
        for items in table:
            print(*items)
            for item in items:
                output.append(item)
        return output

    # Gets either all or just selected columns associated with an item or choice from similar items
    def getItem(self, name, searchCol, column="*", similar=False):
        if similar:
            self.cursor.execute(
                f"SELECT {column} FROM {self.tableName} WHERE {searchCol} LIKE'%{name}%'"
            )
            row = self.cursor.fetchall()
        else:
            self.cursor.execute(
                f"SELECT {column} FROM {self.tableName} WHERE {searchCol} = '{name}'"
            )
            row = self.cursor.fetchone()
        return row

    # Inserts a row to a table taking a dictionary of keys and values as input
    def addRow(self, **values):
        keys = ", ".join(values.keys())
        values = str(list(values.values())).strip("[]")
        self.cursor.execute(f"INSERT INTO {self.tableName} ({keys}) VALUES ({values})")
        self.dataBase.commit()
        

    # Changes the value of one or many cells in the table based on a condition
    def changeCell(self, newValue, condition, column):
        self.cursor.execute(
            f"UPDATE {self.tableName} SET {column} = '{newValue}' WHERE {condition}"
        )
        self.dataBase.commit()

    # Check if a matching or similar item existis in a table
    def isInTable(self, searchCol, searchVal, showColumn="*", similar=False):
        if similar:
            self.cursor.execute(
                f"SELECT {showColumn} FROM {self.tableName} WHERE lower({searchCol}) LIKE '%{searchVal}%'"
            )
            ingredients = self.cursor.fetchall()
        else:
            self.cursor.execute(
                f"SELECT {showColumn} FROM {self.tableName} WHERE lower({searchCol}) = '{searchVal}'"
            )
            ingredients = self.cursor.fetchone()
        if ingredients:
            return True
        else:
            return False



# A class to deal with user's current stock of ingredients
class Stock(Table):
    def __init__(self, table, dbFileName):
        super().__init__(table, dbFileName)

    # Returns a list of ingredients available, optionally choose an ingredient, or print the recipe, or search for specific ingredient
    def getStock(self, item=False, show=False, get=False):
        if get:
            self.cursor.execute(
                f"SELECT name, stock_amount FROM foods_table WHERE stock_amount > 0"
            )
            results = self.cursor.fetchall()
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
            self.cursor.execute(
                f"SELECT name, stock_amount FROM foods_table WHERE name LIKE '%{item}%' AND stock_amount > 0 "
            )
            results = self.cursor.fetchall()
        else:
            self.cursor.execute(
                f"SELECT name, stock_amount FROM foods_table WHERE stock_amount > 0"
            )
            results = self.cursor.fetchall()
        if show:
            for i in results:
                print(f"{i[0]}, {i[1]}g")
        return results

        # Get a string containing ingredient's nutritional values

    def getNutrition(self, name):
        self.cursor.execute(
            f"SELECT name, kcal, proteins, fats, carbs stock_amount FROM foods_table WHERE name = '{name}'"
        )
        fname, energy, proteins, fats, carbs = self.cursor.fetchone()
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
        self.cursor.execute(
            f"SELECT f.id, f.name, i.quantity FROM recipes r LEFT JOIN ingredients i ON r.id = i.recipe_id LEFT JOIN foods_table f ON f.id = i.food_id WHERE lower(r.name) = '{recipeName}'"
        )
        results = self.cursor.fetchall()
        if show:
            print(f"\n  {recipeName} \n")
            for item in results:
                print(f"{item[2]}g of {item[1]}")
        return results
