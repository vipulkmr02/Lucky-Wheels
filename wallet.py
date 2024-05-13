# Project: Lucky Reels

# The objective of this file is to handle the money
# of the user and also make the Transactions & the
# Balance of the User PERSISTENT using a DB

import sqlite3


class Structs:
    '''
    Structs are basically individual 
    storage items for data to be stored
    '''

    def __init__(self, name: str):
        self.NAME = name.upper()
        self.sl3_connection = sqlite3.connect("database")
        self.cursor = lambda: self.sl3_connection.cursor()


    def __del__(self):
        self.sl3_connection.close()

    def destroy(self):
        cur = self.cursor()
        cur.execute(f"DROP TABLE {self.NAME}")
        cur.close()

    def read(self, PrimaryKey: str = None):
        cur = self.cursor()

        cur.execute(f"SELECT * FROM {self.NAME} WHERE ID={PrimaryKey}")
        result = cur.fetchall()
        cur.close()
        return result


    def write(self, values: tuple, condition: str = None):
        cur = self.cursor()

        if condition:
            cur.execute(f"DELETE FROM {self.NAME} WHERE {condition}")

        cur.execute(f"INSERT INTO {self.NAME} VALUES {values}")
        cur.execute("COMMIT")
        cur.close()
        self.sl3_connection.close()


def instantiateDatabase():
    '''
    This function creates the database
    with he necessary schemas
    '''
    newDB = sqlite3.connect("database")
    cursor = newDB.cursor()

    cursor.execute(
        "CREATE TABLE WALLETS \
                (ID INTEGER PRIMARY KEY AUTOINCREMENT, \
                NAME VARCHAR(255), \
                BALANCE INT)")
    cursor.execute(
        "CREATE TABLE TRANSACTIONS \
                (ID INTEGER PRIMARY KEY AUTOINCREMENT, \
                TYPE VARCHAR(6), \
                AMOUNT INT)")
    cursor.execute("INSERT INTO WALLETS VALUES (0, 'test', 0)")
    cursor.execute("COMMIT")
    cursor.close()
    newDB.close()


def createWallet(Name):
    from random import random
    id = random() * 100 // 1
    wlt = Structs("WALLETS")
    wlt.write((id, Name, 0));
    return id


class Wallet:
    def __init__(self, ID: int):
        self.id = ID
        self.transactions = Structs("transactions")
        self.name = ''
        self.balance = 0
        self.history = self.transactions.read(self.id)
        self.readBalance()


    def readBalance(self):
        wallet = Structs("wallets")
        result = wallet.read(self.id)[0]
        self.name = result[1]
        self.balance = result[2]
        del wallet
        return self.name, self.balance


    def updateBalance(self, newBalance: int):
        if newBalance == self.balance: return
        delta = newBalance - self.balance
        transaction_type = "CREDIT" if delta > 0 else "DEBIT "
        wallet = Structs("wallets")
        wallet.write((self.id, self.name, newBalance), f"ID={self.id}")
        self.transactions.write((self.id, transaction_type, delta))
        self.readBalance()


