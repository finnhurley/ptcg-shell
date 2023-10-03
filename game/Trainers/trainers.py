import sys
sys.path.append('')
from actions import *

#Celio's Network (EX Fire Red and Leaf Green)
def celiosNetwork(player):
    player.hand.append(selectPokemonFromDeck(player))

#Life Herb (EX Hidden Legends)
def lifeHerb(player):
    if(coinToss == "Heads"):
        pokemon = selectOwnPokemon(player)
        if (pokemon.damageCounters < 6):
            pokemon.damageCounters = 0
        else:
            pokemon.damageCounters -= 6
        pokemon.isBurned = False
        pokemon.isPoisoned = False
        pokemon.statusCondition = None

#Professor Birch (EX Ruby and Sapphire)
def professorBirch(player):
    while len(player.hand) < 6:
        player.hand.append(player.deck.drawCard())

#Energy Search (EX Ruby and Sapphire)
def energySearch(player):
    player.hand.append(selectEnergyFromDeck(player))

#Switch (EX Ruby and Sapphire)
def switch(player):
    active = player.activePokemon()
    benched = selectOwnBenchedPokemon(player)
    active, benched = benched, active