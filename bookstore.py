import os
import sqlite3

def main():
    cnt = 1
    while cnt == 1:
        print("Welcome to bookstore!")
        while cnt ==1:
            acclogin = input(str('do you have an account?(Y/N)'))
            if acclogin == 'N':
                new_uname = input(str("Enter A Unique UserName \n"))
                new_password = input(str("Enter A Password \n" ))
            elif acclogin == "Y":
                uname = input(str("Please enter your user"))
                password = input(str("please enter your password"))
            else:   
                print("error please try again")
                
                
                             
                
                
                             
                             
        
    
main()
