import math
import random

values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

class Player(object):
    # this is the default player object that all other players are built off of (currently performs the best)
    # this object handles playing cards, starting tricks as well as keeping track of its own hand
    def __init__(self, name):
        self.name = name
        self.startingHand = []
        self.valHand = []
        # this dictionary is the thing that the player uses 99% of the time, it will be populated with how many of each card the player has
        self.cardDict = {
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0,
            9: 0,
            10: 0,
            11: 0,
            12: 0,
            13: 0,
            14: 0
        }
        self.totalCards = 0

    def resetPlayer(self):
        # when a new round starts this is called to reset the players hand (bc/ the same objects are reused across rounds)
        self.startingHand = []
        self.valHand = []
        self.cardDict = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}
        self.totalCards = 0

    def sortHand(self):
        # sorts the players hand into a readable hand for us (valHand) and a dictionary for use by the player object
        for card in self.startingHand:
            self.valHand.append(card.value)
        self.valHand.sort()

        # fills in dictionary for how many of each card they have
        for card in self.valHand:
            self.totalCards += 1
            for typeOfCard in self.cardDict:
                if card == typeOfCard:
                    self.cardDict[typeOfCard] += 1
        # print(self.cardDict)

    def draw(self, deck, num=1):
        # draw n number of cards from a given deck
        for i in range(num):
            self.startingHand.append(deck.draw())

    def showValHand(self):
        return self.valHand

    def showHand(self):
        return self.startingHand

    def checkIfAnyNegatives(self):
        # just a testing function to see if they have any cards that they have a negative amount of
        for card in self.cardDict:
            if self.cardDict[card] < 0:
                print(self.name, "has negative cards")
                print(self.cardDict)

    def play(self, cardsOnTop):
        # print(self.name,"'s hand: ",self.cardDict)

        # checks if they are out
        self.totalCards = 0
        for card in self.cardDict:
            self.totalCards += self.cardDict[card]
        if self.totalCards == 0:
            return ['out']

        if cardsOnTop[0] == 2:
            return ['pass']

        # loops through cardDict (goes forward so plays lowest possible first)
        for card in self.cardDict:
            # checks if its the same type of trick and if they have enough cards to play on the trick (at least one)
            if self.cardDict[card] >= cardsOnTop[1] and (card > cardsOnTop[0] or (card == 2 and cardsOnTop[0] != 2)): 
                    self.cardDict[card] -= cardsOnTop[1]
                    return [card, cardsOnTop[1]]
                   
                # if it has not returned by now then it needs to pass
        return ['pass']

    def start(self):

        # checks if they are out
        self.totalCards = 0
        for card in self.cardDict:
            self.totalCards += self.cardDict[card]
        if self.totalCards == 0:
            return ['out']

        # loops through card forward
        for card in self.cardDict:
            # checks the first card that isn't a two or three and plays all of it
            if card > 2 and self.cardDict[card] > 0:
                amountOfCard = self.cardDict[card]
                self.cardDict[card] -= self.cardDict[card]
                return [card, amountOfCard]

        if self.cardDict[2] > 0:
            self.cardDict[2] -= 1
            return [2, 1]

        print(self.name + ": Error: start() didn't return?")

    def checkIfGuaranteedOut(self):
        # check if the person can go out guaranteed by playing a two
        if self.onlyOneTrick() and self.cardDict[2] > 0:
            return True
        else:
            return False

    def onlyOneTrick(self):
        # checks if the person has only one type of trick left
        numberOfTricks = 0
        for card in self.cardDict:
            if card > 3 and self.cardDict[card] > 0:
                numberOfTricks += 1
        if numberOfTricks == 1:
            return True
        else:
            return False

    def giveLowestCard(self):
        # removes and returns the worst card the players hand
        for card in self.cardDict:
            # checks if the card is a single lower than a 9
            if card > 3 and self.cardDict[card] == 1 and self.cardDict[card] < 9:
                # note -- the number 9 in the if statement above was chosen because of millions of testing games
                self.cardDict[card] -= 1
                return card
        # second loop in-case first didn't return (if they only have pairs lower than 9)
        for card in self.cardDict:
            if card > 3 and self.cardDict[card] > 0:
                self.cardDict[card] -= 1
                return card

    def giveHighestCard(self):
        # removes and returns the highest card in the players hand
        # checks for twos
        if self.cardDict[2] > 0:
            self.cardDict[2] -= 1
            return 2
        # checks for threes
        if self.cardDict[3] > 0:
            self.cardDict[3] -= 1
            return 3
        # loops through dict to find next highest card
        # cant loop through dict reversed so i made a list of the cards (keys for the dict) at the top of this file
        for card in reversed(values):
            if self.cardDict[card] > 0:
                self.cardDict[card] -= 1
                return card

    def anti(self):
        # returns a card to anti
        cardsToAnti = []
        for card in self.cardDict:
            if card > 3 and self.cardDict[card] == 1 and card <= 8:
                self.cardDict[card] -= 1
                cardsToAnti.append(card)
        return cardsToAnti
