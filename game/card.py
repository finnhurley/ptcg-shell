from .move import *
from .actions import *
from .Moves.attacks import *
from .Moves.pokebodies import *
from .Moves.pokepowers import *
from .Moves.trainers import *
import json
import inspect

class Card:
    def __init__(self, name):
        self.name = name
        #self.setName = setName
        #self.setId = setId

class Pokemon(Card):
    def __init__(self, name, pokemonInfo):
        self.cardType = "Pokemon"
        self.pokePowerFlag = False
        self.isPoisoned = False
        self.isBurned = False
        self.statusCondition = None
        self.damageCounters = 0
        self.moves = []
        self.energies = []
        self.previousStage = None
        self.previousCard = None
        pokemonInfo = json.loads(pokemonInfo)
        info = pokemonInfo["info"]
        super().__init__(name)
        self.pokemonType = info["type"]
        self.pokemonHp = info["hp"]
        self.stage = info["stage"]
        if (self.stage != "Basic"):
            self.evolvesFrom = info["evolvesFrom"]
        self.weaknessType = info["weakness"]
        self.resistanceType = info["resistance"]
        self.retreatCost = int(info["retreat"])
        for move in info["moves"]:
            if move["type"] == "Attack":
                self.moves.append(newAttack(self.name, move))
            if move["type"] == "PokePower":
                self.moves.append(newPokePower(self.name, move))
            if move["type"] == "PokeBody":
                self.moves.append(newPokeBody(self.name, move))
    
    def viewCard(self):
        print("==========")
        print("%s\n%sHP\nType: %s" % (self.name, self.pokemonHp, self.pokemonType))
        print("Stage: %s" % self.stage)
        if (self.stage != "Basic"):
            print("Evolves from %s" % self.evolvesFrom)
        print("----------")
        for i in range(len(self.moves)):
            print("Move %s:" % str(i+1))
            self.moves[i].printMove()
            print("----------")
        print("weakness: %s" % self.weaknessType)
        print("resistance: %s" % self.resistanceType)
        print("retreat cost: %s\n==========" % self.retreatCost)

    def getRemainingHP(self):
        dmg = convertCountersToDamage(self.damageCounters)
        return (int(self.pokemonHp) - dmg)
    
    def canRetreat(self):
        return True if (len(self.energies) >= int(self.retreatCost)) else False
        
        
                
class Trainer(Card):
    def __init__(self, name, trainerInfo):
        super().__init__(name)
        self.cardType = trainerInfo["trainerType"]
        self.effect = trainerInfo["description"]
        self.action = getTrainerFunction(name)

    def viewCard(self):
        print("==========")
        print("[%s] %s\n" % (self.cardType, self.name))
        if(self.cardType == "Supporter"):
            print("----------")
            print("You can only use 1 Supporter Card Per Turn")
        print("----------")
        print("%s" % self.effect)
        print("==========")

class Energy(Card):
    def __init__(self, name, energyInfo):
        super().__init__(name)
        self.cardType = "Energy"
        self.energyType = energyInfo["energyType"]
    def viewCard(self):
        print("==========")
        print("[%s] %s\n" % (self.cardType, self.name))
        print("Attach this card to any pokemon to provide 1 %s." % self.name)

def newAttack(pokemonName, attackInfo):
    name = attackInfo["moveName"]
    type = attackInfo["type"]
    atkCost = []
    for energy in attackInfo["cost"]:
        atkCost.append(energy["energy"])
    damage = attackInfo["damage"]
    description = attackInfo["description"]
    action = getAttackFunction(pokemonName, name)
    return Attack(name, type, atkCost, damage, description, action)

def newPokePower(pokemonName, powerInfo):
    name = powerInfo["moveName"]
    type = powerInfo["type"]
    description = powerInfo["description"]
    action = getPokePowerFunction(pokemonName, name)
    return PokePower(name, type, description, action)

def newPokeBody(pokemonName, bodyInfo):
    name = bodyInfo["moveName"]
    type = bodyInfo["type"]
    description = bodyInfo["description"]
    action = getPokeBodyFunction(pokemonName, name)
    return PokePower(name, type, description, action)

#Converts pokemon move to a function name to be called from the PokemonMoves folder
#e.g. Pikachu's Thunder Jolt will return the function name pikachuThunderJolt, which would be called from moves.py
def convertMoveToFunctionName(pokemonName, moveName):
    funcName = pokemonName.lower()
    moveName = moveName.replace(" ", "")
    funcName += moveName
    return funcName

#Converts trainer card to a function name to be called from the Trainers folder
#e.g. Energy Search will return the function name energySearch, which will be called from moves.py
def convertTrainerToFunctionName(trainerName):
    funcName = trainerName[0].lower() + trainerName[1:].replace(" ", "")
    return funcName

def getAttackFunction(pokemonName, moveName):
    functionName = convertMoveToFunctionName(pokemonName, moveName)
    move = getattr(Moves.attacks, functionName)
    return move

def getPokePowerFunction(pokemonName, moveName):
    functionName = convertMoveToFunctionName(pokemonName, moveName)
    move = getattr(Moves.pokepowers, functionName)
    return move

def getPokeBodyFunction(pokemonName, moveName):
    functionName = convertMoveToFunctionName(pokemonName, moveName)
    move = getattr(Moves.pokebodies, functionName)
    return move

def getTrainerFunction(moveName):
    functionName = convertTrainerToFunctionName(moveName)
    move = getattr(Moves.trainers, functionName)
    return move