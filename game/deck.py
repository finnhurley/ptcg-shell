import random

class Deck:
    #Deck constructor takes a deck name and a recipe (a list of Card classes)
    def __init__(self, name, recipe):
        self.cards = []
        self.name = name
        for pkmncard in recipe:
            self.addCard(pkmncard)
    
    #Adds a specified card to the card list
    def addCard(self, card):
        self.cards.append(card)

    #Pop's and returns the top card of the deck to simulate a draw
    def drawCard(self):
        card = self.cards.pop(0)
        return card

    #Randomizes the order of the cards in the list to simulate a shuffle
    def shuffle(self):
        random.shuffle(self.cards)

    #prints the contents of a deck
    def showDeck(self):
        for card in self.cards:
            print(card.name)

    #confirms a deck is comprised of exactly 60 cards and doesn't contain more than 4 copies of a card
    def isLegit(self):
        if (len(self.cards) != 60):
            return False   
        for card in self.cards:
            if (self.countCard(card.name) > 4):
                return False
        return True
    
    #counts the quantity of a specified card in the deck, used in the isLegit function
    def countCard(self, cardName):
        count = 0
        for card in self.cards:
            if (card.name == cardName):
                count += 1
        return count
