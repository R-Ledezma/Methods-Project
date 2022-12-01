import math


## opens a file in read mode
## filename received as a parameter
def openFile(filename):
    try:
        infile = open(filename, "r")

        print("File opened.")
    except IOError:
        print("File by that name does not exist")

## takes two numbers and returns
## the result of a division
def numbers(num1, num2):
    num1 = int(num1)
    num2 = int(num2)
    try:
        return num1 / num2
    except (ZeroDivisionError, TypeError):
        print("you cant do that")


## takes in two points
## finds the distance between the points
def dist(x1, y1, x2, y2):
    try:
        x1=int(x1)
        y1=int(y1)
        x2=int(x2)
        y2=int(y2)
        dist = abs(x2 - x1) ** 2 + abs(y2 - y1) ** 2
        dist = math.sqrt(dist)
        return dist
    except(ZeroDivisionError, TypeError):
        print("how. stop. please")
        

## takes in a string -- reverses it
## then compares the two
def isPalindrome(temp):
    temp=str(temp)
    if len(temp) !=1 or len(temp)!=0:
        
        try:
               
            test = temp[::-1]

            if(test == temp):
                return True

            else:
                return False
        except ValueError:
            print("value errror")
    else:
        print("to short to be palandrone")
                

## has input to receive two numbers
## divides the two, then outputs the result
def divide():
    try:
        num1 = int(input("Enter a number: "))
        num2 = int(input("Enter another number: "))

        div = num1 / num2

        print("Your numbers divided is:", div)
    except (ZeroDivisionError, TypeError):
        print("you cant do that")

## returns the squareroot of a particular number
def sq(num):
    try:
    
        if num > 0:
            return math.sqrt(num)
        else:
            print("converting negative to positve")
            return math.sqrt(num)
    except ValueError:
        print("value error")
## grabs user's name
## greets them by their entire name
## names should be strings
def greetUser(first, middle, last):
    try:
        first=str(first)
        middle=str(middle)
        last=str(last)
        print("Hello!")
        print("Welcome to the program", first, middle, last)
        print("Glad to have you!")
    except ValueError:
        print(any(char.isdiget() for char in inputString))
        print("you had numbers in ther")

## takes in a Python list
## attempts to display the item at the index provided
def displayItem(numbers, index):
    try:
        if len(numbers)> index +1 and len(numbers)> 1:
                print("Your item at", index, "index is", numbers[index])
            
        else:
            print("index too large. out of range")
    except ValueError:
        print("value error")
        
            


