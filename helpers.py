import sqlite3

# Returns a list with all available recipes based on ingredients
def recipesAvailable():

    con = sqlite3.connect("database.db")
    cursor = con.cursor()

    # Query database only for recipes where all ingredient stock quantities are higher than recipe requirements
    cursor.execute(
        "SELECT r.name FROM foods_table ft LEFT JOIN ingredients i ON ft.id = i.food_id LEFT JOIN recipes r ON r.id = i.recipe_id GROUP BY recipe_id HAVING min(ft.stock_amount) >= i.quantity ORDER BY i.recipe_id"
    )

    results = [ingredient[0] for ingredient in cursor.fetchall()]

    con.close()
    return results


# Presents a list and returns the value the user chose, optionally return index, add items, change messages
def chooseFromList(
    list,
    *extraItems,
    returnIndex=False,
    title=False,
    noTitle=False,
    inputMessage="choose an option: ",
):
    if not noTitle:
        if title:
            print(title)
        else:
            print("\nChoose an option\n")
    if extraItems:
        for i in extraItems:
            list.append(i)
    index = 0
    for item in list:
        index += 1
        print(index, item)
    print()
    # Get users choice and validate it chooses an item from list
    while True:
        try:
            choice = int(input(f"{inputMessage}")) - 1
        except ValueError:
            print("Please input an integer")
            continue
        except (KeyboardInterrupt, EOFError):
            exit("")
        else:
            if choice < 0 or choice > index - 1:
                print("please input a value within the selection range")
                continue
            else:
                break
    if returnIndex:
        return choice
    return list[choice]


# A code pauser to allow the user to read the output before continuing
def pressToContinue(message="Press enter to continue"):
    try:
        input(message)
    except (KeyboardInterrupt, EOFError):
        exit("")
    return


# Gets users input and validates it as a string or optionally int
def getUserInput(question, makeInt=False):
    while True:
        try:
            name = input(f"{question}").lower().strip()
        except (EOFError, KeyboardInterrupt):
            exit("")
        if makeInt:
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
