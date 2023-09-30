import random

class attack:
    def __init__(self, name, cost, damage, effect):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.effect = effect

#Attaches an energy to a selected pokemon
def attachEnergy(energy, pokemon):
    pokemon.energies.add(energy)

#Removes an energy from a selected pokemon and returns it as a Card
def detachEnergy(energyType, pokemon):
    return

#simulates a coin toss, returns the value Heads or Tails as a string
def coinToss():
    if (random.randint(0, 1) == 0):
        return "Tails" 
    else:
        return "Heads"
    