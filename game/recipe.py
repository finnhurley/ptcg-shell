from .card import *
import json

#returns a deck recipe for a given path to a decklist
def createRecipe(deckListPath):
    recipe = []
    f = open(deckListPath)
    data = json.load(f)

    for i in data["Deck"]:
        if (cardExistsInList(i["cardName"], i["Set"]) == False):
            print(i["cardName"], "not found... scanning next card.")
            continue
        for j in range(int(i["quantity"])):
            recipe.append(createCard(i))
    
    return recipe

#checks to see if a card exists in the corrensponding cardinfo json, returns boolean
def cardExistsInList(cardName, cardList):
    cardInfoPath = "CardInfo/" + cardList
    f = open(cardInfoPath)
    data = json.load(f)

    for i in data["Cards"]:
        if (cardName == i["cardName"]):
            return True
    
    return False

#Creates a card using the provided json
def createCard(cardData):
    cardInfoPath = "CardInfo/" + cardData["Set"]
    f = open(cardInfoPath)
    data = json.load(f)
    for card in data["Cards"]:
        if (card["cardName"]==cardData["cardName"]):
            break
    
    if(card["cardType"] == "Pokemon"):
        return createPokemon(card)
    if(card["cardType"] == "Trainer"):
        return createTrainer(card)
    if(card["cardType"] == "Energy"):
        return createEnergy(card)

#Creates a Pokemon Card
def createPokemon(pokemonInfo):
    info = json.dumps(pokemonInfo)
    return Pokemon(pokemonInfo["cardName"], info)

#Creates a Trainer Card
def createTrainer(trainerInfo):
    return Trainer(trainerInfo["cardName"], trainerInfo["info"])

#Creates an Energy Card
def createEnergy(energyInfo):
    return Energy(energyInfo["cardName"], energyInfo["info"])