import os
import sys
from Inventory import *
import mysql.connector
from Cart import *
from User import *


def create_user(first_name, last_name, username, password, credit_card, shipping_address, phone_number, cursor, connection):
    tuple = (phone_number, shipping_address, password, first_name, last_name, username, credit_card)
    queryStr = 'INSERT INTO Users (PhoneNumber,ShippingAddress, Password, FirstName, LastName, Username, CreditCard) VALUES (%s,%s,%s,%s,%s,%s,%s)'
    try:
        cursor.execute(queryStr, tuple)
        connection.commit()
    except:
        pass


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

    loginCheck = False

    cnt = 1
    while cnt == 1:
        print("Welcome to bookstore!")
        while loginCheck == False:
            try:
                acclogin = input(str('do you have an account?(Y/N, or Quit to exit) '))
                if acclogin == "quit" or acclogin == "Quit":
                    exit()

                elif acclogin == 'N':
                    print("Lets make one")
                    new_uname = input(str("Enter A Unique UserName \n"))
                    new_password = input(str("Enter A Password \n"))
                    f_name = input(str("Enter Your first name"))
                    l_name = input(str("Enter your last name"))
                    address = input(str("enter your address"))
                    payinfo = input(str("Please enter your card number"))
                    phoneNum = input(str("Please enter your phone number"))
                    create_user(f_name, l_name, new_uname, new_password, payinfo, address, phoneNum, cursor, connection)
                    loginCheck = True
                    currentUser = User(connection, new_uname)
                    cart = Cart(connection, currentUser.getCartID())

                elif acclogin == "Y":
                    liusername = input(str("Enter Your UserName \n"))
                    lipassword = input(str("Enter Your Password \n"))
                    query = "SELECT Password FROM Users WHERE Username = '" + str(liusername) + "'"
                    cursor.execute(query)
                    password = cursor.fetchall()

                    if password != None:
                        print(str(password[0][0]))
                        if lipassword == password[0][0]:
                            loginCheck = True
                            currentUser = User(connection, liusername)
                            cart = Cart(connection, currentUser.getCartID())
                        else:
                            acclogin == 'Y'
                            print("incorrect password or username")



                else:
                    print("error please try again")
            except ValueError:
                print('error please try again')
                continue

        print("What would you like to do. \n 1.View all books | 2.Add Item to cart |  3.Remove Items from cart | 4.Checkout |\n 5.View order history | 6.Edit user account | 7.Delete account | \n 8.View Cart | 9. Logout")
        decision = input("SELECTION: ")
        if decision == "1":
            inv.showInventory()
        elif decision == "2":
            isbn = input("Enter desired ISBN: ")
            quan = input("How many copies would you like? ")
            cart.addItemToCart(isbn,int(quan))
        elif decision == "3":
            isbn = input("Enter the ISBN of the book you want to remove (will remove all copies) : ")
            cart.removeItemFromCart(isbn)
        elif decision == "4":
            currentUser.checkout()
            cart = Cart(connection, currentUser.getCartID())

        elif decision == "5":
            currentUser.viewOrderHistory()

        elif decision == "6":
            editChoice = input("Which would you like to edit: 1. Shipping Address| 2. Payment Method | 3. Password")
            if editChoice == 1:
                currentUser.editShipping()
            elif editChoice == 2:
                currentUser.editPayMethod()
            elif editChoice == 3:
                currentUser.editPassword()

        elif decision == "7":
            currentUser.deleteUser()
            loginCheck = False

        elif decision == "8":
            cart.viewCart()

        elif decision == "9":
            loginCheck = False
main()