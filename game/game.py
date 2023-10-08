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
        self.hasAttacked = False

    def attachEnergy(self, energy, player):
        if (self.usedEnergyThisTurn is True):
            refreshScreen()
            print("%s has already attached an energy this turn!" % player.name)
            input("Press Enter to continue: ")
            return
        selectingEnergyTarget = True
        while selectingEnergyTarget:
            optionList = []
            optionList.append(Card("MissingNo"))
            optionNo = 1
            optionList.insert(optionNo, player.activePokemon())
            print("%s's Pokemon:\n" % player.name)
            print("%d. %s [%s] Energies: %d" % (optionNo, player.activePokemon().name, player.activePokemon().pokemonType, len(player.activePokemon().energies)))
            for poke in player.bench:
                optionNo += 1
                optionList.insert(optionNo, poke)
                print("%d. %s [%s] Energies: %d" % (optionNo, poke.name, poke.pokemonType, len(poke.energies)))
            backOption = optionNo+1
            print("%d. Back" % backOption)
            option = input("\nSelect Pokemon to attach energy to:   ")
            try:
                if(int(option) == backOption):
                    return
                if(int(option) is not 0 and int(option) in range(len(optionList))):
                    refreshScreen()
                    attachEnergy(removeCardFromHand(energy, player), optionList[int(option)])
                    print("%s has been attached to %s" % (energy.name, optionList[int(option)].name))
                    input("\nPress enter to continue:   ")
                    self.usedEnergyThisTurn = True
                    return
            except:
                refreshScreen()

    def chooseAttack(self, pokemon, player, opponent):
        decideAttack = True
        while decideAttack:
            i = -1
            optionNo = 0
            trueIndex = []
            trueIndex.append(i)
            for move in pokemon.moves:
                optionNo +=1
                i += 1
                trueIndex.append(i)
                print("%d. %s" % (optionNo, move.moveName))
            cancel = optionNo + 1
            print("%d. Cancel" % cancel)
            option = input("Select Attack: ")
            #optionInt = int(option)
            try:
                input("optionInt = %d" % int(option))
                input("truIndex = %d" % trueIndex[int(option)])
                if (int(option) == cancel):
                    decideAttack = False
                if (int(option) in range(len(pokemon.moves))):
                    selectedMove = pokemon.moves[trueIndex[int(option)]]
                    input(selectedMove.moveName)
                    if (self.energyCheck(pokemon, selectedMove)):
                        try:
                            input("%s used %s!" % (pokemon.name, selectedMove.moveName))
                            initHp = opponent.activePokemon().getRemainingHP()
                            selectedMove.action(player, opponent)
                            afterHp = opponent.activePokemon().getRemainingHP()
                            print("Foe's %s took the hit! %d -> %d HP" % (opponent.activePokemon().name, initHp, afterHp))
                            self.hasAttacked = True
                            input("Press enter to end turn")
                            return
                        except:
                            refreshScreen()
                            traceback.print_exc()
                            input("")
                    else:
                        refreshScreen()
                        print("%s doesn't have enough energy to perform %s!" % (pokemon.name, selectedMove.moveName))
            except:
                traceback.print_exc()
                print("Error. Please select a number!")
                input("Press enter")

    #Displays all cards in a player's discard pile
    def dumpDiscardPile(self, player):
        viewingDiscardPile = True
        while viewingDiscardPile:
            refreshScreen()
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

    #does all the turn ending checks like status conditions etc.
    def endTurn(self, player):
        refreshScreen()
        self.hasAttacked = False
        if (self.winner is not None):
            return
        self.usedEnergyThisTurn = False
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
            option = input("Press enter to end turn:  ")
            return
            
    #Returns True if a pokemon has enough energies
    def energyCheck(self, pokemon, move):
        pokemonEnergies = []
        moveCost = []
        for energy in pokemon.energies:
            pokemonEnergies.append(energy.energyType)
        for name in move.cost:
            moveCost.append(name)
        print("Energy Check for %s..." % move.moveName)
        for e in pokemonEnergies:
            for c in range(0, len(moveCost)):
                if (moveCost[c]==e or moveCost[c]=="Any"):
                    moveCost.remove(moveCost[c])
                    break
        if (moveCost == []):
            print("Success!")
            return True
        else:
            return False
        
        
    #Evolves the pokemon in the active spot
    def evolveActive(self, player, pokemon):
        evo = removeCardFromHand(pokemon, player)
        target = player.activePokemon()
        evo.previousCard = target
        for energy in target.energies:
            evo.energies.append(energy)
        target.energies.clear()
        evo.damageCounters = target.damageCounters
        player.active.clear()
        player.active.append(evo)
        return evo

    #Evolves the pokemon on the bench
    def evolveBench(self, player, pokemon, index):
        try:
            target = player.bench[index]
            evo = pokemon
            evo.previousCard = target
            for energy in target.energies:
                print(energy.name)
                evo.energies.append(energy)
            target.energies.clear()
            evo.damageCounters = target.damageCounters
            player.bench[index] = evo
            return evo
        except:
            traceback.print_exc()
            input("")
    
    #Removes a target pokemon from hand and evolves it if it's predecessor is on the board, returns true on success
    def evolvePokemon(self, player, pokemon):
        prevStageExists = self.hasPrevStage(pokemon, player)
        if (prevStageExists is False):
            refreshScreen()
            print("%s cannot be played as %s does not have a %s in play." % (pokemon.name, player.name, pokemon.evolvesFrom))
            input("\nPress Enter to Return:   ")
            return False
        else:
            while True:
                self.evolveSelectScreen(pokemon, player)
                return
    
    #Screen for selecting pokemon to evolve
    def evolveSelectScreen(self, pokemon, player):
        refreshScreen()
        viewingSelectScreen = True
        evolveSuccess = False
        while viewingSelectScreen:
            print("Evolve %s into %s.\n" % (pokemon.evolvesFrom, pokemon.name))
            optionNo = 0
            trueIndex = -1
            evoList = []
            trueIndexList = []
            evoList.append(Card("MissingNo"))
            trueIndexList.append(trueIndex)
            activeFlag = False
            if (player.activePokemon().name == pokemon.evolvesFrom):
                optionNo += 1
                evoList.insert(optionNo, player.activePokemon())
                print("%d. (Active) %s" % (optionNo, player.activePokemon().name))
                activeFlag = True
            for poke in player.bench:
                trueIndex += 1
                trueIndexList.append(trueIndex)
                if (poke.name == pokemon.evolvesFrom):
                    optionNo +=1
                    evoList.insert(optionNo, poke)
                    print("%d. (Bench) %s (%d/%s HP) Energies: %d" % (optionNo, poke.name, poke.getRemainingHP(), poke.pokemonHp, len(poke.energies)))
                    print(trueIndex)
            backOption = optionNo + 1
            print("%d. Back" % backOption)
            option = input("Select %s to evolve:    " % pokemon.evolvesFrom)
            try:
                refreshScreen()
                if (option == str(backOption) or option == "0"):
                    return
                else:
                    if (activeFlag) ==  True:
                        evolution = self.evolveActive(player, pokemon)
                        refreshScreen()
                        print("....what? %s is evolving!" % evolution.evolvesFrom)
                        print("Congratulations! Your %s evolved into %s!" % (evolution.evolvesFrom, evolution.name))
                        print("%d/%s HP" % (evolution.getRemainingHP(), evolution.pokemonHp))
                        print("Energies:    ")
                        for energy in evolution.energies:
                            print(" %s" % energy.name)
                        input("\n\nPress enter to return:   ")
                        viewingSelectScreen = False
                    else:
                        evolution = self.evolveBench(player, removeCardFromHand(pokemon, player), trueIndexList[int(option)])
                        viewingSelectScreen = False
                        refreshScreen()
                        print("....what? %s is evolving!" % evolution.evolvesFrom)
                        print("Congratulations! Your %s evolved into %s!" % (evolution.evolvesFrom, evolution.name))
                        print("%d/%s HP" % (evolution.getRemainingHP(), evolution.pokemonHp))
                        print("Energies:    ")
                        for energy in evolution.energies:
                            print(" %s" % energy.name)
                        input("\n\nPress enter to return:   ")
                        viewingSelectScreen = False
            except:
                refreshScreen()
                traceback.print_exc()
                input("")


    #Checks if the previous stage of a pokemon exists on the players bench
    def hasPrevStage(self, pokemon, player):
        if (player.activePokemon().name == pokemon.evolvesFrom):
            return True  
        for poke in player.bench:
            if (pokemon.evolvesFrom == poke.name):
                return True         
        return False           
    
    #Places a pokemon on the bench if there is enough space
    def placeOnBench(self, pokemon, player):
        try:
            refreshScreen() 
            addToBench(removeCardFromHand(pokemon, player), player)
            refreshScreen()
            print("%s has been placed on the bench.\n%s's bench:" % (pokemon.name, player.name))
            for poke in player.bench:
                print("%s [%s] %d/%s HP     Energies: %d" % (poke.name, poke.pokemonType, poke.getRemainingHP(), poke.pokemonHp, len(poke.energies)))
            input("Press enter to continue: ")
            return
        except:
            traceback.print_exc()
            input("")

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
            refreshScreen()
            print("Game started!")
            print("The coin landed on %s! %s will go first!" % (coin, first.name))
            option = input("\n\nPress enter to start:  ")
            menu = False
        refreshScreen()
        return first, second
    
    #Performs the coin tosses, sets up the decks and runs the game
    def start(self):
        first, second = self.setUpGame(self.p1, self.p2)
        self.runGame(first, second)
    
    #The base process of a turn
    def turn(self, player, opponent):
        refreshScreen()
        isTurn = True
        addCardToHand(player.deck.drawCard(), player)
        self.turnBanner(player)
        while isTurn:
            if (self.hasAttacked is True):
                break
            options = "1. View Hand     2. View Active     3. View Bench     4. View Board    5. End Turn    : "
            print("\nWhat will %s do?" % player.name)
            playerMove = input(options)
            refreshScreen()
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

    #Displays a banner stating the player who's turn it is
    def turnBanner(self, player):
        print("--------------------")
        print("%s's Turn" % player.name)
        print("--------------------")

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
                return
            if (playerMove == "2"):
                if (poke.canRetreat()):
                    print("\n%s return!" % poke.name)
                    return
                else:
                    refreshScreen()
                    print("\n%s can't retreat! Not enough energies.\n" % poke.name)
            if (playerMove == "3"):
                refreshScreen()
                return

    #Viewing the bench presents the player with more options
    def viewBench(self, player, opponent):
        viewingBoard = True
        while viewingBoard:
            refreshScreen()
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

    #Displayed selected pokemon from viewBench()        
    def viewBenchedPokemon(self, benchedPoke, player, opponent):
        viewingPokemon = True
        EnergyList = []
        hasPokePower = False
        optionNo = 1
        for energy in benchedPoke.energies:
            EnergyList.append(energy.energyType)
        while viewingPokemon:
            refreshScreen()
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
                refreshScreen()
                return
            if (int(option) == optionNo):
                move.action()

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
            refreshScreen()
            if (playerMove == "1"):
                if (card.cardType == "Pokemon"):
                    if(card.stage == "Basic"):
                        self.placeOnBench(card, player)
                        viewingCard = False
                    else:
                        self.evolvePokemon(player, card)
                        viewingCard = False
                if (card.cardType == "Trainer" or card.cardType == "Supporter"):
                    print("use trainer/supporter")
                    viewingCard = False
                if (card.cardType == "Energy"):
                    self.attachEnergy(card, player)
                    viewingCard = False
            if (playerMove == "2"):
                return
            
    #Prints the number of cards in the players hand, prizes and deck so each player can gauge progress  
    def viewGameStats(self, player, opponent):
        viewingBoard = True
        while viewingBoard:
            refreshScreen()
            self.dumpPlayerBoard(player)
            print("\n--------------------------------------------------")
            print("--------------------------------------------------")
            self.dumpPlayerBoard(opponent)
            print("\n\n1. View Active           2. View Bench              3. View Discard Pile")
            print("4. View Opponent's Active    5. View Opponent's Bench   6. View Opponent's Discard Pile")
            print("7. Back")
            option = input("Select an option:    ")
            refreshScreen()
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
    
    #Viewing a players hand presents the player with more options
    def viewHand(self, player, opponent):
        refreshScreen()
        viewingHand = True
        while viewingHand:
            optionList = []
            optionList.append(Card("MissingNo"))
            optionNo = 0
            for card in player.hand:
                optionNo += 1
                optionList.insert(optionNo, card)
                print("%d. %s [%s]" % (optionNo, card.name, card.cardType))
            backOption = optionNo+1
            print("%s. Back" % backOption)
            playerMove = input("Select a card: ")
            refreshScreen()
            try:
                if (int(playerMove) == backOption):
                    refreshScreen()
                    return
                if (int(playerMove) in range(len(optionList))):
                    self.viewCardInHand(player, opponent, optionList[int(playerMove)])
                    refreshScreen()
            except:
                print("Error, please select a valid number. You select %s" % playerMove)
                refreshScreen()

    #viewing the opponent's active pokemon
    def viewOpponentActive(self, opponent):
        viewingActive = True
        poke = opponent.activePokemon()
        EnergyList = []
        for energy in poke.energies:
            EnergyList.append(energy.energyType)
        while viewingActive:
            refreshScreen()
            poke.viewCard()
            print("EnergyList: ", EnergyList)
            print("Remaining HP: %d (%d Damage Counters)" % (poke.getRemainingHP(), poke.damageCounters))
            playerMove = input("\n1. Back    : ")
            if (playerMove == "1"):
                refreshScreen()
                return
            
    #Viewing the bench presents the player with more options
    def viewOpponentBench(self, opponent):
        viewingBoard = True
        while viewingBoard:
            refreshScreen()
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

    #Displays selected pokemon from viewOpponentBench()
    def viewOpponentBenchedPokemon(self, benchedPoke, opponent):
        viewingPokemon = True
        EnergyList = []
        for energy in benchedPoke.energies:
            EnergyList.append(energy.energyType)
        while viewingPokemon:
            refreshScreen()
            benchedPoke.viewCard()
            print("EnergyList: ", EnergyList)
            print("Remaining HP: %d (%d Damage Counters)" % (benchedPoke.getRemainingHP(), benchedPoke.damageCounters))
            option = input("\nPress Enter to return:  ")
            return

    #Displays the win conditions and the winner of the game
    def winMenu(self):
        while True:
            refreshScreen()
            if (self.forfeit):
                print("%s has forfeited!" % self.loser.name)
                print("%s is the winner!!" % self.winner.name)
                option = input("Enter any key to continue: ")
                return
            if (len(self.winner.prizeCards) == 0):
                print("%s has no prize cards left!" % (self.winner.name))
            if (len(self.loser.bench) == 0):
                print("%s has run out of pokemon!" % self.loser.name)
            if (len(self.loser.deck) == 0):
                print("%s has decked out!" % self.loser.name)
            print("%s is the winner!!" % self.winner.name)
            option = input("Enter any key to continue: ")
            return