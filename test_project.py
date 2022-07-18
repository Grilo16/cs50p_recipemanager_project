import pytest
import mock
import builtins
import sqlite3

# Import functions
from project import pressToContinue
from project import chooseFromList
from project import getUserInput
from project import add_NewIngredient
from project import add_toStock
from project import create_recipeDict
from project import storeRecipeDict
from project import recipesAvailable
from project import cookRecipe


# Set up and clear database test entries
@pytest.fixture
def remove_item_fromdb():
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
    cursor.execute("INSERT INTO food_db (name, kcal, proteins, fats, carbs, quantity, stock_amount) values('test ingredient', 100, 10, 10, 10, 100, 1000)")
    cursor.execute("INSERT INTO food_db (name, kcal, proteins, fats, carbs, quantity, stock_amount) values('test apple', 100, 10, 10, 10, 100, 1000)")
    con.commit()
    con.close()
    yield
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    try:
        cursor.execute("select id from recipes where name like '%test %'")
        result = cursor.fetchone()[0]
        cursor.execute(f"DELETE FROM ingredients where recipe_id = {result}")
    except TypeError:
        pass
    cursor.execute("DELETE FROM recipes where name LIKE '%test %'")
    cursor.execute("DELETE FROM food_db where name LIKE '%test %'")
    con.commit()
    con.close()

# Test classes

# Test functions
def test_pressToContinue():
    with mock.patch.object(builtins, "input", lambda _: " "):
        assert pressToContinue() == None

def test_chooseFromList():
    #Test for List
    with mock.patch.object(builtins, "input", lambda _: 1):
        assert chooseFromList(["yay", "nay"]) == "yay"
    #Test for Extra arguments
    with mock.patch.object(builtins, "input", lambda _: 3):
        assert chooseFromList(["yay", "nay"], "baz") == "baz"
    #Test for showIndex on
    with mock.patch.object(builtins, "input", lambda _: 3):
        assert chooseFromList(["yay", "nay"], "baz", showIndex="on") == 2
    #Test for noChoice on
    assert chooseFromList(["yay", "nay"], "baz", showIndex="on", noChoice="on") == None
    #Test for noMessage on
    assert chooseFromList(["yay", "nay"], "baz", showIndex="on", noChoice="on", noMessage="on") == None
    #Test for message False or something
    assert chooseFromList(["yay", "nay"], "baz", showIndex="on", noChoice="on", noMessage="on", message="test") == None
    #Test for inputMessage
    assert chooseFromList(["yay", "nay"], "baz", showIndex="on", noChoice="on", noMessage="on", message="test", inputMessage="test") == None

def test_getUserInput():
    with mock.patch.object(builtins, "input", lambda _: "Test"):
        assert getUserInput("question") == "test"
    with mock.patch.object(builtins, "input", lambda _: "1"):
        assert getUserInput("question", makeint="on") == 1

@pytest.mark.usefixtures("remove_item_fromdb")
def test_add_NewIngredient():
    # Test adding new ingredient
    mock_inputs = ["3", "test name"]
    with mock.patch("builtins.input", side_effect=mock_inputs):
        assert add_NewIngredient("chicken") == "test name"

    # Test adding new ingredient with repeated name then changing it
    mock_inputs = ["3", "test name", "test name2"]
    with mock.patch("builtins.input", side_effect=mock_inputs):
        assert add_NewIngredient("chicken") == "test name2"

    # Test search again
    mock_inputs = ["26", "beef", "1", "test name3"]
    with mock.patch("builtins.input", side_effect=mock_inputs):
        assert add_NewIngredient("chicken") == "test name3"

    # Test search again cancel
    mock_inputs = ["26", "cancel"]
    with mock.patch("builtins.input", side_effect=mock_inputs):
        assert add_NewIngredient("chicken") == None


@pytest.mark.usefixtures("remove_item_fromdb")
def test_add_toStock():
    mock_inputs = ["1"]
    with mock.patch("builtins.input", side_effect=mock_inputs):
        assert add_toStock("test ingredient", 50) == None

def test_create_recipeDict():
    mock_inputs = ["Test recipe", "test apple", "50", "done"]
    with mock.patch("builtins.input", side_effect=mock_inputs):
        assert create_recipeDict() == {'ingredients': {'test apple': 50}, 'name': 'test recipe'}

@pytest.mark.usefixtures("remove_item_fromdb")
def test_storeRecipeDict():
    recipe = {'ingredients': {'test apple': 50}, 'name': 'test recipe'}
    assert storeRecipeDict(recipe) == None


def test_recipesAvailable():
    recipesAvailable()


def test_cookRecipe():
    cookRecipe()
