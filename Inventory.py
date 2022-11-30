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
        self.cursor.execute(query,details)
        self.connection.commit()

    def updateQuantity(self,ISBN,num):
        details = (str(ISBN),)
        query = "SELECT Quantity FROM Inventory WHERE ISBN = %s"

        self.cursor.execute(query,details)

        try:
            current = self.cursor.fetchall()[0][0]
        except:
            print("Invalid ISBN")
            return

        if int(current) == 0 and num > 0:
            print("Cannot checkout. Item in cart is out of stock")
            return False
        else:
            current = int(current) - num;
            details = (str(current), str(ISBN))
            query = "UPDATE Inventory SET Quantity='" + str(current) + "' WHERE ISBN = '" + str(ISBN) + "'"
            self.cursor.execute(query)
            self.connection.commit()
