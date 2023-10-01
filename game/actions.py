import random
from .card import *

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

#adds a card to the bench
def addToBench(pokemon, player):
    player.bench.append(pokemon)

#removes card from bench, returns card object
def removeFromBench(card, player):
    if isCardOnBench(card) is True:
        for i in range(len(player.bench)):
            if(player.bench[i].name == card.name):
                player.bench.remove(player.bench[i])
                return card

#sets a pokemon as active pokemon
def setActive(pokemon, player):
    player.active.append(pokemon)

#removes card from player's active spot, returns card object
def removeFromActive(pokemon, player):
    if isCardActivePokemon(pokemon) is True:
        for i in range(len(player.active)):
            if(player.active[i].name == card.name):
                player.active.remove(player.active[i])
                return pokemon

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
def isCardOnBench(card, player):
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


#does a check to see if a pokemon has enough damage counters to be knocked out. Returns boolean
def isKnockedOut(pokemon):
    if (pokemon.pokemonHp - pokemon.damageCounters <= 0):
        return True
    else:
        return False

#knocks out a pokemon, adds it and all attached cards to the discard pile
def knockOutPokemon(pokemon, player):
    if (isCardActivePokemon(pokemon, player) is True):
        for i in range(len(player.active)):
            if (player.active[i].name == pokemon.name):
                discard = player.active[i].name
                if (discard.previousStage != None):
                    while discard.previousStage != None:
                        toDiscardPile(discard, player)
                        discard = discard.previousStage
                for energy in pokemon.energies:
                    toDiscardPile(energy, player)
                toDiscardPile(pokemon, player)

#pops the first prize card in the list, returns it as a card object
def takePrizeCard(player):
    prizeCard = player.prizeCards.pop(1)
    return prizeCard

#evolves a target pokemon, appends it as a previousStage to it's evolution, and adds all attached cards/counters to it
def evolvePokemon(pokemon, evolution, player):
    if (isCardActivePokemon(pokemon, player) is True):
        newActive = removeCardFromHand(evolution)
        for energy in oldActive.energies:
            newActive.energies.append(detachEnergy(energy, oldActive))
        newActive.damageCounters = oldActive.damageCounters
        oldActive.damageCounters = 0
        oldActive = removeCardFromActive(pokemon)
        newActive.previousStage = oldActive
        player.active.append(newActive)


#removes a specified card from hand and returns it as a card object
def removeCardFromHand(card, player):
    if (isCardInHand(card, player) is True):
        player.hand.remove(card)
        return card
    
#removes a specified card from an active zone and returns it as a card object
def removeCardFromActive(card, player):
    if (isCardActivePokemon(card, player) is True):
        player.active.remove(card)
        return card
    
#converts damage to counters and returns the amount of damage counters
def convertDamageToCounters(damage):
    return damage/10

#increments damage counters on a pokemon
def addDamageCounters(pokemon, amount):
    pokemon.damageCounters += amount

#Poisons a pokemon, sets isPoisoned to true
def poisonPokemon(pokemon):
    pokemon.isPoisoned = True

#Inflicts poison damage to a pokemon
def inflictPoisonDamage(pokemon):
    pokemon.damageCounters += 1

#Burns a pokemon, sets isBurned to true
def burnPokemon(pokemon):
    pokemon.isBurned = True

#Inflicts burn damage to a pokemon
def inflictBurnDamage(pokemon):
    if (coinToss() == "Heads"):
        pokemon.damageCounters += 2

#Sends pokemon to sleep, sets statusCondition to Asleep
def sleepPokemon(pokemon):
    pokemon.statusCondition = "Asleep"

#Tosses a coin to see if a pokemon should wake up
def sleepCheck(pokemon):
    if (coinToss() == "Heads"):
        pokemon.statusCondition = ""
        print(pokemon.name, "woke up!")
    else:
        print(pokemon.name, "is fast asleep.")

#Confuses the pokemon, sets statusCondition to Confused
def confusePokemon(pokemon):
    pokemon.statusCondition = "Confused"

#Tosses a coin to see if a pokemon hurts itself in confusion
def confuseCheck(pokemon):
    if (coinToss() == "Tails"):
        pokemon.damageCounter += 2

#Paralyzes the pokemon, sets statusCondition to Paralyzed
def paralyzePokemon(pokemon):
    pokemon.statusCondition = "Paralyzed"

#Cures a pokemon's status condition
def cureStatus(pokemon):
    pokemon.statusCondition = None