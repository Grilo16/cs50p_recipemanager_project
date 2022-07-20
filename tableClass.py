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