import random

class attack:
    def __init__(self, name, cost, damage, effect):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.effect = effect

#adds a specified card to a player hand
def addCardToHand(card, player):
    player.hand.append(card)

#Attaches an energy to a selected pokemon
def attachEnergy(energy, pokemon):
    pokemon.energies.add(energy)

#Checks if a specified card exists in a players hand, returns boolean
def isCardInHand(card, player):
    for c in player.hand:
        if (c.name == card.name):
            return True
    return False

#Checks if a specified card exists in a players discard pile, returns boolean
def isCardInDiscardPile(card, player):
    for c in player.discardPile:
        if (c.name == card.name):
            return True
    return False

#Checks if a specified card exists on a players bench, returns boolean
def isCardInDiscardPile(card, player):
    for c in player.bench:
        if (c.name == card.name):
            return True
    return False

#Checks if a specified card is a players active pokemon, returns boolean
def isCardActivePokemon(card, player):
    for c in player.active:
        if (c.name == card.name):
            return True
    return False

#Removes an energy from a selected pokemon and returns it as a Card
def detachEnergy(energyType, pokemon):
    if energyExists(energyType, pokemon) is True:
        for i in range (len(pokemon.energies)):
            if (pokemon.energies[i] == energyType):
                energyCard = pokemon.energies[i]
                pokemon.energies.remove(pokemon.energies[i])
                return energyCard

#Checks if an energy is attached to a pokemon, returns boolean
def energyExists(energyType, pokemon):
    for energy in pokemon.energies:
        if (energyType == energy.energyType):
            return True
    return False

#simulates a coin toss, returns the value Heads or Tails as a string
def coinToss():
    if (random.randint(0, 1) == 0):
        return "Tails" 
    else:
        return "Heads"
    
#knocks out a pokemon, removes all card attached to it from pokemon
def knockOutPokemon(pokemon, player):
    return
    
#removes a specified card from a player's hand, returns card object if successful
def removeCardFromHand(card, player):
    if (isCardInHand(card, player) is True):
        for i in range(len(player.hand)):
            if (player.hand[i].name == card.name):
                player.hand.remove(player.hand[i])
                return card
    
#removes a card from discard pile, returns card object if successful
def fromDiscardPile(card, player):
    if (isCardInDiscardPile(card, player) is True):
        for i in range(len(player.discardPile)):
            if (player.discardPile[i].name == card.name):
                player.discardPile.remove(player.discardPile[i])
                return card
    

#adds a card to the players discard pile
def toDiscardPile(card, player):
    player.discardPile.append(card)