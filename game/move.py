from . import Moves

#defines a move to be used by a pokemon, every move has a name and type
class Move:
    def __init__(self, moveName, moveType):
        self.moveName = moveName
        self.moveType = moveType
    
#defines an attack, a type of move, every attack has a cost, damage amount, description of the move and action
class Attack(Move):
    cost = []
    def __init__(self, moveName, moveType, cost, damage, description, action):
        super().__init__(moveName, moveType)
        self.cost = cost
        self.damage = damage
        self.description = description
        self.action = action

    def printMove(self):
        print(f"{self.moveName} (cost: {self.cost} ")
        print(f"{self.description}")
        print(f"{self.damage}")

#defines a pokepower, a type of move, every pokepower has a description and action
class PokePower(Move):
    usedThisTurn = False
    def __init__(self, moveName, moveType, description, action):
        super().__init__(moveName, moveType)
        self.description = description
        self.action = action

    def printMove(self):
        print(f"PokePower: {self.moveName}")
        print(f"{self.description}")

#defines a pokebody, a type of move, every pokebody as a description and action
class PokeBody(Move):
    def __init__(self, moveName, moveType, description, action):
        super().__init__(moveType, moveName)
        self.description = description
        self.action = action

    def printMove(self):
        print(f"PokeBody: {self.moveName}")
        print(f"{self.description}")

#returns the function for the corresponding moveName, returns function in uncalled state
def getFunctionNameAsString(pokemonName, moveName):
    functionName = pokemonName.lower()
    functionName += moveName.replace(" ", "")
    print(functionName)