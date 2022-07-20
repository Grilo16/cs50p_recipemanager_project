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