from collections import defaultdict
import random
import math

class POMDP(object):
    #Reward is set as (number of cards played) * (1 if the trick was lost, 10 if the trick was won)
    #Number of actions calculated by number of card combinations that can be played
    def __init__(self, name, N = defaultdict(lambda: 0), Q = defaultdict(lambda: 0)):
        self.name = name
        self.cardDict = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}
        self.hand = []
        self.notInHand = {2: 4, 3: 4, 4: 4, 5: 4, 6: 4, 7: 4, 8: 4, 9: 4, 10: 4, 11: 4, 12: 4, 13: 4, 14: 4}
        self.numSimulations = 20
        self.simulationDepth = 5
        self.N = N
        self.Q = Q
        self.c = 0.3
        self.U = defaultdict(lambda: 0)

    def resetPlayer(self):
        self.hand = []
        self.cardDict = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}

    def draw(self, deck, numCards):
        for i in range(numCards):
            newCard = deck.draw()
            self.hand.append(newCard)
            self.cardDict[newCard.value] += 1
            self.notInHand[newCard.value] -= 1

    def sortHand(self):
        pass

    # 0 = pass
    def availableActions(self, currentPlay):
        #TODO: debug to check for currentPlay length first
        actions = [[0]]
        numThrees = self.cardDict[3]
        numCards = currentPlay[1]
        if len(currentPlay) > 2:
            numCards += currentPlay[3]
        cardValue = len(currentPlay) == 0? 1:currentPlay[0]

        for card in cardDict:
            if card == 2 and cardDict[card] > 0:
                actions.append([2])
                continue
            if card == 3 and cardDict[card] > numCards:
                actions.append([3] * numCards)
            if card >= cardValue:
                for i in range(min(numThrees, numCards) + 1):
                    if cardDict[card] + i >= numCards:
                        newAction = []
                        if i == 0:
                            newAction.append([card] * numCards)
                            continue
                        newAction.append([3] * i + [card] * (numCards - i))
    
    def bonus(self, history, a, Nh):
        Nha = self.N[(history, a)]
        if Nha == 0: return float('inf')
        return math.sqrt(math.log(Nh)/Nha)
    
    def explore(self, history, currentPlay):
        Nh = self.N[(history, [-1])]
        actions = self.availableActions(currentPlay)
        max_score = -1
        best_a = None
        for a in actions:
            score = self.Q[(history, a)] + self.c*self.bonus(history, a, Nh)
            if score > max_score:
                max_score = score
                best_a = a
        return best_a, max_score

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

    def basicPlayerTurn(self, currentPlay, hand): 
        # checks if they are out
        totalCards = 0
        for card in hand:
            totalCards += hand[card]
        if totalCards == 0:
            return ['out']

        # checks if they only have twos and one other trick
        if self.checkIfGuaranteedOut():
            hand[2] -= 1
            return [2, 1]
           # loops through cardDict (goes forward so plays lowest possible first)
        for card in hand:
            # checks if its the same type of trick and if they have enough cards to play on the trick (at least one)
            if hand[card] + hand[3] >= currentPlay[1] and hand[card] > 0:
                # checks if the card is playable and not a two or three
                # (shouldn't be possible to be a two or three cuz it should be a four or higher)
                if card >= currentPlay[0] and card > 3:
                    # checks to see if you have enough of the card to play without threes (won't break up larger sets)
                    if hand[card] - currentPlay[1] == 0:
                        hand[card] -= currentPlay[1]
                        return [card, currentPlay[1]]
                    # this says it is ok to break up larger pairs if it is for matching or if its a high card
                    elif hand[card] - currentPlay[1] > 0 and (card == currentPlay[0] or card >= 10):
                        # note -- the value 10 in the if statement above was determined by testing different values through many millions of games
                        hand[card] -= currentPlay[1]
                        return [card, currentPlay[1]]
                    # if you don't have enough without threes, plays what you do have as well as threes, but not if its matching
                    elif card != currentPlay[0] and currentPlay[1] > 1 and hand[card] < currentPlay[1]:
                        threesUsed = currentPlay[1] - hand[card]
                        hand[3] -= currentPlay[1] - hand[card]
                        # should always set it to 0
                        hand[card] -= currentPlay[1] - threesUsed
                        self.checkIfAnyNegatives()
                        return [card, currentPlay[1], "Threes used:", threesUsed]

        # if it gets to here then it has nothing to play other than 2's and 3's

        # checks if it has 2's to play
        if hand[2] > 0:
            hand[2] -= 1
            return [2, 1]
        # checks if it has enough 3's to play as aces
        if currentPlay[0] < 14 and hand[3] >= currentPlay[1]:
            hand[3] -= currentPlay[1]
            return [14, currentPlay[1], "Threes used:", currentPlay[1]]

        # if it has not returned by now then it needs to pass
        return ['pass']

    def sampleS(self, numOtherCards, notHand):
        player1 = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}
        player2 = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}
        player3 = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}

        notHandArray = []
        #deal cards randomly to players
        for cardValue in notHand:
            for cardNumber in range(notHand[cardValue]):
                notHandArray.append(cardValue)

        random.shuffle(notHandArray)
        index = 0
        for i in range(numOtherCards[0]):
            player1[notHandArray[index]] += 1
            index += 1

        for i in range(numOtherCards[1]):
            player2[notHandArray[index]] += 1
            index += 1

        for i in range(numOtherCards[2]):
            player3[notHandArray[index]] += 1
            index += 1

        return player1, player2, player3




    def TRO(self, notHand, numOtherCards, a):
        #generate hands for each of the other players
        player1, player2, player3 = sampleS(numOtherCards, notHand)

        #simulate one round for each of the other players given their hands

            #update notInHand based on what simulation plays

       #return notHand, reward
    
    def simulate(self, notHand, h, d, currentPlay, numOtherCards):
        if d <= 0:
            return self.U[s]
        a, score = self.explore(h, currentPlay)
        if score == 0:
            return self.U[s]
        #finish based on algorithm in book

    def updateNotHand(self, currentPlay):
        self.notInHand[currentPlay[0]] -= currentPlay[1]
        if len(currentPlay) > 2:
            self.notInHand[3] -= currentPlay[3]

    def start(self):
        #play with CurrentPlay = []

    def play(self, currentPlay):
        #play
