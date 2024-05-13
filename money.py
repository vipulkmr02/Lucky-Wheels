# deprecated file: money.py

REWARDS = {
    'a': -.05,
    'b': -.10,
    'c': -.15,
    '6': +.05,
    '7': +.10,
    '8': +.02,
    'x': 0
}


def calculateReward(combination, BETT):
    if len(set(combination)) == 1:
        r = REWARDS[combination[0]] * 10
        change = BETT * r

    else:
        change = 0

        for x in combination:
            change += REWARDS[x] * BETT

    return BETT + change


class wallet:
    def __init__(self):
        self.balance = 0

    def setBalance(self, balance):
        self.balance = balance

    def transaction(self, newBalance):
        change = self.balance - newBalance
        print("New Transaction:",change)

