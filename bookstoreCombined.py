import os
import sys
#from Inventory import *
#import mysql.connector
import sqlite3
from sqlite3.dbapi2 import Connection, Cursor, paramstyle

class user_class:
    def __init__(self, id, first_name, last_name, username, password, credit_card, shipping_address, billing_address):
        user_class.id = id
        user_class.first_name = first_name
        user_class.last_name = last_name
        user_class.username = username
        user_class.password = password
        user_class.credit_card = credit_card
        user_class.shipping_address = shipping_address
        user_class.billing_address = billing_address


class user():
    def __init__(self):
        self.user: user_class = None

    def create_user(self, first_name, last_name, username, password, credit_card, shipping_address, billing_address):

        tuple = (first_name, last_name, username, password, credit_card, shipping_address, billing_address)
        queryStr = '''INSERT INTO user VALUES (?, ?, ?, ?, ?, ?, ?)'''
        try:
            connection.execute(queryStr, tuple)
            connection.commit()
        except:
            pass

    def delete_user(self):
        connection.execute("DELETE FROM user WHERE rowid=?", (self.user.id,))
        connection.commit()

    def edit_shipping(self):
        new_address = input(str("Enter your new Shipping Address: "))
        new_billing_address = input(str("Enter your new Billing Address: "))
        tuple = (new_address, new_billing_address, self.user.id)
        connection.execute('''UPDATE user SET shipping_address = ?, billing_address = ? WHERE rowid=?''', tuple)
        connection.commit()
        self.user.shipping_address = new_address
        self.user.billing_address = new_billing_address


    def edit_pay_method(self):
        new_card = input(str("Enter your new payment info: "))
        tuple = (new_card, self.user.id)
        connection.execute('''UPDATE user SET credit_card = ? WHERE rowid=?''', tuple)
        connection.commit()
        self.user.credit_card = new_card

    def edit_password(self):
        new_password = input(str("Enter your new Password: "))
        tuple = (new_password, self.user.id)
        connection.execute('''UPDATE user SET password = ? WHERE rowid=?''', tuple)
        connection.commit()
        self.user.password = new_password

    def verify(username_entered, password_entered):

        queryStr = '''SELECT rowid, * FROM user WHERE username=?'''
        result = connection.execute(queryStr, (username_entered,)).fetchone()

        if result:
            if result[4] == password_entered:
                user = user_class(result[0], result[1], result[2], result[3], result[4], result[5], result[6],
                                       result[7])
                return user
            else:
                return None

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
    
    inv = Inventory(connection)
    
    

    cnt = 1
    while cnt == 1:
        print("Welcome to bookstore!")
        while cnt ==1:
            try:
                acclogin = input(str('do you have an account?(Y/N, or Quit to exit) '))
                if acclogin == "quit" or acclogin =="Quit":
                    exit()
                    
                elif acclogin == 'N':
                    print("Lets make one")
                    new_uname = input(str("Enter A Unique UserName \n"))
                    new_password = input(str("Enter A Password \n" ))
                    first_name = input(str("Enter Your first name"))
                    last_name = input(str("Enter your last name"))
                    address = input(str("enter your address"))
                    payinfo = input(str("Please enter your card number"))
                elif acclogin == "Y":
                    uname = input(str("Please enter your username"))
                    password = input(str("please enter your password"))
                else:   
                    print("error please try again")
            except ValueError:
                print('error please try again')
                continue
                             
        
    
main()
