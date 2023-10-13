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
            print(f"{player.name} has already attached an energy this turn!")
            input("Press Enter to continue: ")
            return
        selectingEnergyTarget = True
        while selectingEnergyTarget:
            optionList = []
            optionList.append(Card("MissingNo"))
            optionNo = 1
            optionList.insert(optionNo, player.activePokemon())
            print(f"{player.name}'s Pokemon:\n")
            print(f"{optionNo}. {player.activePokemon().name} [{player.activePokemon().pokemonType}] Energies: {len(player.activePokemon().energies)}")
            for poke in player.bench:
                optionNo += 1
                optionList.insert(optionNo, poke)
                print(f"{optionNo}. {poke.name} [{poke.pokemonType}] Energies: {len(poke.energies)}")
            backOption = optionNo+1
            print(f"{backOption}. Back")
            option = input("\nSelect Pokemon to attach energy to:   ")
            try:
                if(int(option) == backOption):
                    return
                if(int(option) is not 0 and int(option) in range(len(optionList))):
                    refreshScreen()
                    attachEnergy(removeCardFromHand(energy, player), optionList[int(option)])
                    print(f"{energy.name} has been attached to {optionList[int(option)].name}")
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
                print(f"{optionNo}. {move.moveName}")
            cancel = optionNo + 1
            print(f"{cancel}. Cancel")
            option = input("Select Attack: ")
            try:
                input(f"optionInt = {int(option)}")
                input(f"truIndex = {trueIndex[int(option)]}")
                if (int(option) == cancel):
                    decideAttack = False
                if (int(option) in range(len(pokemon.moves))):
                    selectedMove = pokemon.moves[trueIndex[int(option)]]
                    input(selectedMove.moveName)
                    if (self.energyCheck(pokemon, selectedMove)):
                        try:
                            input(f"{pokemon.name} used {selectedMove.moveName}")
                            initHp = opponent.activePokemon().getRemainingHP()
                            selectedMove.action(player, opponent)
                            afterHp = opponent.activePokemon().getRemainingHP()
                            print(f"Foe's {opponent.activePokemon().name} took the hit! {initHp} -> {afterHp} HP")
                            if(isKnockedOut(opponent.activePokemon())):
                                knockOutPokemon(opponent.activePokemon())
                                print(f"{opponent.activePokemon.name()} Fainted!")
                                print(f"{player.name} took a prize card! (Prizes left: {len(player.prizes)})")
                            self.hasAttacked = True
                            input("Press enter to end turn")
                            return
                        except:
                            refreshScreen()
                            traceback.print_exc()
                            input("")
                    else:
                        refreshScreen()
                        print(f"{pokemon.name} doesn't have enough energy to perform {selectedMove.moveName}")
            except:
                traceback.print_exc()
                print("Error. Please select a number!")
                input("Press enter")

    #Displays all cards in a player's discard pile
    def dumpDiscardPile(self, player):
        viewingDiscardPile = True
        while viewingDiscardPile:
            refreshScreen()
            print(f"{player.name}'s discard pile")
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
        print(f"{player.name}   Hand: {len(player.hand)}    Prize Cards: {len(player.prizes)}   Deck: {len(player.deck.cards)}")
        print("Active Pokemon:")
        statusString = ""
        playerInfoString = f"{active.name}{statusString}, [{active.pokemonType}] {active.getRemainingHP()}/{active.pokemonHp} HP, Energies: {len(active.energies)}"
        statusString = " ("
        if (active.isPoisoned):
            statusString += " Poisoned "
        if (active.isBurned):
            statusString += " Burned "
        if (active.statusCondition is not None):
            statusString += f"{active.statusCondition}"
        statusString += ")"
        print(playerInfoString)
        print("\nBench:")
        for poke in player.bench:
            print(f"{poke.name}: [{poke.pokemonType}] {poke.getRemainingHP()}/{poke.pokemonHp} HP")

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
            print(f"{player.name}'s Turn is over.")
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
        print(f"Energy Check for {move.moveName}...")
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
            print(f"{pokemon.name} cannot be played as {player.name} does not have a {pokemon.evolvesFrom} in play.")
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
            print(f"Evolve {pokemon.evolvesFrom} into {pokemon.name}.\n")
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
                print(f"{optionNo}. (Active) {player.activePokemon().name}")
                activeFlag = True
            for poke in player.bench:
                trueIndex += 1
                trueIndexList.append(trueIndex)
                if (poke.name == pokemon.evolvesFrom):
                    optionNo +=1
                    evoList.insert(optionNo, poke)
                    print(f"{optionNo}. (Bench) {poke.name} ({poke.getRemainingHp()}/{poke.pokemonHp} HP) Energies: {len(poke.energies)}")
                    print(trueIndex)
            backOption = optionNo + 1
            print(f"{backOption}. Back")
            option = input(f"Select {pokemon.evolvesFrom} to evolve:    ")
            try:
                refreshScreen()
                if (option == str(backOption) or option == "0"):
                    return
                else:
                    if (activeFlag) ==  True:
                        evolution = self.evolveActive(player, pokemon)
                        refreshScreen()
                        print(f"....what? {evolution.evolvesFrom} is evolving!")
                        print(f"Congratulations! Your {evolution.evolvesFrom} evolved into {evolution.name}!")
                        print(f"{evolution.getRemainingHP()}/{evolution.pokemonHp} HP")
                        print("Energies:    ")
                        for energy in evolution.energies:
                            print(f" {energy.name}")
                        input("\n\nPress enter to return:   ")
                        viewingSelectScreen = False
                    else:
                        evolution = self.evolveBench(player, removeCardFromHand(pokemon, player), trueIndexList[int(option)])
                        viewingSelectScreen = False
                        refreshScreen()
                        print(f"....what? {evolution.evolvesFrom} is evolving!")
                        print(f"Congratulations! Your {evolution.evolvesFrom} evolved into {evolution.name}!")
                        print(f"{evolution.getRemainingHP()}/{evolution.pokemonHp} HP")
                        print("Energies:    ")
                        for energy in evolution.energies:
                            print(f" {energy.name}")
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
            print(f"{pokemon.name} has been placed on the bench.\n{player.name}'s bench:")
            for poke in player.bench:
                print(f"{poke.name} [{poke.pokemonType}] {poke.getRemainingHP()}/{poke.pokemonHp} HP     Energies: {len(poke.energies)}")
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
            print(f"The coin landed on {coin}! {first.name} will go first!")
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
            print(f"\nWhat will {player.name} do?")
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
        self.winCheck()
        self.endTurn(player)

    #Displays a banner stating the player who's turn it is
    def turnBanner(self, player):
        print("--------------------")
        print(f"{player.name}'s Turn")
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
            print(f"Remaining HP: {poke.getRemainingHP()} ({poke.damageCounters} Damage Counters)")
            print(f"\nWhat will {poke.name} do?")
            playerMove = input("\n1. Attack    2. Retreat    3. Back    : ")
            if (playerMove == "1"):
                self.chooseAttack(poke, player, opponent)
                return
            if (playerMove == "2"):
                if (poke.canRetreat()):
                    print(f"\n{poke.name} return!")
                    return
                else:
                    refreshScreen()
                    print(f"\n%{poke.name} can't retreat! Not enough energies.\n")
            if (playerMove == "3"):
                refreshScreen()
                return

    #Viewing the bench presents the player with more options
    def viewBench(self, player, opponent):
        viewingBoard = True
        while viewingBoard:
            refreshScreen()
            if (len(player.bench) == 0):
                print(f"{player.name} doesn't have any pokemon on their bench!")
                input("Press enter to return:   ")
                return
            else:
                print(f"{player.name}'s Bench")
                optionNo = 0
                pokeList = []
                for poke in player.bench:
                    optionNo += 1
                    print(f"{optionNo}. {poke.name} [{poke.pokemonType}]")
                    pokeList.append(poke)
                backOption = optionNo+1
                print(f"{backOption}. Back\n")
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
            print(f"Remaining HP: {benchedPoke.getRemainingHP()} ({benchedPoke.damageCounters} Damage Counters)")
            for move in benchedPoke.moves:
                if (move.moveType == "PokeBody"):
                    hasPokePower = True
                    break
            backOption = optionNo
            if (hasPokePower == True):
                print(f"{optionNo}. Use PokePower")
                backOption += 1
            print(f"{backOption}. Back")
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
            print(f"1. {option}   2. Back")
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
                print(f"{optionNo}. {card.name} [{card.cardType}]")
            backOption = optionNo+1
            print(f"{backOption}. Back")
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
                print(f"Error, please select a valid number. You select {playerMove}")
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
            print(f"Remaining HP: {poke.getRemainingHP()} ({poke.damageCounters} Damage Counters)")
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
                print(f"{opponent.name} doesn't have any pokemon on their bench!")
                input("Press enter to return:   ")
                return
            else:
                print(f"{opponent.name}'s Bench")
                optionNo = 0
                pokeList = []
                for poke in opponent.bench:
                    optionNo += 1
                    print(f"{optionNo}. {poke.name} [{poke.pokemonType}]")
                    pokeList.append(poke)
                backOption = optionNo+1
                print(f"{backOption}. Back\n")
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
            print(f"Remaining HP: {benchedPoke.getRemainingHP()} ({benchedPoke.damageCounters} Damage Counters)")
            option = input("\nPress Enter to return:  ")
            return
        
    #Does some end of battle win condition checks
    def winCheck(self, player, opponent):
        if ((len(opponent.active) == 0 and len(opponent.bench) == 0) or len(player.prizes == 0)):
            winner = player.name
            loser = opponent.name
        if ((len(player.active) == 0 and len(player.bench) == 0) or len(opponent.prizes) == 0):
            loser = player.name
            winner = opponent.name

    #Displays the win conditions and the winner of the game
    def winMenu(self):
        while True:
            refreshScreen()
            if (self.forfeit):
                print(f"{self.loser.name} has forfeited!")
                print(f"{self.winner.name} is the winner!!")
                option = input("Enter any key to continue: ")
                return
            if (len(self.winner.prizeCards) == 0):
                print(f"{self.winner.name} has no prize cards left!")
            if (len(self.loser.bench) == 0):
                print(f"{self.loser.name} has run out of pokemon!")
            if (len(self.loser.deck) == 0):
                print(f"{self.loser.name} has decked out!")
            print(f"{self.winner.name} is the winner!!")
            option = input("Enter any key to continue: ")
            return