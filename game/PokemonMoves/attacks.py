import sys
import os
sys.path.append('..')
from ..actions import *

#template to copy+paste for each new move
def pokemonAttack(player, opponent):
    if (player.activePokemon().name == "pokemon"):
        pkmn = player.activePokemon()
        defendingPokemon = opponent.activePokemon()
        damage = 0
        damage = damageMultiplier(pkmn, defendingPokemon, damage)
        inflictDamage(defendingPokemon, damage)

#Blaziken (ex Ruby and Sapphire) Fire Stream
def blazikenFireStream(player, opponent):
    if (player.activePokemon().name == "Blaziken"):
        pkmn = player.activePokemon()
        defendingPokemon = opponent.activePokemon()
        damage = 50
        discardEnergy("Fire", pkmn, player)
        if (len(opponent.bench) > 0):
            for pokemon in opponent.bench:
                addDamageCounters(pokemon, 1)
        damage = damageMultiplier(pkmn, defendingPokemon, damage)
        inflictDamage(defendingPokemon, damage)
        

#Combusken (ex Dragon) Quick Attack
def combuskenQuickAttack(player, opponent):
    if (player.activePokemon().name == "Combusken"):
        pkmn = player.activePokemon()
        defendingPokemon = opponent.activePokemon()
        damage = 10
        if (coinToss() == "Heads"):
            damage + 20
        damage = damageMultiplier(pkmn, defendingPokemon, damage)
        inflictDamage(defendingPokemon, damage)

#Combusken (ex Dragon) Combustion
def combuskenCombustion(player, opponent):
    if (player.activePokemon().name == "Combusken"):
        pkmn = player.activePokemon()
        defendingPokemon = opponent.activePokemon()
        damage = 40
        damage = damageMultiplier(pkmn, defendingPokemon, damage)
        inflictDamage(defendingPokemon, damage)
    

#Torchic (ex Ruby and Sapphire) Peck
def torchicPeck(player, opponent):
    if (player.activePokemon().name == "Torchic"):
        pkmn = player.activePokemon()
        defendingPokemon = opponent.activePokemon()
        damage = 10
        damage = damageMultiplier(pkmn, defendingPokemon, damage)
        inflictDamage(defendingPokemon, damage)

#Torchic (ex Ruby and Sapphire) Fireworks
def torchicFireworks(player, opponent):
    if (player.activePokemon().name == "Torchic"):
        pkmn = player.activePokemon()
        defendingPokemon = opponent.activePokemon()
        damage = 30
        if (coinToss() == "Tails"):
            discardEnergy("Fire", pkmn, player)
        damage = damageMultiplier(pkmn, defendingPokemon, damage)
        inflictDamage(defendingPokemon, damage)

#Numel (ex Dragon) Firebreathing
def numelFirebreathing(player, opponent):
    if (player.activePokemon().name == "Numel"):
        pkmn = player.activePokemon()
        defendingPokemon = opponent.activePokemon()
        damage = 10
        if (coinToss == "Heads"):
            damage += 10
        damage = damageMultiplier(pkmn, defendingPokemon, damage)
        inflictDamage(defendingPokemon, damage)

#Camerupt (ex Dragon) Super Singe
def cameruptSuperSinge(player, opponent):
    if (player.activePokemon().name == "Camerupt"):
        pkmn = player.activePokemon()
        defendingPokemon = opponent.activePokemon()
        damage = 20
        if (coinToss() == "Heads"):
            burnPokemon(defendingPokemon)
        damage = damageMultiplier(pkmn, defendingPokemon, damage)
        inflictDamage(defendingPokemon, damage)

#Camerup (ex Dragon) Ram
def cameruptRam(player, opponent):
    if (player.activePokemon().name == "Camerupt"):
        pkmn = player.activePokemon()
        defendingPokemon = opponent.activePokemon()
        damage = 50
        damage = damageMultiplier(pkmn, defendingPokemon, damage)
        inflictDamage(defendingPokemon, damage)

#Goldeen (ex Ruby and Sapphire) Flail
def goldeenFlail(player, opponent):
    if (player.activePokemon().name == "Goldeen"):
        pkmn = player.activePokemon()
        defendingPokemon = opponent.activePokemon()
        damage = pkmn.damageCounters
        damage = damageMultiplier(pkmn, defendingPokemon, damage)
        inflictDamage(defendingPokemon, damage)

#Seaking (ex Ruby and Sapphire) Water Arrow
def seakingWaterArrow(player, opponent):
    if (player.activePokemon().name == "Seaking"):
        defendingPokemon = selectOpponentsPokemon(opponent)
        inflictDamage(defendingPokemon, 30)

#Seaking (ex Ruby and Sapphire) Fast Stream
def seakingFastStream(player, opponent):
    if (player.activePokemon().name == "Seaking"):
        pkmn = player.activePokemon()
        defendingPokemon = opponent.activePokemon()
        damage = 30
        damage = damageMultiplier(pkmn, defendingPokemon, damage)
        inflictDamage(defendingPokemon, damage)

#Horsea (ex Dragon) Paralyzing Gaze
def horseaParalyzingGaze(player, opponent):
    if (player.activePokemon().name == "Horsea"):
        pkmn = player.activePokemon()
        defendingPokemon = opponent.activePokemon()
        if (coinToss() == "Heads"):
            paralyzePokemon(defendingPokemon)
        damage = 0
        damage = damageMultiplier(pkmn, defendingPokemon, damage)
        inflictDamage(defendingPokemon, damage)

#Horsea (ex Dragon) Wave Splash
def horseaWaveSplash(player, opponent):
    if (player.activePokemon().name == "Horsea"):
        pkmn = player.activePokemon()
        defendingPokemon = opponent.activePokemon()
        damage = 20
        damage = damageMultiplier(pkmn, defendingPokemon, damage)
        inflictDamage(defendingPokemon, damage)

#Seadra (ex Dragon) Energy Cannon
def seadraEnergyCannon(player, opponent):
    if (player.activePokemon().name == "Seadra"):
        pkmn = player.activePokemon()
        defendingPokemon = opponent.activePokemon()
        damage = 0
        damage = damageMultiplier(pkmn, defendingPokemon, damage)
        inflictDamage(defendingPokemon, damage)

#Seadra (ex Dragon) Water Arrow
def seadraWaterArrow(player, opponent):
    if (player.activePokemon().name == "Seadra"):
        defendingPokemon = selectOpponentsPokemon(opponent)
        inflictDamage(defendingPokemon, 30)