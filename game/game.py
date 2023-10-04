from .player import *
from .card import *
from .deck import *
from .actions import *

class Game:
    def __init__(self, player1, player2):
        self.p1, self.p2 = player1, player2
        self.winner = None

    def start(self):
        first, second = self.setUpGame(self.p1, self.p2)
        self.runGame(first, second)

    def setUpGame(self, player1, player2):
        player1.setUpBoard()
        player2.setUpBoard()
        if (coinToss() == "Heads"):
            first = player1
            second = player2
        else:
            first = player2
            second = player1
        return first, second
    
    def runGame(self, first, second):
        selectStartingActivePokemon(first)
        selectStartingActivePokemon(second)
        while self.winner == None:
            self.turn(first, second)
            if (self.winner == None):
                self.turn(second, first)
        print("%s Wins!!!!" % self.winner)


    def turn(self, player, opponent):
        print("--------------------")
        print("%s's Turn" % player.name)
        print("--------------------")
        isTurn = True
        player.deck.drawCard()
        while isTurn:
            options = "\n1. View Hand     2. View Active     3. View Bench     4. Stats    5. End Turn    : "
            print("\n\nWhat will %s do?" % player.name)
            playerMove = input(options)
            if (playerMove == "1"):
                self.viewHand(player)
            if (playerMove == "2"):
                self.viewActive(player)
            if (playerMove == "3"):
                self.viewBench(player)
            if (playerMove == "4"):
                self.viewGameStats(player, opponent)
            if (playerMove == "5"):
                isTurn = False
            if (playerMove == "FF"):
                ff = input("\nAre you sure you want to forfeit? (y/n): ")
                if (ff == "y"):
                    self.winner = opponent.name
                    isTurn = False
        self.endTurn(player)

    def viewHand(self, player):
        return
    
    def viewActive(self, player, opponent):
        poke = player.activePokemon()
        poke.viewCard()
        EnergyList = []
        for energy in poke.energies:
            EnergyList.append(energy.energyType)
        print("EnergyList: ", EnergyList)
        print("Remaining HP: %d (%d Damage Counters)" % poke.getRemainingHP(), poke.damageCounters)

    def viewBench(self, player):
        return
    
    def viewGameStats(self, p1, p2):
        print("%s:      Hand: %d      Prize Cards: %d      Deck: %d" % (p1.name, len(p1.hand), len(p1.prizes), len(p1.deck.cards)))
        print("%s:      Hand: %d      Prize Cards: %d      Deck: %d" % (p2.name, len(p2.hand), len(p2.prizes), len(p2.deck.cards)))

    #does all the turn ending checks like status conditions etc.
    def endTurn(self, player):
        if (player.activePokemon().isBurned):
            poisonPokemon(player.activePokemon())
        if (player.activePokemon().isBurned):
            burnPokemon(player.activePokemon())
        if (player.activePokemon().statusCondition == "Asleep"):
            sleepCheck(player.activePokemon())
        if (player.activePokemon().statusCondition == "Paralyzed"):
            cureStatus(player.activePokemon())