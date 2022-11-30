import os
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

