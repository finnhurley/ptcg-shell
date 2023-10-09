import random
import traceback
import os
from .card import *
from .player import *

class attack:
    def __init__(self, name, cost, damage, effect):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.effect = effect

#adds a specified card to a player hand
def addCardToHand(card, player):
    player.hand.append(card)

#increments damage counters on a pokemon
def addDamageCounters(pokemon, amount):
    pokemon.damageCounters += amount

#adds a card to the bench
def addToBench(pokemon, player):
    player.bench.append(pokemon)

#Attaches an energy to a selected pokemon
def attachEnergy(energy, pokemon):
    pokemon.energies.append(energy)

#Burns a pokemon, sets isBurned to true
def burnPokemon(pokemon):
    pokemon.isBurned = True

#simulates a coin toss, returns the value Heads or Tails as a string
def coinToss():
    if (random.randint(0, 1) == 0):
        return "Tails" 
    else:
        return "Heads"
    
#Tosses a coin to see if a pokemon hurts itself in confusion
def confuseCheck(pokemon):
    if (coinToss() == "Tails"):
        pokemon.damageCounter += 2
        
#Confuses the pokemon, sets statusCondition to Confused
def confusePokemon(pokemon):
    pokemon.statusCondition = "Confused"
    
#converts counters to damage and returns the amount of damage
def convertCountersToDamage(counters):
    if (counters == 0):
        return 0
    return counters * 10
    
#converts damage to counters and returns the amount of damage counters
def convertDamageToCounters(damage):
    if (damage == 0):
        return 0
    return damage/10


#Cures a pokemon's status condition
def cureStatus(pokemon):
    pokemon.statusCondition = None

#runs the weakness and resistance checks for a pokemon, returns modified damage as int
def damageMultiplier(attackingPokemon, defendingPokemon, damage):
    if (weaknessCheck(attackingPokemon, defendingPokemon) is True):
            damage = damage * 2
    if (resistanceCheck(attackingPokemon, defendingPokemon) is True):
            damage = damage - 30
            if (damage <= 0):
                damage = 0
    return damage

#Removes an energy from a selected pokemon and returns it as a Card
def detachEnergy(energyType, pokemon):
    if energyExists(energyType, pokemon) is True:
        for i in range (len(pokemon.energies)):
            if (pokemon.energies[i].energyType == energyType):
                energyCard = pokemon.energies[i]
                pokemon.energies.remove(pokemon.energies[i])
                return energyCard
            
#detaches and discards an energy from a target pokemon          
def discardEnergy(energyType, pokemon, player):
    toDiscardPile(detachEnergy(energyType, pokemon), player)

#Checks if an energy is attached to a pokemon, returns boolean
def energyExists(energyType, pokemon):
    for energy in pokemon.energies:
        if (energyType == energy.energyType):
            return True
    return False

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

#removes a card from discard pile, returns card object if successful
def fromDiscardPile(card, player):
    if (isCardInDiscardPile(card, player) is True):
        for i in range(len(player.discardPile)):
            if (player.discardPile[i].name == card.name):
                player.discardPile.remove(player.discardPile[i])
                return card
            
#returns the remaining HP for a pokemon
def getRemainingHp(pokemon):
    damageCounterToDamage = pokemon.damageCounters * 10
    remainingHp = pokemon.pokemonHp - damageCounterToDamage
    if (remainingHp <= 0):
        return 0
    else:
        return damageCounterToDamage
            
#Inflicts burn damage to a pokemon
def inflictBurnDamage(pokemon):
    if (coinToss() == "Heads"):
        pokemon.damageCounters += 2

#converts damage to counters and adds them to target pokemon
def inflictDamage(pokemon, damage):
    try:
        counters = convertDamageToCounters(damage)
        addDamageCounters(pokemon, counters)
    except:
        refreshScreen()
        traceback.print_exc()
        input()


#Inflicts poison damage to a pokemon
def inflictPoisonDamage(pokemon):
    pokemon.damageCounters += 1

#Checks if a specified card is a players active pokemon, returns boolean
def isCardActivePokemon(card, player):
    for c in player.active:
        if (c.name == card.name):
            return True
    return False

#Checks if a specified card exists in a players discard pile, returns boolean
def isCardInDiscardPile(card, player):
    for c in player.discardPile:
        if (c.name == card.name):
            return True
    return False

#Checks if a specified card exists in a players hand, returns boolean
def isCardInHand(card, player):
    for c in player.hand:
        if (c.name == card.name):
            return True
    return False

#Checks if a specified card exists on a players bench, returns boolean
def isCardOnBench(card, player):
    for c in player.bench:
        if (c.name == card.name):
            return True
    return False

#does a check to see if a pokemon has enough damage counters to be knocked out. Returns boolean
def isKnockedOut(pokemon):
    remainingHp = getRemainingHp(pokemon)
    if (remainingHp == 0):
        print(f"{pokemon.name} has fainted!")
        return True
    else:
        print("%s HP: %d/%d" % (pokemon.name, remainingHp, pokemon.pokemonHp))
        print(f"{pokemon.name} HP: {remainingHp}/{pokemon.pokemonHp}")
        return False
    
#knocks out a pokemon, adds it and all attached cards to the discard pile
def knockOutPokemon(pokemon, player):
    if (isCardActivePokemon(pokemon, player) is True):
        for i in range(len(player.active)):
            if (player.active[i].name == pokemon.name):
                discard = player.active[i].name
                if (discard.previousStage != None):
                    while discard.previousStage != None:
                        next = discard.previousCard
                        toDiscardPile(discard, player)
                        discard = next
                for energy in pokemon.energies:
                    toDiscardPile(energy, player)
                toDiscardPile(removeCardFromActive(discard), player)

#Paralyzes the pokemon, sets statusCondition to Paralyzed
def paralyzePokemon(pokemon):
    pokemon.statusCondition = "Paralyzed"

#Poisons a pokemon, sets isPoisoned to true
def poisonPokemon(pokemon):
    pokemon.isPoisoned = True

#removes a card from active pokemon slot
def removeCardFromActive(card, player):
    player.active.remove(0)
    return card

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

#pops the first prize card in the list, returns it as a card object
def takePrizeCard(player):
    prizeCard = player.prizeCards.pop(1)
    return prizeCard

#adds a card to the players discard pile
def toDiscardPile(card, player):
    player.discardPile.append(card)

def refreshScreen():
        os.system('cls||clear')

#resets all pokePowerFlag instances that were set to True, called at the end of a player's turn
def resetPokePowerFlags(player):
    if (player.activePokemon().pokePowerFlag is True):
        player.activePokemon().pokePowerFlag = False
    for card in player.bench:
        if(card.pokePowerFlag is True):
            card.pokePowerFlag = False

#checks the pokemon's resistance
def resistanceCheck(attackingPokemon, defendingPokemon):
    if (attackingPokemon.pokemonType == defendingPokemon.resistanceType):
        print("it's not very effective...")
        return True
    return False

#lists all pokemon in the players deck, player selects number of corresponding pokemon, returns card object
def selectEnergyFromDeck(player):
    cardList = []
    optionNo = 0
    for card in player.deck.cards:
        if ("Energy" in str(type(card))):
            optionNo += 1
            cardList.append(card)
            print("%d. %s" % (optionNo, card.name))
    while True:
        option = input("\nselect an energy by corresponding number:")
        try:
            i = int(option)-1
            card = cardList[i]
            player.deck.cards.remove(cardList[i])
            player.deck.shuffle()
            return card
        except:
            traceback.print_exc()
            print("error: please select a number")

#displays all the opponent's active and benched pokemon, awaits a number input and returns the corresponding card object
def selectOpponentsPokemon(opponent):
    cardList = []
    cardList.append(opponent.activePokemon())
    optionNo = 1
    print(f"{optionNo}. {opponent.activePokemon().name} (Active)")
    for card in opponent.bench:
        optionNo += 1
        cardList.append(card)
        print(f"{optionNo}. {card.name} (Bench)")
    while True:
        option = input("\nselect a pokemon by corresponding number:")
        try:
            selectedNo = int(option)-1
            return cardList[selectedNo]
        except:
            print("error: please select a number")

#displays all the opponent's benched pokemon, awaits a number input and returns the corresponding card object
def selectOpponentsBenchedPokemon(opponent):
    cardList = []
    optionNo = 0
    for card in opponent.bench:
        optionNo += 1
        cardList.append(card)
        print(f"{optionNo}. {card.name} (Bench)")
    while True:
        option = input("\nselect a pokemon by corresponding number:")
        try:
            selectedNo = int(option)-1
            return cardList[selectedNo]
        except:
            print("error: please select a number")

#displays all the players benched pokemon, awaits a number input and returns the corresponding card object
def selectOwnBenchedPokemon(player):
    cardList = []
    optionNo = 0
    print(f"{optionNo}. {player.activePokemon().name}")
    for card in player.bench:
        optionNo += 1
        cardList.append(card)
        print("{optionNo}. {card.name} (Bench)")
    while True:
        option = input("\nselect a pokemon by corresponding number:")
        try:
            selectedNo = int(option)-1
            return cardList[selectedNo]
        except:
            print("error: please select a number")

#displays all the players active and benched pokemon, awaits a number input and returns the corresponding card object
def selectOwnPokemon(player):
    cardList = []
    cardList.append(player.activePokemon())
    optionNo = 1
    print(f"{optionNo}. {player.activePokemon().name} (Active)")
    for card in player.bench:
        optionNo += 1
        cardList.append(card)
        print(f"{optionNo}. {card.name} (Bench)")
    while True:
        option = input("\nselect a pokemon by corresponding number:")
        try:
            selectedNo = int(option)-1
            return cardList[selectedNo]
        except:
            print("error: please select a number")

#lists all pokemon in the players deck, player selects number of corresponding pokemon, returns card object
def selectPokemonFromDeck(player):
    cardList = []
    optionNo = 0
    for card in player.deck.cards:
        if ("Pokemon" in str(type(card))):
            optionNo += 1
            cardList.append(card)
            print(f"{optionNo}. {card.name}: {card.stage}")
    while True:
        option = input("\nselect a pokemon by corresponding number:")
        try:
            i = int(option)-1
            card = cardList[i]
            player.deck.cards.remove(cardList[i])
            player.deck.shuffle()
            return card
        except:
            traceback.print_exc()
            print("error: please select a number")

#displays all basic pokemon in the players hand, awaits number input and sets that pokemon as active
def selectStartingActivePokemon(player):
    refreshScreen()
    print("%s's Basic Pokemon:\n" % player.name)
    cardList = []
    optionNo = 0
    for card in player.hand:
        if ("Pokemon" in str(type(card))):
            if (card.stage == "Basic"):
                optionNo += 1
                cardList.append(card)
                print(f"{optionNo}. {card.name}")
    while True:
        option = input(f"\n{player.name}: Select the number of your starting active pokemon:    ")
        try:
            selectedNo = int(option)-1
            player.active.append(removeCardFromHand(cardList[selectedNo], player))
            return
        except:
            print("error: please select a number")
    
#displays all basic pokemon in the players hand, awaits number inputs and sets pokemon on the bench until player is done
def selectStartingBenchedPokemon(player):
    while True:
        refreshScreen()
        print("%s: add as many basic pokemon as you want to your bench\n" % player.name)
        cardList = []
        optionNo = 0
        for card in player.hand:
            if ("Pokemon" in str(type(card))):
                if (card.stage == "Basic"):
                    optionNo += 1
                    cardList.append(card)
                    print(f"{optionNo}. {card.name}")
        if (optionNo == 0):
            refreshScreen()
            print(f"{player.name} has no more pokemon to put on the bench.")
            input("Press enter to continue: ")
            return
        optionDone = optionNo+1
        print(f"{optionDone}. Done")
        option = input(f"\n{player.name}: Select a pokemon to put on the bench:    ")
        try:
            selectedNo = int(option)-1
            if (int(option) == optionDone):
                return
            addToBench(removeCardFromHand(cardList[selectedNo], player), player)
            if (len(player.bench) == 5):
                return
        except:
            print("Error: please select a valid number")

#Tosses a coin to see if a pokemon should wake up
def sleepCheck(pokemon):
    if (coinToss() == "Heads"):
        pokemon.statusCondition = ""
        print(f"{pokemon.name} woke up!")
    else:
        print(f"{pokemon.name} is fast asleep.")

#Sends pokemon to sleep, sets statusCondition to Asleep
def sleepPokemon(pokemon):
    pokemon.statusCondition = "Asleep"

#Executes a pokemons attack if it has enough energy to use the move, returns boolean if successful
def useAttack(pokemon, move, player, opponent):
    pokemonEnergies = []
    for energy in pokemon.energies:
        pokemonEnergies.append(energy.name)
    if(all(e in move.cost for e in pokemonEnergies)):
        for m in pokemon.moves:
            if (m.name == move.moveName):
                m.action(player, opponent)
                return True
    else:
        print(f"Error: {pokemon.name} doesn't enough enough energy to use {move.moveName}.")
        return False

#Executes a pokemon's pokepower if it hasnt been used this turn, returns boolean if successful
def usePokePower(pokemon, power, player, opponent):
    if (pokemon.pokePowerFlag is False):
        for m in pokemon.moves:
            if (m.moveType == "PokePower" and m.moveName == power.Name):
                m.action(pokemon, power, player, opponent)
                pokemon.pokePowerFlag = True
                return True
    else:
        print(f"Error: {pokemon.name}'s {power.moveName} has already been used this turn")
        return False
    
#Lists all pokemon in the hand
def viewHand(player):
    optionNo = 0
    for card in player.hand:
        optionNo
        print("%d. %s" % (optionNo, card.name))

#checks the defending pokemon's weakness
def weaknessCheck(attackingPokemon, defendingPokemon):
    if (attackingPokemon.pokemonType == defendingPokemon.weaknessType):
        print("it's super effective!")
        return True
    return False