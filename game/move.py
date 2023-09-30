#defines a move to be used by a pokemon, every move has a name and type
class Move:
    def __init__(self, moveName, moveType):
        self.moveName = moveName
        self.moveType = moveType
    
#defines an attack, a type of move, every attack has a cost, damage amount, description of the move and action
class Attack(Move):
    cost = []
    def __init__(self, moveName, moveType, cost, damage, description, action=print):
        super().__init__(moveName, moveType)
        self.cost = cost
        self.damage = damage
        self.description = description
        self.action = action

#defines a pokepower, a type of move, every pokepower has a description and action
class PokePower(Move):
    def __init__(self, moveName, moveType, description, action=print):
        super().__init__(moveType, moveName)
        self.description = description
        self.action = action

#defines a pokebody, a type of move, every pokebody as a description and action
class PokeBody(Move):
    def __init__(self, moveName, moveType, description, action=print):
        super().__init__(moveType, moveName)
        self.description = description
        self.action = action