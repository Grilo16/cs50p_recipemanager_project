import requests
import sqlite3

# A table handler class
class Table():
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
                f"SELECT {column} FROM {self.tableName} WHERE {searchCol} LIKE'%{name}%'")
            row = cursor.fetchall()
        else:
            cursor.execute(
                f"SELECT {column} FROM {self.tableName} WHERE {searchCol} = '{name}'")
            row = cursor.fetchone()
        con.close
        return row

    # Inserts a row to a table taking a dictionary of keys and values as input
    def addRow(self, **values):
        con = sqlite3.connect(self.database)
        cursor = con.cursor()
        keys = ", ".join(values.keys())
        values = str(list(values.values())).strip("[]")
        cursor.execute(
            f"INSERT INTO {self.tableName} ({keys}) VALUES ({values})")
        con.commit()
        con.close()

    # Changes the value of one or many cells in the table based on a condition
    def changeCell(self, newValue, condition, column):
        con = sqlite3.connect(self.database)
        cursor = con.cursor()
        cursor.execute(
            f"UPDATE {self.tableName} SET {column} = '{newValue}' WHERE {condition}")
        con.commit()
        con.close()

    # Check if a matching or similar item existis in a table
    def is_inTable(self, searchCol, searchVal, showColumn="*", similar=False):
        con = sqlite3.connect(self.database)
        cursor = con.cursor()
        if similar:
            cursor.execute(
                f"SELECT {showColumn} FROM {self.tableName} WHERE lower({searchCol}) LIKE '%{searchVal}%'")
            ingredients = cursor.fetchall()
        else:
            cursor.execute(
                f"SELECT {showColumn} FROM {self.tableName} WHERE lower({searchCol}) = '{searchVal}'")
            ingredients = cursor.fetchone()
        con.close()
        if ingredients:
            return True
        else:
            return False

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

# A class to deal with user's current stock of ingredients
class Stock(Table):
    def __init__(self, table, database):
        super().__init__(table, database)

    # Returns a list of ingredients available, optionally choose an ingredient, or print the recipe, or search for specific ingredient
    def getStock(self, item=False, show=False, get=False):
        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        if get:
            cursor.execute(f"SELECT name, stock_amount FROM food_db WHERE stock_amount > 0")
            results = cursor.fetchall()
            items = []
            names = []
            for result in results:
                items.append(f"{result[1]}g of {result[0]}")
                names.append(result[0])
            choice = chooseFromList(items, "Go back", inputMessage="Show nutrients for ingredient number: ", message="\nAvailable stock items\n", noMessage="on", showIndex="on")
            names.append("Go back")
            return names[choice]
        if item:
            cursor.execute(
                f"SELECT name, stock_amount FROM food_db WHERE name LIKE '%{item}%' AND stock_amount > 0 ")
            results = cursor.fetchall()
        else:
            cursor.execute(
                f"SELECT name, stock_amount FROM food_db WHERE stock_amount > 0")
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
        cursor.execute(f"SELECT name, kcal, proteins, fats, carbs stock_amount FROM food_db WHERE name = '{name}'")
        fname, energy, proteins, fats, carbs = cursor.fetchone()
        con.close()
        return f"100g of {fname} has {energy} calories\n{proteins}g of proteins {carbs}g of carbs and {fats}g of fats"

# Define global Table objecs
FOOD_DB = Table("food_db", "database.db")
RECIPES = Table("recipes", "database.db")
INGREDIENTS = Table("ingredients", "database.db")
# Define recipeBook
RECIPEBOOK = RecipeBook("recipes", "ingredients", "database.db")
# Define ingredient stock
STOCK = Stock("food_db", "database.db")

def main():

    # Check if database exists, if not create it
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master")
    result = cursor.fetchall()
    if not result == [('food_db',), ('sqlite_autoindex_food_db_1',), ('recipes',), ('sqlite_autoindex_recipes_1',), ('ingredients',), ('sqlite_autoindex_ingredients_1',)]:
        # Create food_db table
        cursor.execute("CREATE TABLE food_db(id INTEGER NOT NULL PRIMARY KEY, name TEXT NOT NULL, kcal FLOAT, proteins FLOAT, fats FLOAT, carbs, quantity FLOAT DEFAULT 100, stock_amount INT DEFAULT 0, UNIQUE(name))")
        # Create recipes table
        cursor.execute("CREATE TABLE recipes(id INTEGER NOT NULL PRIMARY KEY, name TEXT NOT NULL, UNIQUE(name))")
        # Create ingredients table
        cursor.execute("CREATE TABLE ingredients(recipe_id INTEGER NOT NULL, food_id INTEGER NOT NULL, quantity INTEGER NOT NULL, UNIQUE (recipe_id, food_id))")
        con.commit()
    con.close()

    # Present the user with program's functionalities to choose from
    choices = ["Show all recipes", "Show ingredients in stock", "Cook from available recipes",
               "Create a recipe", "Add to food stock", "Add ingredient to database", "Close Program"]
    while True:
        choice = chooseFromList(choices)

        if choice == "Show all recipes":
            while True:
                recipe = RECIPEBOOK.showRecipes(get=True)
                if recipe != "Go Back":
                    RECIPEBOOK.getIngredients(recipe, show=True)
                    pressToContinue()
                    continue
                else:
                    break
            continue

        elif choice == "Show ingredients in stock":
            while True:
                ingredient = STOCK.getStock(get=True)
                if ingredient != "Go back":
                    print(STOCK.getNutrition(ingredient))
                    pressToContinue()
                    continue
                else:
                    break
            continue
        elif choice == "Cook from available recipes":
            cookRecipe()
            pressToContinue()
            continue
        elif choice == "Create a recipe":
            recipe = create_recipeDict()
            if recipe == "cancel":
                continue
            while True:
                name = recipe["name"]
                ingredients = recipe["ingredients"]
                ingredientsList = list(ingredients.items())
                print(f"\nRecipe: {name}")
                showList = []
                for ingredient in ingredientsList:
                    fingredients = f"{ingredient[1]}g of {ingredient[0]}"
                    showList.append(fingredients)

                if len(showList) == 0:
                    do = chooseFromList(["Add ingredient to recipe", "Cancel adding recipe"], showIndex="on", message="Your recipe has no ingredients please choose an option below", noMessage="on")
                    print()
                    if do == 0:
                        print("Type cancel to stop inputing recipe")
                        print("--Adding extra ingredient--")
                        newName = getUserInput("Ingredient name: ").lower()
                        if newName == "cancel":
                            pressToContinue(message="Your recipe will not be stored in the database, press enter to continue")
                            break
                        newAmount = getUserInput("Ingredient amount: ", makeint="on")
                        ingredients.update({newName: newAmount})
                        continue
                    else:
                        break

                checkRecipe = chooseFromList(showList, "Add extra ingredient to recipe", "All ingredients are correct, I'd like to input recipe into the database", "Cancel inputing recipe", noMessage="on", message="change any ingredients?", showIndex="on")

                if checkRecipe + 1 == len(showList):
                    pressToContinue("Your recipe will not be input into the database, press enter to continue")
                    break
                elif checkRecipe + 1 == len(showList) -1:
                    print("Adding recipe to database")
                    storeRecipeDict(recipe)
                    pressToContinue()
                    break

                elif checkRecipe + 1 == len(showList) - 2:
                    print("--Adding extra ingredient--")
                    newName = getUserInput("Ingredient name: ")
                    newAmount = getUserInput(
                        "Ingredient amount: ", makeint="on")
                    ingredients.update({newName: newAmount})
                    continue
                else:
                    print(
                        f"\nYou are changing the entry for: \n{showList[checkRecipe]}\n\n-- New entry --")
                    iName = ingredientsList[checkRecipe][0]
                    recipe["ingredients"].pop(iName)
                    newName = getUserInput(
                        "Ingredient name(del to delete ingredient): ")
                    if newName == "del":
                        continue
                    else:
                        newAmount = getUserInput(
                            "Ingredient amount: ", makeint="on")
                        ingredients.update({newName: newAmount})
                        continue
            continue

        elif choice == "Add to food stock":
            while True:
                print("Type 'cancel' to stop adding ingredient")
                ingredient = getUserInput("Ingredient name: ").lower()
                if ingredient == "cancel":
                    break
                amount = getUserInput("Amount in grams: ", makeint="on")
                add_toStock(ingredient, amount)
                addmore = chooseFromList(["Continue adding ingredients", "Go back"], showIndex="on", noMessage="on")
                if addmore == 0:
                    continue
                else:
                    break
            continue
        elif choice == "Add ingredient to database":
            print("Type 'cancel' to go back")
            ingredient = getUserInput("Ingredient name: ")
            add_NewIngredient(ingredient)
            pressToContinue()
            continue
        elif choice == "Close Program":
            break

# Presents the user with available recipes based on ingredient stock and subtract used ingredients from stock, as well as presenting the recipe to the user
def cookRecipe():

    available_recipes = recipesAvailable()
    if len(available_recipes) == 0:
        print("Currently You do not have enough ingredients to cook any recipe")
        return
    recipe_name = chooseFromList(available_recipes, "Go back",  noMessage="on", message="\nChoose recipe to cook\n")
    if recipe_name == "Go back":
        return
    # Get dictionary of ingredients : amounts from recipe
    recipe = RECIPEBOOK.getIngredients(recipe_name)
    # Iterate over every ingredient
    for Ingredient in recipe:
        ingredient = Ingredient[1]
        amount = Ingredient[2]
        newStock = STOCK.getStock(item=ingredient)[0][1] - amount
        # Update database with new stock amount
        FOOD_DB.changeCell(newStock, f"name = '{ingredient}'", "stock_amount")

    # Present the user with the ingredients that were used
    print(f"\n\nyou cooked: {recipe_name}")
    print("You have used: \n")
    for ingredient in recipe:
        print(f"{ingredient[2]}g of {ingredient[1]}")
    print()

    return


# Add a food ingredient and its quantity to the stock of ingredients
def add_toStock(ingredient, amount):

    # Check if ingredient in database
    if similar := FOOD_DB.getItem(ingredient, "name", column="name", similar=True):
        similar = [i[0] for i in similar]
        ingredient = chooseFromList(similar, "search online")
        if ingredient == "search online":
            ingredient = add_NewIngredient(
                getUserInput("Search for new ingredient: "))
    else:
        print(f"\nItem: {ingredient}, is not in the database \nplease add it to the database")
        print("\n-- Adding new ingredient --\nType 'cancel' to go back \n")
        ingredient = add_NewIngredient(getUserInput("Search for new ingredient: "))
        if not ingredient:
            return

    # Get current ingredient's quantity in stock from the database and update it
    currentStock = FOOD_DB.getItem(ingredient, "name", column="stock_amount")[0]
    newStock = currentStock + amount
    FOOD_DB.changeCell(newStock, f"name = '{ingredient}'", "stock_amount")

    print(f"\nSuccessfully added {amount}g to the stock of {ingredient}\n")


# Prompts the user for recipe information and format it correctly for storage
def create_recipeDict():

    recipe = {}

    # Prompt user for a recipe name
    print("\nPlease name your recipe: \nType 'cancel' to stop inputing recipe\n")
    recipeName = getUserInput("Recipe name: ")
    if (cancel := recipeName.lower()) == "cancel":
        return cancel

    # Initialize keys and values for the recipe dictionary
    recipe["name"] = recipeName
    recipe["ingredients"] = {}

    # FOH EVAAH
    while True:
        # Request user for a ingredient, if he types done exit the loop
        print("\nPlease name an ingredient \nType 'done' to stop inputing ingredients\n")
        if (ingredient := getUserInput("Ingredient: ").lower()) == "done":
            break
        # Ask user the amount of ingredient the recipe requires and append it to the recipe
        amount = getUserInput("amount: ", makeint="on")
        recipe["ingredients"][ingredient] = amount

    return recipe


# Receives a recipe correctly formated and adds it to the database
def storeRecipeDict(recipe):

    # Store recipe name and ingredient in variables
    recipe_name = recipe["name"]
    ingredients = recipe["ingredients"]

    # Validade ingredients and get their ids from database
    ids = []
    for ingredient in ingredients.items():
        ingamount = {}
        ingamount["quantity"] = ingredient[1]
        # If ingredient is in database
        if FOOD_DB.is_inTable("name", ingredient[0]):
            ingamount["food_id"] = FOOD_DB.getItem(
                ingredient[0], "name", column="id")[0]
        # Check if there are similar ingredients in the database
        elif similar := FOOD_DB.getItem(ingredient[0], "name", similar=True, column="name"):
            similar = [i[0] for i in similar]
            ingredient = chooseFromList(similar, "Search online")
            if ingredient == "Search online":
                print("-- Search for new ingredient --")
                ingredient = add_NewIngredient(getUserInput("ingredient name: "))
            ingamount["food_id"] = FOOD_DB.getItem(
                ingredient, "name", column="id")[0]
        # If ingredient not in the database Add new ingredient.
        else:
            print(f"\n{ingredient[0]} not in the database\n")
            ingredient = add_NewIngredient(
                getUserInput("Add new ingredient to database: "))
            ingamount["food_id"] = FOOD_DB.getItem(
                ingredient, "name", column="id")[0]

        # Check for duplicate ingredients
        if not ingamount["food_id"] in ids:
            ids.append(ingamount)
        else:
            print(
                "Duplicate ingredient detected, Your recipe was not stored in the database")
            pressToContinue
            return

    # Check if recipe is already in the database
    while True:
        # If it is ask user to rename recipe
        if RECIPES.is_inTable("name", recipe_name):
            print("\nThis recipe name is already in the database\n")
            print("please rename your recipe\n")
            recipe_name = getUserInput("New recipe name: ").lower()
            continue
        break

    # store recipe name in the database and get its unique id
    RECIPES.addRow(**{"name": recipe_name})
    recipeId = RECIPES.getItem(recipe_name, "name")[0]
    # Store validated ingredient ids under the new recipe's id
    for id in ids:
        id["recipe_id"] = recipeId
        INGREDIENTS.addRow(**id)

    print(f"\nSuccessfully added {recipe_name} to the database\n")


def add_NewIngredient(ing_name):

    # Search until satisfied with result
    while True:
        if ing_name == "cancel":
            return
        search = requests.get(
            f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key=MzwHdrUMWKONRuqAyYr654ER0pQkYT9mrXfkXY4D&query={ing_name}&dataType=Foundation,SR%20Legacy&pageSize=25&pageNumber=1&sortBy=dataType.keyword").json()

        # Search resulted in 0 options query the user to search using different terms
        if search["totalHits"] == 0:
            print("no results from your query")
            print("type 'cancel' to go back or")
            ing_name = getUserInput("Search using a different term: ")
            continue
        # Search with positive results
        else:
            # Present user with results by name and ask for a choice
            searchResults = []
            for ingredients in search["foods"]:
                searchResult = ingredients["description"]
                searchResults.append(searchResult)
            user_choice = chooseFromList(
                searchResults, "cancel or search again?", showIndex="on")

            # If user not satisfied with search reasults search for something else
            if user_choice == len(searchResults)-1:
                print("type 'cancel' to go back")
                ing_name = getUserInput("Search using a different term: ").lower()
                if ing_name == "cancel":
                    return
                else:
                    continue
            else:
                break

    # Show users choice
    print(
        f"\n      You chose: {search['foods'][user_choice]['description']}\n")

    # Get selected food ingredients from the website
    nutrients = search["foods"][user_choice]["foodNutrients"]

    output = {}
    # Ask user to Name ingredient and input it lowercase
    while True:
        output["name"] = getUserInput(
            "How would you like to name your ingredient: ").lower()
        # Check if chosen name is in the database already
        if FOOD_DB.is_inTable("name", output["name"]):
            print("\nName already on database, Please use a different name")
            print(f"\n      You chose: {search['foods'][user_choice]['description']}\n")
            continue
        break

    # Define nutrients to search for by their nutrient number
    nutrientDict = {"203": "proteins",
                    "204": "fats", "205": "carbs", "208": "kcal"}

    # Set default nutrient amounts to 0
    for item in nutrientDict.values():
        output[item] = 0

    # Get information on nutrients in nutrientDict
    for nutrient in nutrients:
        if nutrient["nutrientNumber"] in nutrientDict.keys():
            output[nutrientDict[nutrient["nutrientNumber"]]] = nutrient["value"]

    # Add to database and notify user operation was successfull
    FOOD_DB.addRow(**output)
    print(f"\n       Successfully added item to database: {output['name']}\n")

    return output["name"]


# A code pauser to allow the user to read the output before continuing
def pressToContinue(message="Press enter to continue"):
    try:
        input(message)
    except (KeyboardInterrupt, EOFError):
        exit("")
    return

# Gets users input and validates it as a string or optionally int
def getUserInput(question, makeint="off"):
    while True:
        try:
            name = input(f"{question}").lower().strip()
        except (EOFError, KeyboardInterrupt):
            exit("")
        if makeint=="on":
            try:
                name = int(name)
            except ValueError:
                print("Please input an integer")
                continue
            if name <= 0:
                print("Please input a positive integer")
                continue
        else:
            if len(name) == 0:
                print("Names cannot be blank")
                continue
        break
    return name


# Presents a list and returns the value the user chose, optionally return index, add items, change messages
def chooseFromList(list, *extra, showIndex="off", noChoice="off", message=False, noMessage="off", inputMessage = "choose an option: "):
    if message:
        print(message)
    if noMessage == "off":
        print("\nChoose an option\n")
    if extra:
        for i in extra:
            list.append(i)
    index = 0
    for item in list:
        index += 1
        print(index, item)
    print()
    if noChoice == "on":
        return
    # Get users choice and validate it chooses an item from list
    while True:
        try:
            choice = int(input(f"{inputMessage}"))-1
        except ValueError:
            print("Please input an integer")
            continue
        except (KeyboardInterrupt, EOFError):
            exit("")
        else:
            if choice < 0 or choice > index-1:
                print("please input a value within the selection range")
                continue
            else:
                break
    if showIndex == "on":
        return choice
    return list[choice]


# Returns a list with all available recipes based on ingredients
def recipesAvailable():

    con = sqlite3.connect("database.db")
    cursor = con.cursor()

    # Query database only for recipes where all ingredient stock quantities are higher than recipe requirements
    cursor.execute("SELECT r.name FROM food_db fdb LEFT JOIN ingredients i ON fdb.id = i.food_id LEFT JOIN recipes r ON r.id = i.recipe_id GROUP BY recipe_id HAVING min(fdb.stock_amount) >= i.quantity ORDER BY i.recipe_id")

    results = [ingredient[0] for ingredient in cursor.fetchall()]

    con.close()
    return results


if __name__ == "__main__":
    main()
