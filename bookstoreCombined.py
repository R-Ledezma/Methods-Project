import os
import sys
#from Inventory import *
#import mysql.connector
import sqlite3
from sqlite3.dbapi2 import Connection, Cursor, paramstyle

def create_user(first_name, last_name, username, password, credit_card, shipping_address, phone_number):

    tuple = (phone_number, shipping_address, password, first_name, last_name,username, credit_card)
    queryStr = 'INSERT INTO Users (PhoneNumber,ShippingAddress, Password, FirstName, LastName, Username, CreditCard) VALUES (%s,%s,%s,%s,%s,%s,%s)'
    try:
        cursor.execute(queryStr, tuple)
        connection.commit()
    except:
        pass
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

    def delete_user(self):
        self.cursor.execute("DELETE FROM Users WHERE UserID=?", (self.UserID,))
        self.connection.commit()

    def edit_shipping(self):
        new_address = input(str("Enter your new Shipping Address: "))
        new_billing_address = input(str("Enter your new Billing Address: "))
        tuple = (new_address, self.UserID)
        self.cursor.execute('''UPDATE Users SET shipping_address = ? WHERE rowid=?''', tuple)
        self.connection.commit()
        print("New address: " + new_address + "\n")

    def edit_pay_method(self):
        new_card = input(str("Enter your new payment info: "))
        tuple = (new_card, self.UserID,)
        self.cursor.execute('''UPDATE Users SET credit_card = ? WHERE rowid=?''', tuple)
        self.connection.commit()
        print("New credit card info: " + new_card + "\n")

    def edit_password(self):
        new_password = input(str("Enter your new Password: "))
        tuple = (new_password, self.UserID,)
        self.connection.execute('''UPDATE Users SET password = ? WHERE rowid=?''', tuple)
        self.connection.commit()
        print("New password is : " + new_password + "\n")

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
class Cart:

    def __init__(self, connection, cartID):
        self.connection = connection
        self.cursor = connection.cursor()
        self.cartID = str(cartID)

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

    def clearCart(self):
        query = "DELETE FROM CartItem WHERE CartID =" + str(self.cartID)
        self.cursor.execute(query)
        self.connection.commit()

    def viewCart(self):
        self.cursor.execute("SELECT ISBN, Quantity FROM CartItem WHERE CartID = " + self.cartID)
        items = self.cursor.fetchall()
        print("\nCART CONTENTS: \n")

        total = 0

        for x in items:
            self.cursor.execute("SELECT Title, Price FROM Inventory WHERE ISBN = " + x[0] + "")
            title = self.cursor.fetchall()
            print(title[0][0] + " | Quantity: " + str(x[1]) + " | Price: $" + str(x[1] * title[0][1]))
            total += (x[1]*title[0][1])

        print("TOTAL: $" + str(total) + "\n")

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



def main():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="Methods-Project-DB"
        )
        print("Connected to Database")

    except:
        print("Couldn't Connect to Database")
        sys.exit()
    cursor = connection.cursor()
    inv = Inventory(connection)
    
    loginCheck == False

    cnt = 1
    while cnt == 1:
        print("Welcome to bookstore!")
        while loginCheck == False:
            try:
                acclogin = input(str('do you have an account?(Y/N, or Quit to exit) '))
                if acclogin == "quit" or acclogin =="Quit":
                    exit()
                    
                elif acclogin == 'N':
                    print("Lets make one")
                    new_uname = input(str("Enter A Unique UserName \n"))
                    new_password = input(str("Enter A Password \n" ))
                    f_name = input(str("Enter Your first name"))
                    l_name = input(str("Enter your last name"))
                    address = input(str("enter your address"))
                    payinfo = input(str("Please enter your card number"))
                    phoneNum = input(str("Please enter your phone number"))
                    create_user(f_name, l_name, new_uname, new_password, payinfo, adress, phoneNum) 
                elif acclogin == "Y":
                   liusername=input(str("Enter Your UserName \n"))
                   lipassword=input(str("Enter Your Password \n" ))
                   query = "SELECT Password FROM Users WHERE Username = '" + str(liusername) + "'"
                   cursor.execute(query)
                   str(password = cursor.fetchall()[0])
                   if lipassword == password:
                       loginCheck = True
                   else:
                       acclogin == 'Y'
                       print("incorrect password or username")
                   
                   
                 
                else:   
                    print("error please try again")
            except ValueError:
                print('error please try again')
                continue
        currentUser = User(connection, liusername)
        cart = Cart(connection, currentUser.getCartID())
        print("What would you like to do. \n 1.View all books \n 2.Add Item to cart. \n 3.Remove Items from cart \n 4.Checkout \n 5.view order history \n 6.edit user account \n 7.delete account")  
        
                             
        
    
main()
