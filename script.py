from player import *
from game import *
from decks_and_cards import *
from presRound import *
from randomPlayer import *
from worstPlayer import *
from noTwoPlayer import *
from twoerPlayer import *
from personInputPlayer import *
from oldPlayer import *

# example scripts to play some games

# print("-----------------------below is normal bots just playing one game")
#game1 = Game(4, 'game1', 10000, 'none', 1, Player, True, POMDP, 0)

#below is a game with 3 normal bots and a random bot
game1 = Game(4, 'game1', 10000, 'none', 1, Player, True, Random, 1)

#below is a game with 3 normal bots and the pomdp bot
#game1 = Game(4, 'game1', 1000, 'none', 1, Player, True, POMDP, 1)
game1.startGame()
#
# print("-----------------------below is passing two with a person playing against 3 bots")
# game2 = Game(4, 'game2', 10, 'two', 1, Player, True, PlayerInputPlayer, 1)
# game2.startGame()
#
# print("-----------------------below is bots passing one")
# game3 = Game(4, 'game3', 10000, 'one', 1, Player)
# game3.startGame()
#
# print("-----------------------below is normal bots compared to a player playing random (playable) cards")
# game4 = Game(4, 'game4', 10000, 'two', 1, Player, False, RandomPlayer, 1)
# game4.startGame()
#
# print("-----------------------below is normal bots compared to the worst bot I could make (other than just passing)")
# game5 = Game(4, 'game5', 10000, 'two', 1, Player, False, WorstPlayer, 1)
# game5.startGame()
#
# print("-----------------------below is normal bots compared to a bot that plays twos VERY aggressively")
# game6 = Game(4, 'game6', 10000, 'two', 1, Player, False, TwoerPlayer, 1)
# game6.startGame()
#
# print("-----------------------below is normal bots compared to a bot that doesn't use twos (unless its their last card)")
# game7 = Game(4, 'game7', 10000, 'two', 1, Player, False, NoTwoPlayer, 1)
# game7.startGame()
#
# print("-----------------------below is just for testing new player objects")
# game8 = Game(4, 'game8', 5, 'two', 1, Player, True, OldPlayer, 1, True)
# game8.startGame()
#
# print("-----------------------below is one deck")
# game9 = Game(4, 'game9', 20000, 'two', 1, Player, False)
# game9.startGame()
#
# print("-----------------------below is two decks")
# game10 = Game(4, 'game10', 10000, 'two', 2, Player, False)
# game10.startGame()
#
# testDict = {}
# for i in range(4,14):
#     game11 = Game(4, 'game8', 100000, 'none', 1, Player, False, OldPlayer, 1, True, [i, i - 1])
#     game12 = Game(4, 'game8', 100000, 'none', 1, Player, False, OldPlayer, 1, True, [i, i + 1])
#     testDict[i, i - 1] = game11.startGame()
#     testDict[i, i + 1] = game12.startGame()
#
# print(testDict)
