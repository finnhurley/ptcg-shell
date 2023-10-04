from .deck import *
from .card import *

class Player:

    #Constructor takes a player name and a deck to use
    def __init__(self, name, deck):
        self.name = name
        self.deck = deck
        self.prizes = []
        self.hand = []
        self.active = []
        self.bench = []
        self.discardPile = []
        self.supporterFlag = False

    #Shuffles the player's deck, sets up prize cards and hand
    def setUpBoard(self):
        self.deck.shuffle()

        for i in range(6):
            self.prizes.append(self.deck.drawCard())

        for i in range(7):
            self.hand.append(self.deck.drawCard())

        validHand = self.isValidHand()
        if validHand is False:
            while validHand is False:
                print("Invalid Hand. Performing Mulligan...")
                self.mulligan()
                validHand = self.isValidHand()
    
    #removes specified card from players hand, adds it to deck
    def returnHandToDeck(self):
        for card in self.hand:
            self.deck.cards.append(card)
        self.hand.clear()
        
    #checks to see if hand has any basic pokemon (used at start of game)
    def isValidHand(self):
        for card in self.hand:
            if (type(card).__name__ == "Pokemon"):
                if (card.stage == "Basic"):
                    return True
        return False
    
    #adds hand to deck, shuffles, then draws new hand
    def mulligan(self):
        handSize = len(self.hand)
        self.returnHandToDeck()
        self.deck.shuffle()
        for i in range(7):
            self.hand.append(self.deck.drawCard())

    #returns the contents of a players hand as a string
    def showHand(self):
        hand = "Hand: "
        for card in self.hand:
            hand += card.name + ", "
        return hand
    
    #getter for Active Pokemon, returns card object
    def activePokemon(self):
        return self.active[0]
    
    #getter for a specified pokemon on the bench, returns card object
    def benchPokemon(self, pokemonName):
        for pokemon in self.bench:
            if (pokemon.name == pokemonName):
                return pokemon
    
    #returns a string array of pokemon names on the players bench
    def showBenchedPokemon(self):
        nameList = []
        for pokemon in self.bench:
            nameList.append(pokemon.name)
        return nameList