import mysql.connector
import sys


class Inventory:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def showInventory(self):
        print("Available Books: \n")
        self.cursor.execute("SELECT * FROM Inventory")
        contents = self.cursor.fetchall()
        for x in contents:
            print("ISBN: " ,x[0], "Quantity: ", x[1], "| Price: $", x[2], "| Author: ", x[3], "| Title: ", x[4], "\n")

    def addItem(self,ISBN,Quantity,Price,Author,Title):
        details = (str(ISBN),str(Quantity), str(Price),str(Author),str(Title))
        query = "INSERT INTO Inventory (ISBN,Quantity,Price,Author,Title) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query, details)
        self.connection.commit()

