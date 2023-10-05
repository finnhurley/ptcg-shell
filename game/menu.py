import os
from .deck import *
from .player import *
from .recipe import *
from .game import *


class Menu:
    def __init__(self):
        self.p1 = Player("Player 1", defaultDeck())
        self.p2 = Player("Player 2", defaultDeck())
        self.decks = decks()
        self.g = Game(self.p1, self.p2)

    def open(self):
        self.mainmenu()
    
    def mainmenu(self):
        viewingMenu = True
        while viewingMenu:
            refreshScreen()
            if (self.g.winner is not None): self.resetWinner()
            banner()
            options()
            option = input("\nSelect Menu Option By Number: ")
            if (option == "1"):
                self.g.start()
            if (option == "2"):
                self.editPlayer()
            if (option == "3"):
                self.editOpponent()
            if (option == "4"):
                self.viewAbout()
            if (option == "5"):
                refreshScreen()
                option = input("Are you sure you want to exit? y/n: ")
                if (option == "y"): viewingMenu = False

    def editPlayer(self):
        viewingPage = True
        while viewingPage:
            refreshScreen()
            print("Name: %s     | Deck: %s" % (self.p1.name, self.p1.deck.name))
            option = input("1. Edit Name     2. Select Deck      3. Exit    : ")
            if (option == "1"):
                newName = input("Enter New Name: ")
                self.p1.name = newName
            if (option == "2"):
                self.selectDeck(self.p1)
            if (option == "3"):
                viewingPage = False
    
    def selectDeck(self, player):
        selectingDeck = True
        deckList = self.decks
        while selectingDeck:
            ("\n\n")
            options = 0
            for deck in deckList:
                options += 1
                print("%d. %s" % (options, deck.name))
            input("\nSelect Deck: ")
            if ((options-1) in range(len(deckList))):
                player.deck = deckList[options-1]
                selectingDeck = False

    def editOpponent(self):
        viewingPage = True
        while viewingPage:
            refreshScreen()
            print("Name: %s     | Deck: %s" % (self.p2.name, self.p2.deck.name))
            option = input("1. Edit Name     2. Select Deck      3. Exit    : ")
            if (option == "1"):
                newName = input("Enter New Name: ")
                self.p2.name = newName
            if (option == "2"):
                self.selectDeck(self.p2)
            if (option == "3"):
                viewingPage = False
    
    def viewAbout(self):
        refreshScreen()
        viewingAbout = True
        while viewingAbout:
            print("Description coming soon...")
            option = input("1. Exit")
            if (option == "1"):
                viewingAbout = False

    def resetWinner(self):
        print("%s is the winner!\n" % self.g.winner.name)
        self.g.winner = None


def defaultDeck():
    recipe = createRecipe("Decks/blazikendeck.json")
    return Deck("EX Master Trainer Deck - Blaziken", recipe)

#TODO: Make this dynamic
def decks():
    deckBox = []
    recipe = createRecipe("Decks/blazikendeck.json")
    deckBox.append(Deck("EX Master Trainer Deck - Blaziken", recipe))
    return deckBox


def banner():
    print("==========================")
    print("|        ptcg-shell      |")
    print("==========================")

def options():
        print("1. Battle")
        print("2. Edit Player")
        print("3. Edit Opponent")
        print("4. About")
        print("5. Exit")

def refreshScreen():
    os.system('cls||clear')
