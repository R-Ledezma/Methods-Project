import os
import sys
from Inventory import *

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
            acclogin = input(str('do you have an account?(Y/N)'))
            if acclogin == 'N':
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
                #if unname catch
            else:   
                print("error please try again")
                
                
                             
                
                
                             
                             
        
    
main()
