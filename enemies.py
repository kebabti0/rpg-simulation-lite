# Enemeies inspired by the game "Dragon Quest"

enemies = {
    "Slime": {
        "health": 95,
        "attack": 13,
        "defense": 4,
        "speed": 5,
        "gold_drop": (50, 75),
        "inventory" : {"Small Potion": 1, "Sticky Web": 1, "Power Elixir": 1} # Introdctory enemy, more defensive and can slow
    }, # Prioritize sticky web against hunters or faster enemies, heal if low, otherwise buff and attack

    "Skeleton": {
        "health": 100,
        "attack": 20,
        "defense": 6,
        "speed": 6,
        "gold_drop": (75, 100),
        "inventory": {"Small Potion": 1, "Power Elixir": 1, "Haste Potion": 1, "Hexdust": 1} # Early game enemy, more offensive and can boost speed, aggressive/burst
    }, # Buff attack early, use Haste Potion if slower than player, heal if low, debuff if facing a Warrior

    "Ghost": {
        "health": 90,
        "attack": 18,
        "defense": 6,
        "speed": 11,
        "gold_drop": (100, 125),
        "inventory": {"Medium Potion": 1, "Hexdust": 1, "Shadow Veil": 1, "Sticky Web": 1} # Early game enemy, faster and can debuff attack and defense, glass cannon
    }, # Debuff player's attack & defense first, heal if low, attack especially if player already debuffed

    "Chimaera": {
        "health": 120,
        "attack": 23,
        "defense": 9,
        "speed": 7,
        "gold_drop": (125, 150),
        "inventory": {"Medium Potion": 1,"Haste Potion": 1, "Sticky Web": 1, "Power Elixir": 1} # Mid game enemy, all rounder, acts accordingly 
    }, # Use Hase Potion if slower, Sticky web if faster or Hunter, heal if low, buff / attack otherwise

    "Sorcerer": {
        "health": 110,
        "attack": 26,
        "defense": 5,
        "speed": 9,
        "gold_drop": (150, 175),
        "inventory": {"Fire Scroll": 1, "Frost Shard": 1, "Cursed Ash": 1, "Medium Potion": 1} # Mid game enemy, uses special items, sets their burst up with debuffs
    }, # Open with Cursed Ash or Frost Shard against strong/fast players, use Fire Scroll for burst, heal if low
    "Golem": {
        "health": 200,
        "attack": 20,
        "defense": 18,
        "speed": 4,
        "gold_drop": (175, 200),
        "inventory": {"Stonewall Brew": 1, "Lightning Elixir": 1, "Fury Draught": 1, "Armour Piercer": 1, "Medium Potion": 1} # Mid game enemy, more defensive and can boost attack, tanky
    }, # Use Stonewall if defense is lower than player's attack, Fury Draught for burst, Lightning Elixir if player outspeeds, heal if low

    "Knight Aberrant": {
        "health": 165,
        "attack": 28,
        "defense": 20,
        "speed": 6,
        "gold_drop": (200, 225),
        "inventory": {"Titan's Brew": 1, "Armour Piercer": 1, "Lightning Elixir": 1, "Fury Draught": 1} # Late game enemy, has 75% block like warrior, is very tanky and sets up burst with pierce and buff
    }, # Use Titan's Brew early, Armour Piercer against Warriors or tanky players, Lightning Elixir if slower, heal if low, defensive

    "Dragon": {
        "health": 230,
        "attack": 32,
        "defense": 14,
        "speed": 10,
        "gold_drop": (225, 250),
        "inventory": {"Mega Elixir": 1, "Bullhorn Brew": 1, "Lightning Elixir": 1, "Titan's Brew": 1, "Fire Scroll": 1} # Final boss, has the best items and stats, very aggressive
    } # Buff up First (Bullhorn, Titan's), then lightning if slower, Mega Elixir if low, attack or Fire Scroll for burst

}
