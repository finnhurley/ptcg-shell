from ..actions import *

#Blaziken (ex Ruby and Sapphire) Fire Stream
def blazikenFireStream(player, opponent):
    if (player.activePokemon().name == "Blaziken"):
        blaziken = player.activePokemon()
        defendingPokemon = opponent.activePokemon
        damage = 50
        discardEnergy("Fire", blaziken, player)
        if (len(opponent.bench) > 0):
            for pokemon in opponent.bench:
                addDamageCounters(pokemon, 1)
        damage = damageMultiplier(blaziken, defendingPokemon, damage)
        inflictDamage(defendingPokemon, damage)
        

#Combusken (ex Dragon) Quick Attack
def combuskenQuickAttack(player, opponent):
    if (player.activePokemon().name == "Combusken"):
        combusken = player.activePokemon()
        defendingPokemon = opponent.activePokemon()
        damage = 10
        if (coinToss == "Heads"):
            damage + 20
        damage = damageMultiplier(combusken, defendingPokemon, damage)
        inflictDamage(defendingPokemon, damage)

#Combusken (ex Dragon) Combustion
def combuskenCombustion(player, opponent):
    if (player.activePokemon().name == "Combusken"):
        combusken = player.activePokemon()
        defendingPokemon = opponent.activePokemon()
        damage = 40
        damage = damageMultiplier(combusken, defendingPokemon, damage)
        inflictDamage(defendingPokemon, damage)
    

#Torchic (ex Ruby and Sapphire) Peck
def torchicPeck(player, opponent):
    if (player.activePokemon().name == "Torchic"):
        torchic = player.activePokemon()
        defendingPokemon = opponent.activePokemon()
        damage = 10
        damage = damageMultiplier(torchic, defendingPokemon, damage)
        inflictDamage(defendingPokemon, damage)

#Torchic (ex Ruby and Sapphire) Fireworks
def torchicFireworks(player, opponent):
    if (player.activePokemon().name == "Torchic"):
        torchic = player.activePokemon()
        defendingPokemon = opponent.activePokemon()
        damage = 30
        if (coinToss == "Tails"):
            discardEnergy("Fire", torchic, player)
        damage = damageMultiplier(torchic, defendingPokemon, damage)
        inflictDamage(defendingPokemon, damage)