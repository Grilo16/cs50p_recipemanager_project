from classes import Table, RecipeBook, Stock
from helpers import chooseFromList, getUserInput, pressToContinue, recipesAvailable

import requests
import sqlite3


    
# Define global Table objecs
FOOD_TABLE = Table("foods_table", "database.db")
RECIPES = Table("recipes", "database.db")
INGREDIENTS = Table("ingredients", "database.db")

# Define recipeBook
RECIPEBOOK = RecipeBook("recipes", "ingredients", "database.db")

# Define ingredient stock
STOCK = Stock("foods_table", "database.db")


def main():

    ensureTables()
    showUi()
    
def showUi():
    
    # Present the user with program's functionalities to choose from
    choices = [
        "Show all recipes",
        "Show ingredients in stock",
        "Cook from available recipes",
        "Create a recipe",
        "Add to food stock",
        "Add ingredient to database",
        "Close Program",
    ]
    while True:
        choice = chooseFromList(choices)

        if choice == "Show all recipes":
            while True:
                recipe = RECIPEBOOK.getRecipe()
                if recipe != "Go Back":
                    RECIPEBOOK.getIngredients(recipe, show=True)
                    pressToContinue()
                    continue
                else:
                    break
            continue

        elif choice == "Show ingredients in stock":
            while True:
                formatedStock = []
                stock = STOCK.getStock(all=True)
                for item in stock:
                    formatedStock.append(f"{item[1]}g of {item[0]}")

                ingredient = chooseFromList(formatedStock, "Go back", title="\nItems in stock\nChoose an item to show nutritional contents\n", inputMessage="Select an option: ", returnIndex=True)    

                if ingredient != len(formatedStock) - 1:
                    print(STOCK.getNutrition(stock[ingredient][0]))
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
            recipe = createRecipeDict()
            if recipe:
                recipe = verifyRecipe(recipe)
                if recipe:
                    storeRecipeDict(recipe)
                    pressToContinue()
            else:
                continue

        elif choice == "Add to food stock":
            while True:
                print("Type 'cancel' to stop adding ingredient")
                ingredient = getUserInput("Ingredient name: ").lower()
                if ingredient == "cancel":
                    break
                amount = getUserInput("Amount in grams: ", makeInt=True)
                addToStock(ingredient, amount)
                addmore = chooseFromList(
                    ["Continue adding ingredients", "Go back"],
                    returnIndex=True,
                    noTitle=True,
                )
                if addmore == 0:
                    continue
                else:
                    break
            continue
        elif choice == "Add ingredient to database":
            print("Type 'cancel' to go back")
            ingredient = getUserInput("Ingredient name: ")
            addNewIngredient(ingredient)
            pressToContinue()
            continue
        elif choice == "Close Program":
            break

def ensureTables(dataBase="database.db"):
    # Check if database exists, if not create it
    con = sqlite3.connect(dataBase)
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master")
    result = cursor.fetchall()
    if not result == [
        ("foods_table",),
        ("sqlite_autoindex_foods_table_1",),
        ("recipes",),
        ("sqlite_autoindex_recipes_1",),
        ("ingredients",),
        ("sqlite_autoindex_ingredients_1",),
    ]:

        # Create foods_table table
        cursor.execute(
            "CREATE TABLE foods_table(id INTEGER NOT NULL PRIMARY KEY, name TEXT NOT NULL, kcal FLOAT, proteins FLOAT, fats FLOAT, carbs, quantity FLOAT DEFAULT 100, stock_amount INT DEFAULT 0, UNIQUE(name))"
        )

        # Create recipes table
        cursor.execute(
            "CREATE TABLE recipes(id INTEGER NOT NULL PRIMARY KEY, name TEXT NOT NULL, UNIQUE(name))"
        )

        # Create ingredients table
        cursor.execute(
            "CREATE TABLE ingredients(recipe_id INTEGER NOT NULL, food_id INTEGER NOT NULL, quantity INTEGER NOT NULL, UNIQUE (recipe_id, food_id))"
        )
        con.commit()
    con.close()



def verifyRecipe(recipe):

    # Display recipe to the user
    while True:
        name = recipe["name"]
        ingredients = recipe["ingredients"]
        ingredientsList = list(ingredients.items())
        print(f"\nRecipe: {name}")
        showList = []
        for ingredient in ingredientsList:
            fingredients = f"{ingredient[1]}g of {ingredient[0]}"
            showList.append(fingredients)

        # Check recipe has at least 1 ingredient
        if len(showList) == 0:
            do = chooseFromList(
                ["Add ingredient to recipe", "Cancel adding recipe"],
                returnIndex=True,
                title="Your recipe has no ingredients please choose an option below",
            )
            print()
            if do == 0:
                print("Type cancel to stop inputing recipe")
                print("--Adding extra ingredient--")
                newName = getUserInput("Ingredient name: ").lower()
                if newName == "cancel":
                    pressToContinue(
                        message="Your recipe will not be stored in the database, press enter to continue"
                    )
                    break
                newAmount = getUserInput("Ingredient amount: ", makeInt=True)
                ingredients.update({newName: newAmount})
                continue
            else:
                break

        checkRecipe = chooseFromList(
            showList,
            "Add extra ingredient to recipe",
            "All ingredients are correct, I'd like to input recipe into the database",
            "Cancel inputing recipe",
            title="change any ingredients?",
            returnIndex=True,
        )

        # If user chose to cancel recipe input
        if checkRecipe + 1 == len(showList):
            pressToContinue(
                "Your recipe input has been cancelled, press enter to continue"
            )
            return False

        # If recipe is deemed valid
        elif checkRecipe + 1 == len(showList) - 1:
            validRecipe = {"name": name, "ingredients": ingredients}
            print("Your recipe has been validated")
            return validRecipe

        # If user wants to add extra ingredients
        elif checkRecipe + 1 == len(showList) - 2:
            print("--Adding extra ingredient--")
            newName = getUserInput("Ingredient name: ")
            newAmount = getUserInput("Ingredient amount: ", makeInt=True)
            ingredients.update({newName: newAmount})
            continue

        # If user selected an ingredient
        else:
            print(
                f"\nYou are changing the entry for: \n{showList[checkRecipe]}\n\n-- New entry --"
            )
            iName = ingredientsList[checkRecipe][0]
            recipe["ingredients"].pop(iName)
            newName = getUserInput("Ingredient name(del to delete ingredient): ")
            if newName == "del":
                continue
            else:
                newAmount = getUserInput("Ingredient amount: ", makeInt=True)
                ingredients.update({newName: newAmount})
                continue


# Presents the user with available recipes based on ingredient stock and subtract used ingredients from stock, as well as presenting the recipe to the user
def cookRecipe():

    availableRecipes = recipesAvailable()
    if len(availableRecipes) == 0:
        print("Currently You do not have enough ingredients to cook any recipe")
        return
    recipeName = chooseFromList(
        availableRecipes, "Go back", title="\nChoose recipe to cook\n"
    )
    if recipeName == "Go back":
        return

    # Get dictionary of ingredients : amounts from recipe
    recipe = RECIPEBOOK.getIngredients(recipeName)

    # Iterate over every ingredient changing the stock in the database
    for Ingredient in recipe:
        ingredient, amount = Ingredient[1::]
        STOCK.useFromStock(ingredient, amount)

    # Present the user with the ingredients that were used
    print(f"\n\nyou cooked: {recipeName}\nYou have used: \n")
    for ingredient in recipe:
        print(f"{ingredient[2]}g of {ingredient[1]}")
    print()

    return


# Add a food ingredient and its quantity to the stock of ingredients
def addToStock(ingredient, amount):

    # Check if ingredient in database
    if similar := FOOD_TABLE.getItem(ingredient, "name", column="name", similar=True):
        similar = [i[0] for i in similar]
        ingredient = chooseFromList(similar, "search online")
        if ingredient == "search online":
            ingredient = addNewIngredient(getUserInput("Search for new ingredient: "))
    else:
        searchOption = chooseFromList([f"Search for {ingredient} online", "Search using a different term", "cancel adding ingredients"], returnIndex=True, title=f"\nItem: {ingredient}, is not in the database \n")
        if searchOption == 0:
            ingredient = addNewIngredient(ingredient)
        elif searchOption == 1:
            ingredient = addNewIngredient(getUserInput("What food would you like to search for? "))
        elif searchOption == 2:
            return
        if not ingredient:
            return

    STOCK.addToStock(ingredient, amount)
    
    print(f"\nSuccessfully added {amount}g to the stock of {ingredient}\n")


# Prompts the user for recipe information and format it correctly for storage
def createRecipeDict():

    recipe = {}

    # Prompt user for a recipe name
    print("\nPlease name your recipe: \nType 'cancel' to stop inputing recipe\n")
    recipeName = getUserInput("Recipe name: ")
    if recipeName.lower() == "cancel":
        return False

    # Initialize keys and values for the recipe dictionary
    recipe["name"] = recipeName
    recipe["ingredients"] = {}

    # FOH EVAAH
    while True:

        # Request user for a ingredient, if he types done exit the loop
        print(
            "\nPlease name an ingredient \nType 'done' to stop inputing ingredients\n"
        )
        if (ingredient := getUserInput("Ingredient: ").lower()) == "done":
            break

        # Ask user the amount of ingredient the recipe requires and append it to the recipe
        amount = getUserInput("amount: ", makeInt=True)
        recipe["ingredients"][ingredient] = amount

    return recipe


# Receives a recipe correctly formated and adds it to the database
def storeRecipeDict(recipe):

    # Store recipe name and ingredient in variables
    recipeName = recipe["name"]
    ingredients = recipe["ingredients"]

    # Validade ingredients and get their ids from database
    ids = []
    for ingredient in ingredients.items():
        ingamount = {}
        ingamount["quantity"] = ingredient[1]

        # If ingredient is in database
        if FOOD_TABLE.isInTable("name", ingredient[0]):
            ingamount["food_id"] = FOOD_TABLE.getItem(
                ingredient[0], "name", column="id"
            )[0]

        # Check if there are similar ingredients in the database
        elif similar := FOOD_TABLE.getItem(
            ingredient[0], "name", similar=True, column="name"
        ):
            similar = [i[0] for i in similar]
            ingredient = chooseFromList(similar, "Search online")
            if ingredient == "Search online":
                print("-- Search for new ingredient --")
                ingredient = addNewIngredient(getUserInput("ingredient name: "))
            ingamount["food_id"] = FOOD_TABLE.getItem(ingredient, "name", column="id")[
                0
            ]

        # If ingredient not in the database Add new ingredient.
        else:
            print(f"\n{ingredient[0]} not in the database\n")
            ingredient = addNewIngredient(
                getUserInput("Add new ingredient to database: ")
            )
            ingamount["food_id"] = FOOD_TABLE.getItem(ingredient, "name", column="id")[
                0
            ]

        # Check for duplicate ingredients
        if not ingamount["food_id"] in ids:
            ids.append(ingamount)
        else:
            print(
                "Duplicate ingredient detected, Your recipe was not stored in the database"
            )
            pressToContinue
            return

    # Check if recipe is already in the database
    while True:

        # If it is ask user to rename recipe
        if RECIPES.isInTable("name", recipeName):
            print("\nThis recipe name is already in the database\n")
            print("please rename your recipe\n")
            recipeName = getUserInput("New recipe name: ").lower()
            continue
        break

    # store recipe name in the database and get its unique id
    RECIPES.addRow(**{"name": recipeName})
    recipeId = RECIPES.getItem(recipeName, "name")[0]

    # Store validated ingredient ids under the new recipe's id
    for id in ids:
        id["recipe_id"] = recipeId
        INGREDIENTS.addRow(**id)

    print(f"\nSuccessfully added {recipeName} to the database\n")


def addNewIngredient(ingName):

    # Search until satisfied with result
    while True:
        if ingName == "cancel":
            return
        search = requests.get(
            f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key=MzwHdrUMWKONRuqAyYr654ER0pQkYT9mrXfkXY4D&query={ingName}&dataType=Foundation,SR%20Legacy&pageSize=25&pageNumber=1&sortBy=dataType.keyword"
        ).json()

        # Search resulted in 0 options query the user to search using different terms
        if search["totalHits"] == 0:
            print("no results from your query\ntype 'cancel' to go back or")
            ingName = getUserInput("Search using a different term: ")
            continue
        # Search with positive results
        else:

            # Present user with results by name and ask for a choice
            searchResults = []
            for ingredients in search["foods"]:
                searchResult = ingredients["description"]
                searchResults.append(searchResult)
            userChoice = chooseFromList(
                searchResults, "cancel or search again?", returnIndex=True
            )

            # If user not satisfied with search reasults search for something else
            if userChoice == len(searchResults) - 1:
                print("type 'cancel' to go back")
                ingName = getUserInput("Search using a different term: ").lower()
                if ingName == "cancel":
                    return
                else:
                    continue
            else:
                break

    # Show users choice
    print(f"\n      You chose: {search['foods'][userChoice]['description']}\n")

    # Get selected food ingredients from the website
    nutrients = search["foods"][userChoice]["foodNutrients"]
    output = {}

    # Ask user to Name ingredient and input it lowercase
    while True:
        output["name"] = getUserInput(
            "How would you like to name your ingredient: "
        ).lower()

        # Check if chosen name is in the database already
        if FOOD_TABLE.isInTable("name", output["name"]):
            print("\nName already on database, Please use a different name")
            print(f"\n      You chose: {search['foods'][userChoice]['description']}\n")
            continue
        break

    # Define nutrients to search for by their nutrient number
    nutrientDict = {"203": "proteins", "204": "fats", "205": "carbs", "208": "kcal"}

    # Set default nutrient amounts to 0
    for item in nutrientDict.values():
        output[item] = 0

    # Get information on nutrients in nutrientDict
    for nutrient in nutrients:
        if nutrient["nutrientNumber"] in nutrientDict.keys():
            output[nutrientDict[nutrient["nutrientNumber"]]] = nutrient["value"]

    # Add to database and notify user operation was successfull
    FOOD_TABLE.addRow(**output)
    print(f"\n       Successfully added item to database: {output['name']}\n")

    return output["name"]


if __name__ == "__main__":
    main()
