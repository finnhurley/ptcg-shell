from game.card import *
from game.deck import *
from game.player import *
from game.recipe import *
from game.move import *
from game.actions import *
from game.game import *


#quick test that sets up a board to test some functions with
recipe = createRecipe("Decks/blazikendeck.json")
blazikenDeck = Deck("BlazikenDeck", recipe)
p1 = Player("Player 1", blazikenDeck)
p2 = Player("Player 2", blazikenDeck)
g = Game(p1, p2)
g.start()


#print("Prize Cards:", len(p1.prizes))
#print(p1.showHand())

#print("\n\n")
#selectedCard = selectOwnPokemon(p1)
#selectedCard = selectPokemonFromDeck(p1)
#selectedCard.viewCard()