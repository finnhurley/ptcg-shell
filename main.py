from game.card import *
from game.deck import *
from game.player import *
from game.recipe import *
from game.actions import *


#quick test that sets up a board to test some functions with
recipe = createRecipe("Decks/blazikendeck.json")
blazikenDeck = Deck("BlazikenDeck", recipe)
p1 = Player("Player 1", blazikenDeck)
p1.setUpBoard()
print("Prize Cards:", len(p1.prizes))
print(p1.showHand())


for card in p1.hand:
    if ("Pokemon" in str(type(card))):
        p1.active.append(removeCardFromHand(card, p1))
        break

toBench = []

for card in p1.hand:
    print("%s: %s" % (card.name, str(type(card))))
    if ("Pokemon" in str(type(card))):
        toBench.append(card)
        addToBench(card, p1)

for card in toBench:
    removeCardFromHand(card, p1)

print("\n\n")
selectedCard = selectOwnPokemon(p1)
selectedCard.viewCard()