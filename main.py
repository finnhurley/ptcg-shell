from game.card import *
from game.deck import *
from game.player import *
from game.recipe import *


#quick test that creates a deck, sets up a players board and see's if cards are being added to the correct places
recipe = createRecipe("Decks/blazikendeck.json")
blazikenDeck = Deck("BlazikenDeck", recipe)
p1 = Player("Player 1", blazikenDeck)
p1.setUpBoard()
print("Prize Cards:", len(p1.prizes))
print(p1.showHand())

for card in p1.hand:
    if ("Pokemon" in str(type(card))):
        card.viewCard()