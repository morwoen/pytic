import numpy as np
import pickle
import random

data = {}

def hashBoard(board):
    boardNP = np.array(board)
    result = ""
    for item in boardNP.flatten():
        if not item:
            result += "e"
        else:
            result += item
    return result

# Returns row, column of the AI's action
def nextMove(board):
    boardHash = hashBoard(board)
    if boardHash in data:
        # analyse previous data
        situation = data[boardHash]
        total = float(situation["total"])

        bestAction = ""
        bestChance = 0

        actions = without(situation.keys(), "total")

        for action in actions:
            chance = situation[action] / total
            if chance > bestChance:
                bestChance = chance
                bestAction = action

        splitAction = bestAction.split(",")
        return int(splitAction[0]), int(splitAction[1])

    else:
        possibleActions = []
        for rindex, row in enumerate(board):
            for cindex, value in enumerate(row):
                if not value:
                    possibleActions.append([rindex, cindex])

        if len(possibleActions):
            randomChoice = random.randint(0, len(possibleActions) - 1)
            choice = possibleActions[randomChoice]
            return choice[0], choice[1]
        return -1, -1

# Remember all actions
def remember(actions):
    for result in actions:
        board = result[0]
        row = result[1]
        column = result[2]

        boardHash = hashBoard(board)

        actionKey = str(row) + "," + str(column)
        if boardHash in data:
            # already been there, remember
            situation = data[boardHash]
            situation["total"] += 1
            if actionKey in situation:
                situation[actionKey] += 1
            else:
                situation[actionKey] = 1

        else:
            # Never been in this situation
            data[boardHash] = {
                "total": 1
            }
            data[boardHash][actionKey] = 1

def won():
    registerOutcome("wins")

def lost():
    registerOutcome("losses")

def tie():
    registerOutcome("ties")

def registerOutcome(key):
    if key in data:
        data[key] += 1
    else:
        data[key] = 1

    if "games" in data:
        data["games"] += 1
    else:
        data["games"] = 1

# Returns true if there are no more actions
def isTie(board):
    boardHash = hashBoard(board)
    return "e" not in boardHash

# Checks the board if anybody is winning
def isWinning(board):
    boardNP = np.array(board)
    for index in range(len(boardNP)):
        if same(boardNP[index]):
            return boardNP[index][0]
        if same(boardNP[:, index]):
            return boardNP[:, index][0]

    if same(np.diag(boardNP)):
        return boardNP[0][0]
    fliped = np.fliplr(boardNP)
    if same(np.diag(fliped)):
        return fliped[0][0]

    return ""

# Checks if array contains only identical non empty items
def same(array):
    if len(array) < 1:
        return True

    value = array[0]
    if not value:
        return False

    for index in range(1, len(array)):
        if value != array[index]:
            return False

    return True

def load():
    global data
    try:
        dataFile = open(r'data.pkl', 'rb')
        data = pickle.load(dataFile)
        dataFile.close()
        print "Previous data loaded"
    except:
        print "No data found, starting clean"

def save():
    global data
    try:
        dataFile = open(r'data.pkl', 'wb')
        pickle.dump(data, dataFile)
        dataFile.close()
        print "Data saved"
    except:
        print "Failed to save data"

def without(array, item):
    result = []
    for value in array:
        if value != item:
            result.append(value)
    return result
