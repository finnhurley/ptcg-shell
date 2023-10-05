import os
from .player import *
from .card import *
from .deck import *
from .actions import *

class Game:
    def __init__(self, player1, player2):
        self.p1, self.p2 = player1, player2
        self.winner = None
        self.loser = None
        self.forfeit = False
        self.usedEnergyThisTurn = False

    #Performs the coin tosses, sets up the decks and runs the game
    def start(self):
        first, second = self.setUpGame(self.p1, self.p2)
        self.runGame(first, second)

    #Performs a coin toss to see which player will go first
    def setUpGame(self, player1, player2):
        coin = coinToss()
        if (coin == "Heads"):
            first = player1
            second = player2
        else:
            first = player2
            second = player1
        menu = True
        while menu:
            self.refreshScreen()
            print("Game started!")
            print("The coin landed on %s! %s will go first!" % (coin, first.name))
            option = input("\n\nPress enter to start:  ")
            menu = False
        self.refreshScreen()
        return first, second
    
    #Sets up the decks, prize card and starting hands, then runs the game until someone wins
    def runGame(self, first, second):
        first.setUpBoard()
        second.setUpBoard()
        selectStartingActivePokemon(first)
        selectStartingBenchedPokemon(first)
        selectStartingActivePokemon(second)
        selectStartingBenchedPokemon(second)
        while self.winner is None:
            self.turn(first, second)
            if (self.winner is None):
                self.turn(second, first)
        self.winMenu()

    #The base process of a turn
    def turn(self, player, opponent):
        self.refreshScreen()
        isTurn = True
        addCardToHand(player.deck.drawCard(), player)
        self.turnBanner(player)
        while isTurn:
            options = "1. View Hand     2. View Active     3. View Bench     4. View Board    5. End Turn    : "
            print("\nWhat will %s do?" % player.name)
            playerMove = input(options)
            self.refreshScreen()
            if (playerMove == "1"):
                self.viewHand(player, opponent)
            if (playerMove == "2"):
                self.viewActive(player, opponent)
            if (playerMove == "3"):
                self.viewBench(player, opponent)
            if (playerMove == "4"):
                self.viewGameStats(player, opponent)
            if (playerMove == "5"):
                isTurn = False
            if (playerMove == "FF" or playerMove == "ff"):
                ff = input("\nAre you sure you want to forfeit? (y/n): ")
                if (ff == "y"):
                    self.winner = opponent
                    self.loser = player
                    self.forfeit = True
                    isTurn = False
        self.endTurn(player)

    #Viewing a players hand presents the player with more options
    def viewHand(self, player, opponent):
        self.refreshScreen()
        viewingHand = True
        optionList = []
        while viewingHand:
            optionNo = 0
            for card in player.hand:
                optionNo += 1
                optionList.append(card)
                print("%d. %s [%s]" % (optionNo, card.name, card.cardType))
            optionNo += 1
            print("%s. Back" % optionNo)
            playerMove = input("Select a card: ")
            if (playerMove == str(optionNo)):
                return
            if (int(playerMove) in range(len(optionList))):
                self.viewCardInHand(player, opponent, optionList[int(playerMove)-1])

    #Viewing a card in the players hand presents the player with a unique option depending on the card
    def viewCardInHand(self, player, opponent, card):
        viewingCard = True
        card = card
        while viewingCard:
            card.viewCard()
            if (card.cardType == "Pokemon"):
                if (card.stage == "Basic"):
                    option = "Bench"
                else:
                    option = "Evolve"
            if (card.cardType == "Trainer" or card.cardType == "Supporter"):
                option = "Use"
            if (card.cardType == "Energy"):
                option = "Attach"
            print("1. %s    2. Back" % option)
            playerMove = input("Select option: ")
            self.refreshScreen()
            if (playerMove == "1"):
                if (card.cardType == "Pokemon" and card.cardType == "Basic"): print("bench")
                if (card.cardType == "Pokemon" and card.cardType != "Basic"): print("evolve")
                if (card.cardType == "Trainer" or card.cardType == "Supporter"): print("use trainer/supporter")
                if (card.cardType == "Energy"): print("attach energy")
            if (playerMove == "2"):
                return

    #viewing the active pokemon presents the player with more options
    def viewActive(self, player, opponent):
        viewingActive = True
        poke = player.activePokemon()
        EnergyList = []
        for energy in poke.energies:
            EnergyList.append(energy.energyType)
        while viewingActive:
            poke.viewCard()
            print("EnergyList: ", EnergyList)
            print("Remaining HP: %d (%d Damage Counters)" % (poke.getRemainingHP(), poke.damageCounters))
            print("\nWhat will %s do?" % poke.name)
            playerMove = input("\n1. Attack    2. Retreat    3. Back    : ")
            if (playerMove == "1"):
                self.chooseAttack(poke, player, opponent)
            if (playerMove == "2"):
                if (poke.canRetreat()):
                    print("\n%s return!" % poke.name)
                    return
                else:
                    self.refreshScreen()
                    print("\n%s can't retreat! Not enough energies.\n" % poke.name)
            if (playerMove == "3"):
                self.refreshScreen()
                return
            
    def viewBenchedPokemon(self, benchedPoke, player, opponent):
        viewingPokemon = True
        EnergyList = []
        hasPokePower = False
        optionNo = 1
        for energy in benchedPoke.energies:
            EnergyList.append(energy.energyType)
        while viewingPokemon:
            self.refreshScreen()
            benchedPoke.viewCard()
            print("EnergyList: ", EnergyList)
            print("Remaining HP: %d (%d Damage Counters)" % (benchedPoke.getRemainingHP(), benchedPoke.damageCounters))
            for move in benchedPoke.moves:
                if (move.moveType == "PokeBody"):
                    hasPokePower = True
                    break
            backOption = optionNo
            if (hasPokePower == True):
                print("%d. Use PokePower" % optionNo)
                backOption += 1
            print("%d. Back" % backOption)
            option = input("\nSelect an option:  ")
            if (int(option) == backOption):
                self.refreshScreen()
                return
            if (int(option) == optionNo):
                move.action()

    def viewOpponentBenchedPokemon(self, benchedPoke, opponent):
        viewingPokemon = True
        EnergyList = []
        for energy in benchedPoke.energies:
            EnergyList.append(energy.energyType)
        while viewingPokemon:
            self.refreshScreen()
            benchedPoke.viewCard()
            print("EnergyList: ", EnergyList)
            print("Remaining HP: %d (%d Damage Counters)" % (benchedPoke.getRemainingHP(), benchedPoke.damageCounters))
            option = input("\nPress Enter to return:  ")
            return

            
    #viewing the opponent's active pokemon
    def viewOpponentActive(self, opponent):
        viewingActive = True
        poke = opponent.activePokemon()
        EnergyList = []
        for energy in poke.energies:
            EnergyList.append(energy.energyType)
        while viewingActive:
            self.refreshScreen()
            poke.viewCard()
            print("EnergyList: ", EnergyList)
            print("Remaining HP: %d (%d Damage Counters)" % (poke.getRemainingHP(), poke.damageCounters))
            playerMove = input("\n1. Back    : ")
            if (playerMove == "1"):
                self.refreshScreen()
                return

    #Viewing the bench presents the player with more options
    def viewBench(self, player, opponent):
        viewingBoard = True
        while viewingBoard:
            self.refreshScreen()
            if (len(player.bench) == 0):
                print("%s doesn't have any pokemon on their bench!" % player.name)
                input("Press enter to return:   ")
                return
            else:
                print("%s's Bench" % player.name)
                optionNo = 0
                pokeList = []
                for poke in player.bench:
                    optionNo += 1
                    print("%d. %s [%s]" % (optionNo, poke.name, poke.pokemonType))
                    pokeList.append(poke)
                backOption = optionNo+1
                print("%d. Back\n" % backOption)
                option = input("Select a pokemon by number")
                selectedNo = int(option)-1
                try:
                    if (int(option) == backOption):
                        return
                    self.viewBenchedPokemon(pokeList[selectedNo], player, opponent)
                    return
                except:
                    print("error: please select a valid number")

    #Viewing the bench presents the player with more options
    def viewOpponentBench(self, opponent):
        viewingBoard = True
        while viewingBoard:
            self.refreshScreen()
            if (len(opponent.bench) == 0):
                print("%s doesn't have any pokemon on their bench!" % opponent.name)
                input("Press enter to return:   ")
                return
            else:
                print("%s's Bench" % opponent.name)
                optionNo = 0
                pokeList = []
                for poke in opponent.bench:
                    optionNo += 1
                    print("%d. %s [%s]" % (optionNo, poke.name, poke.pokemonType))
                    pokeList.append(poke)
                backOption = optionNo+1
                print("%d. Back\n" % backOption)
                option = input("Select a pokemon by number")
                selectedNo = int(option)-1
                try:
                    if (int(option) == backOption):
                        return
                    self.viewOpponentBenchedPokemon(pokeList[selectedNo], opponent)
                    return
                except:
                    print("error: please select a valid number")

    #Prints the number of cards in the players hand, prizes and deck so each player can gauge progress  
    def viewGameStats(self, player, opponent):
        viewingBoard = True
        while viewingBoard:
            self.refreshScreen()
            self.dumpPlayerBoard(player)
            print("\n--------------------------------------------------")
            print("--------------------------------------------------")
            self.dumpPlayerBoard(opponent)
            print("\n\n1. View Active           2. View Bench              3. View Discard Pile")
            print("4. View Opponent's Active    5. View Opponent's Bench   6. View Opponent's Discard Pile")
            print("7. Back")
            option = input("Select an option:    ")
            self.refreshScreen()
            if (option == "1"):
                self.viewActive(player, opponent)
            if (option == "2"):
                self.viewBench(player, opponent)
            if (option == "3"):
                self.dumpDiscardPile(player)
            if (option == "4"):
                self.viewOpponentActive(opponent)
            if (option == "5"):
                self.viewOpponentBench(opponent)
            if (option == "6"):
                self.dumpDiscardPile(opponent)
            if (option == "7"):
                viewingBoard = False

    #Displays info on a player's board
    def dumpPlayerBoard(self, player):
        active = player.activePokemon()
        print("%s:      Hand: %d      Prize Cards: %d      Deck: %d\n" % (player.name, len(player.hand), len(player.prizes), len(player.deck.cards)))
        print("Active Pokemon:")
        statusString = ""
        playerInfoString = "%s%s, [%s] %d/%s HP, Energies: %d " % (active.name, statusString, active.pokemonType, active.getRemainingHP(), active.pokemonHp, len(active.energies))
        statusString = " ("
        if (active.isPoisoned):
            statusString += " Poisoned "
        if (active.isBurned):
            statusString += " Burned "
        if (active.statusCondition is not None):
            statusString += " %s " % active.statusCondition
        statusString += ")"
        print(playerInfoString)
        print("\nBench:")
        for poke in player.bench:
            print("%s: [%s] %s/%s HP" % (poke.name, poke.pokemonType, poke.getRemainingHP(), poke.pokemonHp))

    #Displays all cards in a player's discard pile
    def dumpDiscardPile(self, player):
        viewingDiscardPile = True
        while viewingDiscardPile:
            self.refreshScreen()
            print("%s's discard pile" % player.name)
            if (len(player.discardPile) == 0):
                print("There's nothing here!")
            else:
                for card in player.disardPile:
                    print(card.name)
            print("\n\n1. Back")
            option = input("Select Option:  ")
            if (option == "1"):
                viewingDiscardPile = False

    #does all the turn ending checks like status conditions etc.
    def endTurn(self, player):
        if (self.winner is not None):
            return
        if (player.activePokemon().isBurned):
            poisonPokemon(player.activePokemon())
        if (player.activePokemon().isBurned):
            burnPokemon(player.activePokemon())
        if (player.activePokemon().statusCondition == "Asleep"):
            sleepCheck(player.activePokemon())
        if (player.activePokemon().statusCondition == "Paralyzed"):
            cureStatus(player.activePokemon())
        while True:
            print("%s's Turn is over." % player.name)
            print("1. Continue")
            option = input("Select option:  ")
            if (option == "1"):
                return
            
    def winMenu(self):
        while True:
            self.refreshScreen()
            if (self.forfeit):
                print("%s has forfeited!" % self.loser.name)
                print("%s is the winner!!" % self.winner.name)
                option = input("Enter any key to continue: ")
                return
            if (len(self.winner.prizeCards) == 0):
                print("%s has no prize cards left!" % (self.winner.name))
            if (len(self.loser.bench) == 0):
                print("%s has run out of pokemon!" % self.loser.name)
            print("%s is the winner!!" % self.winner.name)
            option = input("Enter any key to continue: ")
            return

    #Returns True if a pokemon has enough energies
    def energyCheck(self, pokemon, move):
        pokemonEnergies = []
        for energy in pokemon.energies:
            pokemonEnergies.append(energy.name)
        if (len(pokemonEnergies) == 0):
            return False
        if (set(pokemonEnergies).issubset(move.cost) or set(move.cost).issubset(pokemonEnergies)):
            return True
        else:
            return False

    def chooseAttack(self, pokemon, player, opponent):
        decideAttack = True
        while decideAttack:
            optionNo = 0
            for move in pokemon.moves:
                optionNo +=1
                print("%d. %s" % (optionNo, move.moveName))
            optionNo += 1
            print("%d. Cancel" % optionNo)
            option = input("Select Attack: ")
            optionInt = int(option) - 1
            if (optionInt in range(len(pokemon.moves))):
                selectedMove = pokemon.moves[int(optionInt)]
                if (self.energyCheck(pokemon, move)):
                    selectedMove.action(player, opponent)
                    decideAttack = False
                else:
                    self.refreshScreen()
                    print("%s doesn't have enough energy to perform %s!" % (pokemon.name, selectedMove.moveName))
            if (int(option) == optionNo):
                decideAttack = False

    def refreshScreen(self):
        os.system('cls||clear')

    def turnBanner(self, player):
        print("--------------------")
        print("%s's Turn" % player.name)
        print("--------------------")
