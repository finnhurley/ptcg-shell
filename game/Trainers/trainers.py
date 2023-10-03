from ..actions import *

#Celio's Network (EX Fire Red and Leaf Green)
def celiosNetwork(player):
    player.supporterFlag = False
    player.hand.append(selectPokemonFromDeck(player))