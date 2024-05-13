# Project: Lucky Reels

# This is the core file which has all the necessary functions 
# and the classes required for the core functioning of the game
# The gui is going to be in a separate file which will be using
# QT Framework, for cross-platform support of the application

#!/usr/bin/python3
from datetime import datetime
from time import sleep
from sys import argv
from wallet import *


REWARDS = {
    'a': -.20,
    'b': -.30,
    'c': -.50,
    '6': +.50,
    '7': +.75,
    '8': +.25,
    'x': 0
}

VIEW = [
        ['a', '6', 'b', 'x', 'c', '7', '8']
] * 3

LINES, SLOTS = 3, len(VIEW)
JACKPOT = [4, 4, 4]


def spin(indices):

    '''
    spins the slots in VIEW list
    '''

    for index in range(SLOTS):
        view = VIEW[index]
        i = indices[index]
        VIEW[index] = view[i:] + view[:i]
 

def rSpin(winRate):

    '''
    use this function to spin the slots
    randomize the slots multiple times with
    a win rate, 

    winRate should be less than (winRate < 50)
    '''

    for i in range(SLOTS):
        MS = datetime.now().microsecond 
        add = (MS % SLOTS) + 1

        if (MS % 100 < winRate):
            add = VIEW[i].index('7') - 1

        VIEW[i] = VIEW[i][add:] + VIEW[i][:add]


def getLine():
    ''' returns the current playline '''
    return [ x[1] for x in VIEW ]


def calculateReward(balance = 1):
    '''
    calculates the reward using the
    current playline if no balance 
    is there, the default will be 1
    '''
    
    combination = getLine()
    change = 0
    
    if len(set(combination)) == 1 and combination[0] == '7':
        r = REWARDS[combination[0]] * 10
        change = balance * r

    else:
        for x in combination:
            change += REWARDS[x] * balance

    return balance + change


def printSlot():
    '''
    prints the current playline on 
    the console
    '''

    slotString = ''
    
    for i in range(LINES):
        for j in VIEW:
            slotString += j[i] + ' | '
        slotString += '\b' * 3 + '\n'

    print(slotString)


if __name__ == '__main__':
    rSpin(0)

    if len(argv) == 1:
        print("Please give some arguments")
        exit(-1)

    if argv[1] == 'SPIN':
        # wlt = Wallet(argv[2])
        winRate = 10 if len(argv) == 2 else int(argv[2])
        rSpin(winRate)
        print('|'.join(getLine()))

    elif argv[1] == 'WALLET':
        if len(argv) == 3:
            wId = argv[2] 
        else:
            print("Please specify ID")
            exit(-1)

        print(f"Wallet ID: {wId}\n\n")
        print("--- Transactions ---")
        wallet = Wallet(wId)
        print("\n".join(wallet.history))
    
    elif argv[1] == 'REGISTER':
        if len(argv) == 3:
            name = argv[2]
        else:
            name = input("NAME: ")

        wId = createWallet(name)
        print(wId)
    
    elif argv[1] == 'clearDB':
        Structs("WALLETS").destroy()
        Structs("TRANSACTIONS").destroy()
        instantiateDatabase()

    exit(0)
