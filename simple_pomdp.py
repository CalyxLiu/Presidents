from collections import defaultdict
import random
import math

class POMDP(object):
    #Reward is set as (number of cards played) * (1 if the trick was lost, 10 if the trick was won)
    #Number of actions calculated by number of card combinations that can be played
    def __init__(self, name, N = defaultdict(lambda: 0), Q = defaultdict(lambda: 0)):
        self.name = name
        self.cardDict = {3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
        self.hand = []
        self.notInHand = {3: 4, 4: 4, 5: 4, 6: 4, 7: 4, 8: 4, 9: 4, 10: 4, 11: 4, 12: 4, 13: 4, 14: 4, 15: 4}
        #v1 = 20
        self.numSimulations = 50
        self.simulationDepth = 5
        self.N = N
        self.Q = Q
        #v1 = 0.3
        self.c = 0.3
        self.U = defaultdict(lambda: 0)
        #v1 = 0.8
        self.gamma = 0.9
        self.h = ""
        self.numOtherCards = [13, 13, 13]

    def resetPlayer(self):
        self.hand = []
        self.h = ""
        self.cardDict = {3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
        self.notInHand = {3: 4, 4: 4, 5: 4, 6: 4, 7: 4, 8: 4, 9: 4, 10: 4, 11: 4, 12: 4, 13: 4, 14: 4, 15: 4}
        self.numOtherCards = [13, 13, 13]

    def draw(self, deck, numCards):
        for i in range(numCards):
            newCard = deck.draw()
            self.hand.append(newCard)
            if newCard.value == 2:
                newCard.value = 15
            self.cardDict[newCard.value] += 1
            self.notInHand[newCard.value] -= 1

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
    
    def bonus(self, history, a, Nh):
        Nha = self.N[(history, str(a))]
        if Nha == 0: return float('inf')
        return math.sqrt(math.log(Nh)/Nha)
    
    def explore(self, history, currentPlay, cardDict):
        Nh = self.N[(history, '-1')]
        actions = self.availableActions(currentPlay, cardDict)
        max_score = -1
        best_a = None
        for a in actions:
            score = self.Q[(history, str(a))] + self.c*self.bonus(history, a, Nh)
        #    print(f"Action: {a} Score: {score}")
            if score > max_score:
                max_score = score
                best_a = a
#        print(f"Actions: {actions} Best: {best_a} Cards: {cardDict}")
        if len(best_a) > 1:
            cardDict[best_a[0]] -= best_a[1]
        return best_a, max_score

    def basicPlayerTurn(self, currentPlay, hand): 
        # checks if they are out
        totalCards = 0
        for card in hand:
            totalCards += hand[card]
        if totalCards == 0:
            return ['out']
        #print(f"Basic turn: {currentPlay}")

           # loops through cardDict (goes forward so plays lowest possible first)
        for card in hand:
            # checks if its the same type of trick and if they have enough cards to play on the trick (at least one)
            if card > currentPlay[0] and hand[card] >= currentPlay[1]:
                return [card, currentPlay[1]]

        # if it has not returned by now then it needs to pass
        return ['pass']

    def sampleS(self, numOtherCards, notHand):
        player1 = {3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
        player2 = {3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
        player3 = {3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}

        notHandArray = []
        #deal cards randomly to players
        for cardValue in notHand:
            for cardNumber in range(notHand[cardValue]):
                notHandArray.append(cardValue)

        random.shuffle(notHandArray)
        index = 0
        
        if(numOtherCards[0] > 0):
            for i in range(numOtherCards[0]):
                player1[notHandArray[index]] += 1
                index += 1

        if(numOtherCards[1] > 0):
            for i in range(numOtherCards[1]):
                player2[notHandArray[index]] += 1
                index += 1

        if(numOtherCards[2] > 0):
            for i in range(numOtherCards[2]):
                player3[notHandArray[index]] += 1
                index += 1

        return player1, player2, player3




    def TRO(self, player1, player2, player3, notHand, numOtherCards, a, cardDict):
        totalCards = 0
        for card in cardDict:
            totalCards += cardDict[card]

        if totalCards == 0:
            return 1000, a

        #generate hands for each of the other players
        oldPlay = a

        #simulate one round for each of the other players given their hands
        currentPlay = self.basicPlayerTurn(a, player1)
        if len(currentPlay) > 1:
            notHand[currentPlay[0]] -= currentPlay[1] 
            numOtherCards[0] -= currentPlay[1]
        else:
            currentPlay = oldPlay

        oldPlay = currentPlay
        currentPlay = self.basicPlayerTurn(currentPlay, player2)
        if len(currentPlay) > 1:
            notHand[currentPlay[0]] -= currentPlay[1]
            numOtherCards[1] -= currentPlay[1]
        else:
            currentPlay = oldPlay

        oldPlay = currentPlay
        currentPlay = self.basicPlayerTurn(currentPlay, player3)
        if len(currentPlay) > 1:
            notHand[currentPlay[0]] -= currentPlay[1]
            numOtherCards[2] -= currentPlay[1]
        else:
            currentPlay = oldPlay
        
        #print(f"TRO: {currentPlay}")
        reward = a[1]
        if a == currentPlay:
            reward = reward * 10

        return reward, currentPlay
    
    def simulate(self, notHand, h, d, currentPlay, numOtherCards, cardDict):
        player1, player2, player3 = self.sampleS(numOtherCards, notHand)
        s = str(player1) + ";" + str(player2) + ";" + str(player3) + ";" + str(cardDict)

        totalCards = 0
        for card in cardDict:
            totalCards += cardDict[card]

        if totalCards == 0:
            return self.U[s]
        if d <= 0: 
            return self.U[s]
        a, score = self.explore(h, currentPlay.copy(), cardDict)
        if score == 0:
            return self.U[s]
        
        if a != [0]:
            reward, newPlay = self.TRO(player1, player2, player3, notHand, numOtherCards, a.copy(), cardDict)
        else:
            reward, newPlay = self.TRO(player1, player2, player3, notHand, numOtherCards, currentPlay.copy(), cardDict)

        if len(a) > 1:
            h = h + f"{a[0]}{a[1]};"
        else:
            h = h + "0;"

        if reward >= 1000:
            q = reward + self.gamma * self.simulate(notHand, h, 0, newPlay, numOtherCards, cardDict)
        else:
            q = reward + self.gamma * self.simulate(notHand, h, d - 1, newPlay, numOtherCards, cardDict)

        self.N[(h, '-1')] += 1
        self.N[(h, str(a))] += 1
        self.Q[(h, str(a))] += (q - self.Q[(h, str(a))])/self.N[(h, str(a))]
        return q
        

    def start(self):
        maxTrick = 0
        for card in self.cardDict:
            if self.cardDict[card] > maxTrick:
                maxTrick = self.cardDict[card]

        dictCopy = self.cardDict.copy()

#        print(f"max trick: {maxTrick} card dict: {self.cardDict}")
        option1 = self.play([1, 1])
        if(option1[0] == 2):
            option1[0] = 15

        self.cardDict = dictCopy.copy()
        
        option2, option3, option4 = None, None, None
        if maxTrick >= 2:
            option2 = self.play([1, 2])
            if(option2[0] == 2):
                option2[0] = 15
            self.cardDict = dictCopy.copy()
        
        if maxTrick >= 3:
            option3 = self.play([1, 3])
            if(option3[0] == 2):
                option3[0] = 15
            self.cardDict = dictCopy.copy()

        if maxTrick >= 4:
            option4 = self.play([1, 4])
            if(option4[0] == 2):
                option4[0] = 15
            self.cardDict = dictCopy.copy()

        best_option = (option1, self.Q[(self.h, str(option1))])

        if option2 != None and self.Q[(self.h, str(option2))] > best_option[1]:
            best_option = (option2, self.Q[(self.h, str(option2))])

            
        if option3 != None and self.Q[(self.h, str(option3))] > best_option[1]:
            best_option = (option3, self.Q[(self.h, str(option3))])
        if option4 != None and self.Q[(self.h, str(option4))] > best_option[1]:
            best_option = (option4, self.Q[(self.h, str(option4))])

        if(len(best_option[0]) > 1):
            self.cardDict[best_option[0][0]] -= best_option[0][1]
            self.h += f"{best_option[0][0]}{best_option[0][1]};"
        else:
            self.h += "0;"
        
        if best_option[0] == [0]:
            return ['pass']
        if best_option[0][0] == 15:
            best_option[0][0] = 2
        return best_option[0]




    def play(self, topCards):
        #print(f"Cards: {self.cardDict}")
#        print(f"Play: {currentPlay}")
        currentPlay = topCards.copy()
        if currentPlay[0] == 2:
            currentPlay[0] = 15

        totalCards = 0
        for card in self.cardDict:
            totalCards += self.cardDict[card]

        if totalCards == 0:
            return ['out']

        for i in range(self.numSimulations):
            self.simulate(self.notInHand.copy(), self.h, self.simulationDepth, currentPlay.copy(), self.numOtherCards.copy(), self.cardDict.copy())

        actions = self.availableActions(currentPlay, self.cardDict)
#        print(f"Play actions: {actions} Play: {currentPlay} Cards: {self.cardDict}")
        best_option = (actions[0], self.Q[(self.h, str(actions[0]))])
        for action in actions:
            q = self.Q[(self.h, str(action))]
            if q > best_option[1]:
                best_option = (action, q)

        if(len(best_option[0]) > 1):
            self.h = self.h + f"{best_option[0][0]}{best_option[0][1]};"
            self.cardDict[best_option[0][0]] -= best_option[0][1]
        else:
            self.h = self.h + "0;"

        if best_option[0] == [0]:
            return ['pass']
        if best_option[0][0] == 15:
            best_option[0][0] = 2
        return best_option[0]

    def updateNotHand(self, currentPlay, playerName):
#        print(type(playerName))
        play = currentPlay.copy()
        if playerName == 3:
            return

#        print(f"Not hand: {currentPlay} Player: {playerName}")

        if len(play) > 1:
            if play[0] == 2:
                play[0] = 15

            self.notInHand[play[0]] -= play[1]
            self.numOtherCards[playerName] -= play[1]
        
       # print(f"Not hand: {play} Player: {playerName}")
        
    def getNandQ(self):
        return self.N, self.Q
