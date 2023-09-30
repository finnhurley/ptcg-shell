from .deck import *
from .card import *

class Player:
    prizes = []
    hand = []
    active = []
    bench = []
    discardPile = []

    #Constructor takes a player name and a deck to use
    def __init__(self, name, deck):
        self.name = name
        self.deck = deck        

    #Shuffles the player's deck, sets up prize cards and hand
    def setUpBoard(self):
        self.deck.shuffle()

        for i in range(6):
            self.prizes.append(self.deck.drawCard())

        for i in range(7):
            self.hand.append(self.deck.drawCard())

        mullyCount = 0
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