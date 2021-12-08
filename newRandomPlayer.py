from collections import defaultdict
import random
import math

class Random(object):
    #Reward is set as (number of cards played) * (1 if the trick was lost, 10 if the trick was won)
    #Number of actions calculated by number of card combinations that can be played
    def __init__(self, name):
        self.name = name
        self.cardDict = {3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
        self.hand = []

    def resetPlayer(self):
        self.hand = []
        self.cardDict = {3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
 
    def draw(self, deck, numCards):
        for i in range(numCards):
            newCard = deck.draw()
            self.hand.append(newCard)
            if newCard.value == 2:
                newCard.value = 15
            self.cardDict[newCard.value] += 1

    def sortHand(self):
        pass

    def showHand(self):
        return self.hand

    # 0 = pass
    def availableActions(self, currentPlay, cardDict):
        actions = []
        cardValue = currentPlay[0]
        numCards = currentPlay[1]

        for card in cardDict:
            if card > cardValue and cardDict[card] >= numCards:
                actions.append([card, numCards])
        if cardValue != 1:
            actions.append([0])
        return actions
    
    def start(self):
        totalCards = 0
        for card in self.cardDict:
            totalCards += self.cardDict[card]

        if totalCards == 0:
            return ['out']

        cardValue = random.randint(3, 15)
        while self.cardDict[cardValue] == 0:
            cardValue = random.randint(3, 15)

        amount = random.randrange(1, self.cardDict[cardValue] + 1)
        self.cardDict[cardValue] -= amount
        if cardValue == 15:
            cardValue = 2
        return [cardValue, amount]



    def play(self, topCards):
        currentPlay = topCards.copy()
        if currentPlay[0] == 2:
            currentPlay[0] = 15

        totalCards = 0
        for card in self.cardDict:
            totalCards += self.cardDict[card]

        if totalCards == 0:
            return ['out']

        actions = self.availableActions(currentPlay, self.cardDict)
        action = random.choice(actions)
        if action[0] == 15:
            action[0] = 2
        if action == [0]:
            action = ['pass']
        return action

