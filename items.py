# Dictionary of items sold in the ingame shop and granted to the player at the start of the game

items = {
    "Small Potion": {
        "type": "heal", "price": 5, "heal_amount": 10, "description": "Restores 10 HP."
    },
    "Medium Potion": {
        "type": "heal", "price": 10, "heal_amount": 20, "description": "Restores 20 HP."
    },
    "Mega Elixir": {
        "type": "heal", "price": 30, "heal_amount": 50, "description": "Restores 50 HP."
    },
    "Power Elixir": {
        "type": "buff", "price": 10, "attack_boost": 5, "duration": 3, "description": "Increases attack by 5 for 3 turns."
    },
    "Fury Draught": {
        "type": "buff", "price": 15, "attack_boost": 10, "duration": 3, "description": "Increases attack by 10 for 3 turns."
    },
    "Bullhorn Brew": {
        "type": "buff", "price": 25, "attack_boost": 15, "duration": 3, "description": "Increases attack by 15 for 3 turns."
    },
    "Iron Skin Tonic": {
        "type": "buff", "price": 10, "defense_boost": 5, "duration": 3, "description": "Raises defense by 5 for 3 turns."
    },
    "Stonewall Brew": {
        "type": "buff", "price": 15, "defense_boost": 10, "duration": 3, "description": "Raises defense by 10 for 3 turns."
    },
    "Titan's Brew": {
        "type": "buff", "price": 25, "defense_boost": 15, "duration": 3, "description": "Raises defense by 15 for 3 turns."
    },
    "Haste Potion": {
        "type": "buff", "price": 10, "speed_boost": 5, "duration": 3, "description": "Increases speed by 2 for 3 turns."
    },
    "Gale Essence": {
        "type": "buff", "price": 15, "speed_boost": 10, "duration": 3, "description": "Increases speed by 5 for 3 turns."
    },
    "Lightning Elixir": {
        "type": "buff", "price": 25, "speed_boost": 15, "duration": 3, "description": "Increases speed by 8 for 3 turns."
    }, 
    "Hexdust": {
        "type": "debuff", "price": 10, "attack_debuff": 5, "duration": 3, "description": "Reduces enemy attack by 5 for 3 turns."
    },
    "Cursed Ash": {
        "type": "debuff", "price": 20, "attack_debuff": 10, "duration": 3, "description": "Reduces enemy attack by 10 for 3 turns"
    },
    "Shadow Veil": {
        "type": "debuff", "price": 10, "defense_debuff": 5, "duration": 3, "description": "Reduces enemy defense by 5 for 3 turns."
    },
    "Armour Piercer": {
        "type": "debuff", "price": 20, "defense_debuff": 10, "duration": 3, "description": "Reduces enemy defense by 10 for 3 turns."
    },
    "Sticky Web": {
        "type": "debuff", "price": 10, "speed_debuff": 5, "duration": 3, "description": "Reduces enemy speed by 5 for 3 turns."
    },
    # Mage-exclusive items
    "Fire Scroll": {
        "type": "special", "price": 30, "damage": 30, "description": "Deals 30 damage to an enemy.", "exclusive": "Mage"
    },
    "Frost Shard": {
        "type": "special", "price": 30, "damage": 10, "speed_debuff": 7, "duration": 3, "description": "Deals 10 damage and reduces enemy speed by 7 for 3 turns.", "exclusive": "Mage"
    }
}