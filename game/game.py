import os
from .player import *
from .card import *
from .deck import *
from .actions import *

class Game:
    def __init__(self, player1, player2):
        self.p1, self.p2 = player1, player2
        self.winner = None

    #Performs the coin tosses, sets up the decks and runs the game
    def start(self):
        first, second = self.setUpGame(self.p1, self.p2)
        self.runGame(first, second)

    #Performs a coin toss to see which player will go first
    def setUpGame(self, player1, player2):
        if (coinToss() == "Heads"):
            first = player1
            second = player2
        else:
            first = player2
            second = player1
        return first, second
    
    #Sets up the decks, prize card and starting hands, then runs the game until someone wins
    def runGame(self, first, second):
        first.setUpBoard()
        second.setUpBoard()
        selectStartingActivePokemon(first)
        selectStartingActivePokemon(second)
        while self.winner == None:
            self.turn(first, second)
            if (self.winner == None):
                self.turn(second, first)
        print("%s Wins!!!!" % self.winner)


    #The base process of a turn
    def turn(self, player, opponent):
        self.refreshScreen()
        isTurn = True
        addCardToHand(player.deck.drawCard(), player)
        while isTurn:
            self.turnBanner(player)
            options = "1. View Hand     2. View Active     3. View Bench     4. Stats    5. End Turn    : "
            print("\nWhat will %s do?" % player.name)
            playerMove = input(options)
            self.refreshScreen()
            if (playerMove == "1"):
                self.viewHand(player, opponent)
            if (playerMove == "2"):
                self.viewActive(player, opponent)
            if (playerMove == "3"):
                self.viewBench(player, opponent)
            if (playerMove == "4"):
                self.viewGameStats(player, opponent)
            if (playerMove == "5"):
                isTurn = False
            if (playerMove == "FF" or playerMove == "ff"):
                ff = input("\nAre you sure you want to forfeit? (y/n): ")
                if (ff == "y"):
                    self.winner = opponent.name
                    isTurn = False
        self.endTurn(player)

    #Viewing a players hand presents the player with more options
    def viewHand(self, player, opponent):
        self.refreshScreen()
        viewingHand = True
        optionList = []
        while viewingHand:
            optionNo = 0
            for card in player.hand:
                optionNo += 1
                optionList.append(card)
                print("%d. %s [%s]" % (optionNo, card.name, card.cardType))
            optionNo += 1
            print("%s. Back" % optionNo)
            playerMove = input("Select a card: ")
            if (playerMove == str(optionNo)):
                return
            if (int(playerMove) in range(len(optionList))):
                self.viewCardInHand(player, opponent, optionList[int(playerMove)-1])

    #Viewing a card in the players hand presents the player with a unique option depending on the card
    def viewCardInHand(self, player, opponent, card):
        viewingCard = True
        card = card
        while viewingCard:
            card.viewCard()
            if (card.cardType == "Pokemon"):
                if (card.stage == "Basic"):
                    option = "Bench"
                else:
                    option = "Evolve"
            if (card.cardType == "Trainer" or card.cardType == "Supporter"):
                option = "Use"
            if (card.cardType == "Energy"):
                option = "Attach"
            print("1. %s    2. Back" % option)
            playerMove = input("Select option: ")
            self.refreshScreen()
            if (playerMove == "1"):
                if (card.cardType == "Pokemon" and card.cardType == "Basic"): print("bench")
                if (card.cardType == "Pokemon" and card.cardType != "Basic"): print("evolve")
                if (card.cardType == "Trainer" or card.cardType == "Supporter"): print("use trainer/supporter")
                if (card.cardType == "Energy"): print("attach energy")
            if (playerMove == "2"):
                return

    #viewing the active pokemon presents the player with more options
    def viewActive(self, player, opponent):
        viewingActive = True
        poke = player.activePokemon()
        EnergyList = []
        for energy in poke.energies:
            EnergyList.append(energy.energyType)
        while viewingActive:
            poke.viewCard()
            print("EnergyList: ", EnergyList)
            print("Remaining HP: %d (%d Damage Counters)" % (poke.getRemainingHP(), poke.damageCounters))
            print("\nWhat will %s do?" % poke.name)
            playerMove = input("\n1. Attack    2. Retreat    3. Back    : ")
            self.refreshScreen()
            if (playerMove == "1"):
                print("\n attacks coming soon!")
            if (playerMove == "2"):
                if (poke.canRetreat()):
                    print("\n%s return!" % poke.name)
                    return
                else:
                    print("\n%s can't retreat! Not enough energies.\n" % poke.name)
            if (playerMove == "3"):
                return

    #Viewing the bench presents the player with more options
    def viewBench(self, player):
        return

    #Prints the number of cards in the players hand, prizes and deck so each player can gauge progress  
    def viewGameStats(self, p1, p2):
        print("%s:      Hand: %d      Prize Cards: %d      Deck: %d" % (p1.name, len(p1.hand), len(p1.prizes), len(p1.deck.cards)))
        print("%s:      Hand: %d      Prize Cards: %d      Deck: %d" % (p2.name, len(p2.hand), len(p2.prizes), len(p2.deck.cards)))

    #does all the turn ending checks like status conditions etc.
    def endTurn(self, player):
        if (self.winner is not None):
            return
        if (player.activePokemon().isBurned):
            poisonPokemon(player.activePokemon())
        if (player.activePokemon().isBurned):
            burnPokemon(player.activePokemon())
        if (player.activePokemon().statusCondition == "Asleep"):
            sleepCheck(player.activePokemon())
        if (player.activePokemon().statusCondition == "Paralyzed"):
            cureStatus(player.activePokemon())

    def refreshScreen(self):
        os.system('cls||clear')

    def turnBanner(self, player):
        print("--------------------")
        print("%s's Turn" % player.name)
        print("--------------------")
