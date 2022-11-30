import sys
#sys.path.insert(0,"..")

from Inventory import *
from Cart import *
from User import *

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Methods-Project-DB"
    )
    cursor = connection.cursor()
    print("Connected to Database")


except:
    print("Couldn't Connect to Database")
    sys.exit()

def create_user(first_name, last_name, username, password, credit_card, shipping_address, phone_number):

    tuple = (phone_number, shipping_address, password, first_name, last_name,username, credit_card)
    queryStr = 'INSERT INTO Users (PhoneNumber,ShippingAddress, Password, FirstName, LastName, Username, CreditCard) VALUES (%s,%s,%s,%s,%s,%s,%s)'
    try:
        cursor.execute(queryStr, tuple)
        connection.commit()
    except:
        pass

inv = Inventory(connection)

#create_user("Frank","Smith", "frank28","dog","1234556","13 Road ST", "5564564567")

currentUser = User(connection, "Nate15")

cart = Cart(connection, currentUser.getCartID())

inv.showInventory()

#inv.updateQuantity("1234" , 2)

#inv.showInventory()

#cart.addItemToCart("1234", 4)

#cart.viewCart()

#cart.clearCart()

#cart.removeItemFromCart("9780140350067")



#cart.addItemToCart("1234", 6)

cart.viewCart()

currentUser.checkout()

#cart.clearCart()

#cart.viewCart()

#inv.addItem(1234,28,10,"Stephanie Meyer", "Twilight")
