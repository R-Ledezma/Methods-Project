import mysql.connector
import sys

class Cart:

    def __init__(self, connection, cartID):
        self.connection = connection
        self.cursor = connection.cursor()
        self.cartID = cartID

    def setCart(self, cartID):
        self.cartID = cartID

    def addItemToCart(self,ISBN, num):
        query = "SELECT Quantity FROM Inventory WHERE ISBN =" + str(ISBN)
        self.cursor.execute(query)
        try:
            quantity = self.cursor.fetchall()[0][0]
        except:
            print("Invalid ISBN")
            return

        if(num > quantity):
            print("There are not enough copies in stock to add to your cart \n")
        else:
            query = "SELECT Quantity FROM CartItem WHERE ISBN =" + str(ISBN) + " AND CartID =" + str(self.cartID)
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            if len(results) == 0:
                query = "INSERT INTO CartItem (ISBN, CartID, Quantity) VALUES ('" + str(ISBN) + "','" + str(self.cartID) + "','" + str(num) + "')"
                self.cursor.execute(query)
                self.connection.commit()
            else:
                newQuan = results[0][0] + num
                query = "UPDATE CartItem SET Quantity = " + str(newQuan) + " WHERE ISBN = " + str(ISBN) + " AND CartID = " + str(self.cartID)
                self.cursor.execute(query)
                self.connection.commit()


    def removeItemFromCart(self, ISBN):
        query = "DELETE FROM CartItem WHERE ISBN =" + str(ISBN) + " AND CartID =" + str(self.cartID)
        self.cursor.execute(query)
        self.connection.commit()

    def viewCart(self):
        self.cursor.execute("SELECT ISBN, Quantity FROM CartItem WHERE CartID = " +  self.cartID)
        items = self.cursor.fetchall()
        print("\nCART CONTENTS: \n")

        total = 0

        for x in items:
            self.cursor.execute("SELECT Title, Price FROM Inventory WHERE ISBN = " + x[0] + "")
            title = self.cursor.fetchall()
            print(title[0][0] + " | Quantity: " + str(x[1]) + " | Price: $" + str(x[1] * title[0][1]))
            total += (x[1]*title[0][1])

        print("TOTAL: $" + str(total) + "\n")