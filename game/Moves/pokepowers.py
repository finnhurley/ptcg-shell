import sys 
sys.path.append('..')

from ..card import *
from ..actions import *

#Blaziken (ex Ruby and Sapphire) Firestarter
def blazikenFirestarter(player):
    fireEnergy = Card("Fire Energy", "Fire")
    discardPileEnergy = fromDiscardPile(player, fireEnergy)
    if (fireEnergy == discardPileEnergy):
        attachEnergy(selectOwnBenchedPokemon(), discardPileEnergy) 
    else:
        print("No Fire Energies found in %s's discard pile" % player.name)