from .move import *
import json

class Card:
    def __init__(self, name):
        self.name = name
        #self.setName = setName
        #self.setId = setId 

class Pokemon(Card):
    statusCondition = ""
    damageCounters = 0
    moves = []
    energies = []
    previousStage = None
    
    def __init__(self, name, pokemonInfo):
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
                self.moves.append(newAttack(move))
            if move["type"] == "PokePower":
                self.moves.append(newPokePower(move))
            if move["type"] == "PokeBody":
                self.moves.append(newPokeBody(move))
                
class Trainer(Card):
    def __init__(self, name, trainerInfo):
        super().__init__(name)
        self.trainerType = trainerInfo["trainerType"]
        self.effect = trainerInfo["description"]

class Energy(Card):
    def __init__(self, name, energyInfo):
        super().__init__(name)
        self.energyType = energyInfo["energyType"]

def newAttack(attackInfo):
    name = attackInfo["moveName"]
    type = attackInfo["type"]
    atkCost = []
    for energy in attackInfo["cost"]:
        atkCost.append(energy["energy"])
    damage = attackInfo["damage"]
    description = attackInfo["description"]
    return Attack(name, type, atkCost, damage, description)

def newPokePower(powerInfo):
    name = powerInfo["moveName"]
    type = powerInfo["type"]
    description = powerInfo["description"]
    return PokePower(name, type, description)

def newPokeBody(bodyInfo):
    name = bodyInfo["moveName"]
    type = bodyInfo["type"]
    description = bodyInfo["description"]
    return PokePower(name, type, description)