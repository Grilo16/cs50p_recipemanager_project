# Recipe and food stock manager showing to jay
#### Video Demo:  <URL HERE>
#### Description:

### This program starts by checking for a database and creating a database.db file containing the following 3 tables if one is not found:

    -food_db: This table stores from a chosen food, id, Name, kcal, proteins, fats, carbs, amount, and stock_amount
        id = Unique number given to each entry to the database
        name = User decided name for the food
        Kcal = Amount of calories
        proteins = Amount of proteins in grams
        fats = Amount of fats in grams
        carbs = Amount of carbs in grams
        amount = The amount to divide nutritional values by
        stock_amount = Quantity of food currently in stock

    -recipes: This table stores the name of each added recipe and assigns it a unique id
        id = Unique id used to search for ingredients
        name = Recipe name given by the user

    -ingredients: This table is used as a many to many relationship table where it stores the amount, food_id and recipe_id
        food_id = from food_db table
        recipe_id = from recipes table
        quantity = amount of ingreadient required by the recipe

Example database

    food_db :
    +----+----------------+-------+----------+------+-------+----------+--------------+
    | id |      name      | kcal  | proteins | fats | carbs | quantity | stock_amount |
    +----+----------------+-------+----------+------+-------+----------+--------------+
    | 1  | brown bread    | 254.0 | 12.3     | 3.55 | 43.1  | 100.0    | 1000         |
    | 2  | cheddar cheese | 408.0 | 23.3     | 34.0 | 2.44  | 100.0    | 1000         |
    | 3  | salted butter  | 717.0 | 0.0      | 82.2 | 0     | 100.0    | 1000         |
    | 4  | chicken        | 156.0 | 23.9     | 5.95 | 0.0   | 100.0    | 1000         |
    +----+----------------+-------+----------+------+-------+----------+--------------+

    recipes :
    +----+------------------+
    | id |       name       |
    +----+------------------+
    | 1  | cheese sandwich  |
    | 2  | chicken sandwich |
    +----+------------------+

    ingredients :
    +-----------+---------+----------+
    | recipe_id | food_id | quantity |
    +-----------+---------+----------+
    | 1         | 1       | 200      |
    | 1         | 2       | 100      |
    | 1         | 3       | 10       |
    | 2         | 4       | 100      |
    | 2         | 1       | 200      |
    | 2         | 3       | 20       |
    +-----------+---------+----------+

### Next the program will present the user with a numbered list of options for the user to choose from.

    1 Show all recipes
    2 Show ingredients in stock
    3 Cook from available recipes
    4 Create a recipe
    5 Add to food stock
    6 Add ingredient to database
    7 Close program

#### 1 Show all recipes
This option presents the user with a numbered list of recipes that the user has inputed into the database and promts the user with a choice of showing recipe ingrediends or going back

    -Choose an option

    1 cheese sandwich
    2 chicken sandwich
    3 Go Back

    Show ingredients for recipe number:

The user selects an option by inputing the corresponding option number, in the case the user inputs 1, the program is going to show the required ingredients for a cheese sandwich

    Show ingredients for recipe number: 1

    cheese sandwich

    200g of brown bread
    100g of cheddar cheese
    10g of salted butter
    Press enter to continue

The user can then press enter to go back to the previous page, and if the user chooses the last option the program will return to the initial list of choices.

#### 2 Show ingredients in stock
This option presents the user with choices containing all ingredients that they currently have in stock as a list containing ingredient names and amounts in grams

    Available stock items

    1 1000g of brown bread
    2 1000g of cheddar cheese
    3 1000g of salted butter
    4 1000g of chicken
    5 Go back

    Show nutrients for ingredient number:

If the user chooses an item, the nutritional values of the item will be displayed, in this example the user will have chosen option 4.

    Show nutrients for ingredient number: 4
    100g of chicken has 156.0 calories
    23.9g of proteins 0.0g of carbs and 5.95g of fats
    Press enter to continue

pressing enter will take the user to the show ingredients in stock list where the last option will take the user to the main selection menu.


#### 3 Cook from available recipes
This option presents the user with a list of recipes where they currently have the nescessary ingredients for

    Choose recipe to cook

    1 cheese sandwich
    2 chicken sandwich
    3 Go back

    choose an option:

Where if the user chooses a recipe the corresponding ingredients for that recipe will be removed from the user's stock and the recipe will be displayed to the user, in this example we will use option 1 cheese sandwich:


    you cooked: cheese sandwich
    You have used:

    200g of brown bread
    100g of cheddar cheese
    10g of salted butter

    Press enter to continue

Now if we check the ingredients in stock the values will have been updated

    Available stock items

    1 800g of brown bread
    2 900g of cheddar cheese
    3 990g of salted butter
    4 1000g of chicken
    5 Go back

    Show nutrients for ingredient number:


#### 4 Create a recipe
This option allows the user to create a recipe by prompting the user for inputs

the first input will ask for a recipe name

    choose an option: 4

    Please name your recipe:
    Type 'cancel' to stop inputing recipe

    Recipe name:

in this example we will add a chicken cheese sandwich. leading the program to prompt the user for ingredients, followed by amounts in grams.

    Recipe name: chicken cheese sandwich

    Please name an ingredient
    Type 'done' to stop inputing ingredients

    Ingredient:

First ingredient will be chicken and amount will be 200

    Ingredient: chicken
    amount: 200

    Please name an ingredient
    Type 'done' to stop inputing ingredients

    Ingredient:

leading the program to prompt the user for another ingredient until user types done.

For this example recipe we will further add 100 grams of cheese, 200 grams of bread, and 20 grams of butter.

Once the user types done the program will present the user with the recipe inputed and options to either modify or delete an ingredient, add another ingredient or insert the recipe into the database or cancel inputing a recipe.

    Ingredient: done

    Recipe: chicken cheese sandwich
    change any ingredients?
    1 200g of chicken
    2 100g of cheese
    3 200g of bread
    4 20g of butter
    5 Add extra ingredient to recipe
    6 All ingredients are correct, I'd like to input recipe into the database
    7 Cancel inputing recipe

    choose an option:

for this example we will change option 4 20g of butter

    choose an option: 4

    You are changing the entry for:
    20g of butter

    -- New entry --
    Ingredient name(del to delete ingredient):

Now the user can either add a completely new ingredient, delete this item from the recipe or simply input the same name to change the ingredient's amount.

in this case we will use butter again and increase the amount to 30g.

    -- New entry --
    Ingredient name(del to delete ingredient): butter
    Ingredient amount: 30

which results in:

    Recipe: chicken cheese sandwich
    change any ingredients?
    1 200g of chicken
    2 100g of cheese
    3 200g of bread
    4 30g of butter
    5 Add extra ingredient to recipe
    6 All ingredients are correct, I'd like to input recipe into the database
    7 Cancel inputing recipe

    choose an option:

For the sake of this example we will add a test ingredient and subsequently remove it as follows

    choose an option: 5
    --Adding extra ingredient--
    Ingredient name: test ingredient
    Ingredient amount: 69

resulting in :

    Recipe: chicken cheese sandwich
    change any ingredients?
    1 200g of chicken
    2 100g of cheese
    3 200g of bread
    4 30g of butter
    5 69g of test ingredient
    6 Add extra ingredient to recipe
    7 All ingredients are correct, I'd like to input recipe into the database
    8 Cancel inputing recipe

    choose an option:

now to remove the ingredient we will select it and type del in the prompt

    choose an option: 5

    You are changing the entry for:
    69g of test ingredient

    -- New entry --
    Ingredient name(del to delete ingredient): del


resulting in :

    Recipe: chicken cheese sandwich
    change any ingredients?
    1 200g of chicken
    2 100g of cheese
    3 200g of bread
    4 30g of butter
    5 Add extra ingredient to recipe
    6 All ingredients are correct, I'd like to input recipe into the database
    7 Cancel inputing recipe

    choose an option:

Now that the recipe is complete we will choose to input it into the database in this case option 6.

If the ingredient name does not fully match with any item in the database the program will suggest simillar items or an option for an online search to input a new ingredient in the database.

for this example chicken was automatically entered as it matches an item in the database, however for cheese we get presented with the following choice:

    choose an option: 6
    Adding recipe to database

    Choose an option

    1 cheddar cheese
    2 Search online

    choose an option:

For this example we will only use items in our private database as follows and once all items have been selected the recipe will be inputed into the database and the program will display the following message:

    Adding recipe to database

    Choose an option

    1 cheddar cheese
    2 Search online

    choose an option: 1

    Choose an option

    1 brown bread
    2 Search online

    choose an option: 1

    Choose an option

    1 salted butter
    2 Search online

    choose an option: 1

    Successfully added chicken cheese sandwich to the database

    Press enter to continue

once the user presses enter the program will return to the main page.

Now if we check our recipes we should see that a new recipe has been added to the list:

    Choose an option

    1 cheese sandwich
    2 chicken sandwich
    3 chicken cheese sandwich
    4 Go Back

    Show ingredients for recipe number:


#### 5 Add to food stock

This option allows the user to add an amount to the stock of that ingredient in the database

    choose an option: 5
    Type 'cancel' to stop adding ingredient
    Ingredient name:

in this example we will add 1000g of chicken to the stock as follows, leading the program to present the user with choices of ingredients from the database with a matching name to add to, or an option to add a new ingredient to the database.

    Ingredient name: chicken
    Amount in grams: 1000

    Choose an option

    1 chicken
    2 search online

    choose an option:

for this example we will add it to the current entry of chicken in our database.

    choose an option: 1

    Successfully added 1000g to the stock of chicken

    1 Continue adding ingredients
    2 Go back

    choose an option:

and now the user can continue adding new ingredients to the stock or go back to the main page.

and now if we go to our ingredients in stock option we should see that the value for chicken has been updated.

    Available stock items

    1 800g of brown bread
    2 900g of cheddar cheese
    3 990g of salted butter
    4 2000g of chicken
    5 Go back

    Show nutrients for ingredient number:

#### 6 Add ingredient to database
This option allows the user to search from the Food central database for new ingredients to be added to our local database with the name of our choosing.

    choose an option: 6
    Type 'cancel' to go back
    Ingredient name:

now we can search for any ingredient, in this case we will search for ham.

The program will then present the user with 25 options to choose from or to search for a different term as well as cancel the search.

    Ingredient name: ham

    Choose an option

    1 Ham, sliced, restaurant
    2 Ham, sliced, pre-packaged, deli meat (96%fat free, water added)
    3 Ham, minced
    4 Ham and cheese spread
    5 Ham salad spread
    6 Ham, chopped, canned
    7 Ham, chopped, not canned
    8 Babyfood, apples with ham, strained
    9 Babyfood, meat, ham, junior
    10 Babyfood, meat, ham, strained
    11 Fast foods, biscuit, with ham
    12 Ham and cheese loaf or roll
    13 Ham, honey, smoked, cooked
    14 HORMEL, Cure 81 Ham
    15 Fast foods, biscuit, with egg and ham
    16 LEAN POCKETS, Ham N Cheddar
    17 Pork, cured, ham, patties, unheated
    18 Fast foods, croissant, with egg, cheese, and ham
    19 Ham, sliced, regular (approximately 11% fat)
    20 Ham, smoked, extra lean, low sodium
    21 Oscar Mayer, Ham (chopped with natural juice)
    22 Soup, lentil with ham, canned, ready-to-serve
    23 Soup, pea, split with ham, canned, condensed
    24 Ham, turkey, sliced, extra lean, prepackaged or deli
    25 Pork, cured, ham, separable fat, boneless, heated
    26 cancel or search again?

    choose an option:

For this example we will choose the first option


    choose an option: 1

        You chose: Ham, sliced, restaurant

    How would you like to name your ingredient:

And name it as ham:

    How would you like to name your ingredient: ham

        Successfully added item to database: ham

    Press enter to continue

#### 7 Close program
Simply exits the program.


