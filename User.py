import mysql.connector
import sys


class User:
    def __init__(self, connection, username):

        #Establishes connection with database, & creates or resumes active cart

        self.connection = connection
        self.cursor = connection.cursor()
        self.cursor.execute("SELECT UserID FROM Users WHERE Username = '" + str(username) + "'")
        self.UserID = self.cursor.fetchall()[0][0]
        self.cursor.execute("SELECT CartID FROM Cart WHERE UserID = '" + str(self.UserID) + "' AND Purchased = '0'")
        test = self.cursor.fetchone()

        if test != None:
            self.cursor.execute("SELECT CartID FROM Cart WHERE UserID = '" + str(self.UserID) + "' AND Purchased = '0'")
            self.CartID = self.cursor.fetchone()[0]
        else:
            self.createCart()

    def getCartID(self):
        return self.CartID

    def deleteUser(self):
        self.cursor.execute("DELETE FROM Cart WHERE UserID= '" + str(self.UserID) + "'")
        self.connection.commit()
        self.cursor.execute("DELETE FROM Users WHERE UserID= '" + str(self.UserID) + "'")
        self.connection.commit()

    def editShipping(self):
        newAddress = input(str("Enter your new Shipping Address: "))
        self.cursor.execute("UPDATE Users SET ShippingAddress = '" + newAddress + "' WHERE UserID = '" + str(self.UserID) +"'")
        self.connection.commit()
        print("New address: " + newAddress + "\n")

    def editPayMethod(self):
        newCard = input(str("Enter your new payment info: "))
        self.cursor.execute("UPDATE Users SET CreditCard = '" + newCard + "' WHERE UserID = '" + str(self.UserID) + "'")
        self.connection.commit()
        print("New credit card info: " + newCard + "\n")

    def editPassword(self):
        newPassword = input(str("Enter your new Password: "))
        self.cursor.execute("UPDATE Users SET Password = '" + newPassword + "' WHERE UserID = '" + str(self.UserID) + "'")
        self.connection.commit()
        print("New password is : " + newPassword + "\n")

    def checkout(self):
        # update inventory to reflect purchases
        self.cursor.execute("SELECT ISBN, Quantity FROM CartItem WHERE CartID = '" + str(self.CartID) + "'")
        results = self.cursor.fetchall()
        for x in results:
            self.updateQuantity(x[0],x[1])
        # set cart purchased flag to 1
        self.cursor.execute("UPDATE Cart SET Purchased = 1 WHERE CartID = '" + str(self.CartID) + "'")
        self.connection.commit()

        # display checkout message
        self.cursor.execute("SELECT ISBN, Quantity FROM CartItem WHERE CartID = " + str(self.CartID))
        items = self.cursor.fetchall()
        print("\nSUCCESSFULLY CHECKED OUT!\n")

        total = 0

        for x in items:
            self.cursor.execute("SELECT Title, Price FROM Inventory WHERE ISBN = " + x[0] + "")
            title = self.cursor.fetchall()
            total += (x[1] * title[0][1])

        print("TOTAL COST: $" + str(total) + "\n")

        # create new cart
        self.createCart()


        return True


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

    def createCart(self):
        details = (str(self.UserID), "0")
        query = "INSERT INTO Cart (UserID, Purchased) VALUES (%s, %s)"
        self.cursor.execute(query, details)
        self.connection.commit()
        self.cursor.execute("SELECT CartID FROM Cart WHERE UserID = '" + str(self.UserID) + "' AND Purchased = '0'")
        self.CartID = self.cursor.fetchone()[0]

    def viewOrderHistory(self):
        # find all carts with user id
        print("Order History: \n")
        self.cursor.execute("SELECT CartID FROM Cart WHERE UserID = '" + str(self.UserID) + "' AND Purchased = '1'")
        orders = self.cursor.fetchall()
        count = 1
        totalPrice = 0
        for x in orders:
            self.cursor.execute("SELECT ISBN, Quantity FROM CartItem WHERE CartID = '" + str(x[0]) + "'")
            order = self.cursor.fetchall()
            #print(order)
            print("ORDER: " + str(count))
            orderPrice = 0
            # Display all carts
            for y in order:
                self.cursor.execute("SELECT Title, Price FROM Inventory WHERE ISBN = '" + str(y[0]) +"'")
                tp = self.cursor.fetchall()
                print("Title: " + str(tp[0][0]) + " Quantity: " + str(y[1]) + " Price: $" + str(tp[0][1] * y[1]) + "\n")
                totalPrice += tp[0][1] * y[1]
                orderPrice += tp[0][1] * y[1]
                #quan = y[1]
                #title = tp[0]
                #price = tp[1]
            print("ORDER TOTAL: $" + str(orderPrice) + "\n")
            count += 1
        print("TOTAL PRICE: $" + str(totalPrice) + "\n")
