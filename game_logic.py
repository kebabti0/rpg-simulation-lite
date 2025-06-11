import random
import pickle
from collections import Counter
from characters import *
from game_display import *
from items import *
from enemies import *

# RPG Simulation Lite inspired by JRPG games, mainly Dragon Quest
# Main game logic for a very simple turn-based RPG battle simulator
# Handles player/enemy creation, battle loop, shop, AI an dporgression
# Code and comments will be in english for simplicity

# The order in which enemies appear in the game
enemy_order = ["Slime", "Skeleton", "Ghost", "Chimaera", "Sorcerer", "Golem", "Knight Aberrant", "Dragon"]

# Returns first healing item in inventory, or None if none found
def get_heal_item(inventory):
    for item in inventory:
        if item in items and items[item].get("type") == "heal":
            return item
    return None

def reset_buffs_debuffs(character):
    for stat in character.buffs:
         character.buffs[stat] = 0
         character.buff_duration[stat] = 0
    for stat in character.debuffs:
         character.debuffs[stat] = 0
         character.debuff_duration[stat] = 0 

def create_enemy(stage_index):
    name = enemy_order[stage_index]
    data = enemies[name]
    gold = random.randint(*data["gold_drop"])
    inventory = []
    for item, count in data["inventory"].items():
         inventory.extend([item] * count)
    return Enemy(name, data["health"], data["attack"], data["defense"], data["speed"], gold, list(data["inventory"]))

def execute_action(actor, target, action, item_name=None):
    if action == "attack":
        actor.attack_enemy(target)
    elif action == "defend":
        actor.defend()
    elif action == "use_item":
        item = items.get(item_name)
        if item and item.get("type") in ("debuff", "special"):
            actor.use_item(item_name, target=target)
        else:
            actor.use_item(item_name)
   
        
def decide_enemy_action(enemy, player):
    inv = Counter(enemy.inventory) if isinstance(enemy.inventory, list) else Counter(enemy.inventory)
    # Helper to check if an item available in enemy's inventory
    def has_item(item):
        return inv.get(item, 0) > 0
    
    # Enemy AI logic based on comments in enemies.py
    if enemy.name == "Slime":
        if enemy.health / enemy.max_health < 0.35 and has_item("Small Potion"):
            return ("use_item", "Small Potion")
        if player.player_class == "Hunter" or player.get_effective_stat("speed") > enemy.get_effective_stat("speed"):
            if has_item("Sticky Web"):
                return ("use_item", "Sticky Web")
        if has_item("Power Elixir"):
                return ("use_item", "Power Elixir")
        if enemy.health / enemy.max_health < 0.35 and not has_item("Small Potion"):
                return "defend" if random.random() < 0.5 else "attack"
        return "attack"
      
    # Skeleton: aggressive, buffs, debuffs, burst
    if enemy.name == "Skeleton":
        if enemy.health / enemy.max_health < 0.3 and has_item("Small Potion"):
                return ("use_item", "Small Potion")
        if enemy.buffs["attack"] == 0 and has_item("Power Elixir"):
                return ("use_item", "Power Elixir")
        if player.get_effective_stat("speed") > enemy.get_effective_stat("speed") and has_item("Haste Potion"):
                return ("use_item", "Haste Potion")
        if player.player_class == "Warrior" and player.debuffs["attack"] == 0 and has_item("Hexdust"):
                return ("use_item", "Hexdust")
        
        # If buffed, attack to use burst window
        if enemy.buffs["attack"] > 0 or enemy.buffs["speed"] > 0:
             return "attack"
        if enemy.health / enemy.max_health < 0.3 and not has_item("Small Potion"):
             return "defend" if random.random() < 0.5 else "attack"
        return "attack"
          
    # Ghost: debuff-focused, glass cannon
    if enemy.name == "Ghost":
        if enemy.health / enemy.max_health < 0.3 and has_item("Medium Potion"):
            return ("use_item", "Medium Potion")
        # Debuff player if not already debuffed
        if player.debuffs["attack"] == 0 and has_item("Hexdust"):
             return ("use_item", "Hexdust")
        if player.debuffs["defense"] == 0 and has_item("Shadow Veil"):
             return ("use_item", "Shadow Veil")
        if player.get_effective_stat("speed") > enemy.get_effective_stat("speed") and player.debuffs["speed"] == 0 and has_item("Sticky Web"):
                  return ("use_item", "Sticky Web")
        # If player is debuffed, attack for max value
        if player.debuffs["attack"] > 0 or player.debuffs["defense"] > 0:
             return "attack"
        if enemy.health / enemy.max_health < 0.35 and not has_item("Medium Potion"):
             return "defend" if random.random() < 0.5 else "attack"
        return "attack"
    # Chimaera: all-rounder, buffs, debuffs, burst
    if enemy.name == "Chimaera":
         if enemy.health / enemy.max_health < 0.35 and has_item("Medium Potion"):
              return ("use_item", "Medium Potion")
         if player.get_effective_stat("speed") > enemy.get_effective_stat("speed") and enemy.buffs["speed"] == 0 and has_item("Haste Potion"):
              return ("use_item", "Haste Potion")
         if player.debuffs["speed"] == 0 and (player.player_class == "Hunter" or player.get_effective_stat("speed") > enemy.get_effective_stat("speed")) and has_item("Sticky Web"):
              return ("use_item", "Sticky Web")
         if enemy.buffs["attack"] == 0 and has_item("Power Elixir"):
              return ("use_item", "Power Elixir")
         # If buffed, attack for burst
         if enemy.buffs["attack"] > 0 or enemy.buffs["speed"] > 0:
              return "attack"
         if enemy.health / enemy.max_health < 0.35 and not has_item("Medium Potion"):
              return "defend" if random.random() < 0.3 else "attack"
         return "attack"

    # Sorcerer: debuff, burst, heal, cycle specials
    if enemy.name == "Sorcerer":
        if enemy.health / enemy.max_health < 0.35 and has_item("Medium Potion"):
                return ("use_item", "Medium Potion")
        if (player.get_effective_stat("attack") > 20 or player.get_effective_stat("speed") > 8) and player.debuffs["attack"] ==  0 and has_item("Cursed Ash"):
                return ("use_item", "Cursed Ash")
        if player.get_effective_stat("speed") > enemy.get_effective_stat("speed") and player.debuffs["speed"] == 0 and has_item("Frost Shard"):
                return ("use_item", "Frost Shard")
        # Use Fire Scroll for burst if player is debuffed or Sorcerer is buffed
        if has_item("Fire Scroll") and (player.debuffs["attack"] > 0 or player.debuffs["speed"] > 0):
                return ("use_item", "Fire Scroll")
        # Use Frost Shard if available and player not debuffed
        if has_item("Frost Shard") and player.debuffs["speed"] == 0:
                return ("use_item", "Frost Shard")
        # If debuffs are up, attack
        if player.debuffs["attack"] > 0 or player.debuffs["speed"] > 0:
             return "attack"
        if enemy.health / enemy.max_health < 0.35 and not has_item("Medium Potion"):
                return "defend" if random.random() < 0.5 else "attack"
        return "attack"
    
    # Golem: tanky, buffs, debuffs, burst, heal
    if enemy.name == "Golem":
        if enemy.health / enemy.max_health < 0.3 and has_item("Medium Potion"):
             return ("use_item", "Medium Potion")
        if enemy.buffs["defense"] == 0 and has_item("Stonewall Brew"):
             return ("use_item", "Stonewall Brew")
        if enemy.buffs["attack"] == 0 and has_item("Fury Draught"):
             return ("use_item", "Fury Draught")
        # Only debuff if player not already debuffed
        if player.debuffs["defense"] == 0 and has_item("Armour Piercer"):
             return ("use_item", "Armour Piercer")
        if player.get_effective_stat("speed") > enemy.get_effective_stat("speed") and enemy.buffs["speed"] == 0 and has_item("Lightning Elixir"):
             return ("use_item", "Lightning Elixir")
        # If buffed or player is debuffed, attack for burst
        if enemy.buffs["attack"] > 0 or player.debuffs["defense"] > 0:
             return "attack"
        if enemy.health / enemy.max_health < 0.35 and not has_item("Medium Potion"):
             return "defend" if random.random() < 0.3 else "attack"
        return "attack"
        
    # Knight Aberrant: tanky, buffs, debuffs, burst
    if enemy.name == "Knight Aberrant":
        if enemy.buffs["defense"] == 0 and has_item("Titan's Brew"):
                return ("use_item", "Titan's Brew")
        if (player.player_class == "Warrior" or player.get_effective_stat("defense") > 10) and has_item("Armour Piercer"):
                return ("use_item", "Armour Piercer")
        if player.get_effective_stat("speed") > enemy.get_effective_stat("speed") and enemy.buffs["speed"] == 0 and has_item("Lightning Elixir"):
                return ("use_item", "Lightning Elixir")
        if enemy.buffs["attack"] == 0 and has_item("Fury Draught"):
                return ("use_item", "Fury Draught")
        # If buffed or player is debuffed, attack for burst
        if enemy.buffs["attack"] > 0 or enemy.buffs["defense"] > 0 or player.debuffs["defense"] > 0:
             return "attack"
        return "defend" if random.random() < 0.45 else "attack"

    # Dragon: boss, burst, heal, aggressive
    if enemy.name == "Dragon":
        if enemy.health / enemy.max_health < 0.35 and has_item("Mega Elixir"):
                return ("use_item", "Mega Elixir")
        if enemy.buffs["attack"] == 0 and has_item("Bullhorn Brew"):
                return ("use_item", "Bullhorn Brew")
        if enemy.buffs["defense"] == 0 and has_item ("Titan's Brew"):
                return ("use_item", "Titan's Brew")
        if player.get_effective_stat("speed") > enemy.get_effective_stat("speed") and enemy.buffs["speed"] == 0 and has_item("Lightning Elixir"):
                return ("use_item", "Lightning Elixir")
        # Only use Fire Scroll if no attack buffs and no more Bullhorn Brew
        if enemy.buffs["attack"] == 0 and not has_item("Bullhhorn Brew") and has_item("Fire Scroll"):
             return ("use_item", "Fire Scroll")
        # If buffed, attack for burst
        if enemy.buffs["attack"] > 0 or enemy.buffs["defense"] > 0:
             return "attack"
        return "attack"
    
    # Default: attack or defend randomly
    return "attack" if random.random() < 0.75 else "defend"
         

def priority_action(action):
    return 1 if action == "defend" else 0

def grant_stat_boost(player):
    slow_text("You feel stronger after the battle...")

    if player.player_class == "Warrior":
        player.max_health += 12
        player.attack += 1
        player.defense += 2
        player.speed += 1

    elif player.player_class == "Mage":
        player.max_health += 8
        player.attack += 2
        player.defense += 1
        player.speed += 1

    elif player.player_class == "Hunter":
        player.max_health += 10
        player.attack += 2
        player.defense += 1
        player.speed += 2

    player.health = player.max_health
    slow_text(f"{GREEN}★ Your stats have increased and your health has been restored!{RESET}")
    print(f"{GREEN}♥ Max Health: {player.max_health} ⚔ Attack: {player.attack} 🛡 Defense: {player.defense} 💨 Speed: {player.speed}{RESET}")


    
def battle(player, enemy, stage_index):
        round_number = 1

        while player.is_alive() and enemy.is_alive(): # Loop until one of them is defeated
            # Display health of both after each turn
            clear_screen()
            print_divider()
            print(f"{CYAN}★ Round {round_number} ★{RESET}")
            print()
            display_health(player, enemy)
            print()
        

            slow_text("Choose your action: \n1. ⚔ Attack\n2. 🛡 Defend\n3. 🎒 Inventory")
            print()

            # Player chooses action
            while True:
                try:  
                    action = int(input("> ").strip())
                    print_divider()
                    if action not in [1, 2, 3]:
                        clear_screen()
                        slow_text("Invalid action! Please choose again.")
                        continue
                except ValueError:
                    clear_screen()
                    slow_text("Invalid input! Please enter a number")
                    continue

                item_to_use = None

                if action == 1:
                     player_action = "attack"
                     break

                elif action == 2:
                    player_action = "defend"
                    break

                elif action == 3:
                    usable_items = [item for item in player.inventory if items.get(item, {}).get("type") in ("heal", "buff", "debuff", "special")]
                    if not usable_items:
                        slow_text("You have no usable items!")
                        continue

                    item_counts = Counter(usable_items)
                    for idx, item in enumerate(item_counts, 1):
                         count = item_counts[item]
                         print(f"{idx}. {YELLOW}{item}{RESET} x{count} - {items[item]["description"]}")
                    use = input("Use an item? (type number or 'n'): ").strip()
                    if use.lower() == 'n':
                        continue
                    elif use.isdigit() and 1 <= int(use) <= len(usable_items):
                         player_action = "use_item"
                         item_to_use = list(item_counts.keys())[int(use) - 1]
                         break
                    else:
                        clear_screen()
                        slow_text("Invalid item! Try again.")
                        continue
            
            # Enemy chooses action using AI
            enemy_action_result = decide_enemy_action(enemy, player)
            if isinstance(enemy_action_result, tuple):
                enemy_action, enemy_item_to_use = enemy_action_result
            else:
                enemy_action = enemy_action_result
                enemy_item_to_use = None

            print_divider()
            if enemy_action == "use_item" and enemy_item_to_use:
                slow_text(f"{PURPLE}{enemy.name} uses {enemy_item_to_use}!{RESET}")
            else:
                slow_text(f"{CYAN}{enemy.name}'s action: {enemy_action.capitalize()}{RESET}")

            
            # Determine turn order: defend has prioirty, then speed
            actions = [
                 ((priority_action(player_action), player.get_effective_stat("speed")), player, enemy, player_action, item_to_use),
                   ((priority_action(enemy_action), enemy.get_effective_stat("speed")), enemy, player, enemy_action, enemy_item_to_use)
                ]

             # Sort by Speed, highest first
            actions.sort(reverse=True, key=lambda x: x[0])
            print()
            print(f"{CYAN}Turn order: {actions[0][1].name} → {actions[1][1].name}{RESET}\n")

            # Execute actions in order
            for _, actor, target, act, item in actions:
                if not actor.is_alive():
                    continue

                if act == "use_item":
                    execute_action(actor, target, act, item)
                else:
                    execute_action(actor, target, act)
                time.sleep(0.5)

            
            # Reset defend after turn
            player.is_defending = False
            enemy.is_defending = False


            # Check if player or enemy is defeated
            if not player.is_alive():
                slow_text(f"{RED}✖ You were defeated... ✖{RESET}")
                break

            elif not enemy.is_alive():
                slow_text(f"{enemy.name} has been defeated! {GREEN}You win! ✔{RESET}")
                reward_gold(player, enemy)
                print()
                if enemy.name == "Dragon":
                     slow_text("Congratulations! You've completed all stages!")
                     return # Skip shop/stat boost
                print(f"{CYAN}Preparing the shop...{RESET}")
                for i in range(3):
                    print(".", end='', flush=True) 
                    time.sleep(0.5)
                print("\n")
                shop(player, stage_index)
                print()
                grant_stat_boost(player)
                player.health = player.max_health # Reset health after the stage
                reset_buffs_debuffs(player)
                reset_buffs_debuffs(enemy)
                slow_text(f"{GREEN}You feel rested. Your health has been restored! {RESET}")
                break

            player.updated_stats()
            enemy.updated_stats()

            time.sleep(0.7)
            round_number += 1

def reward_gold(player, enemy):
    player.gold += enemy.gold_drop
    slow_text(f"{YELLOW}You've earned {enemy.gold_drop} gold! Total gold: {player.gold} {RESET}")

def create_player():
        name = input("Enter your character's name: ")
        
        slow_text("Choose your class:")
        slow_text("1. Warrior\n2. Mage\n3. Hunter")

        while True:
            choice = input("> ").strip()
            if choice == "1":
                player_class = "Warrior"
                player = Player(name, player_class)
                # Warrior: More HP & Defense, High Attack, stronger defend mechanic
                player.max_health = 120
                player.health = 120
                player.attack = 16
                player.defense = 8
                player.speed = 5
                player.inventory = ["Small Potion", "Haste Potion", "Sticky Web", "Power Elixir", "Iron Skin Tonic"]
                break
            elif choice == "2":
                player_class = "Mage"
                player = Player(name, player_class)
                # Mage: Balanced stats, has exclusive items
                player.max_health = 90
                player.health = 90
                player.attack = 15
                player.defense = 5
                player.speed = 7
                player.inventory = ["Small Potion", "Fire Scroll", "Fire Scroll", "Frost Shard", "Haste Potion"]
                break
            elif choice == "3":
                player_class = "Hunter"
                player = Player(name, player_class)
                # Hunter: High Speed, moderate Attack, can land critical hits
                player.max_health = 100
                player.health = 100
                player.attack = 14
                player.defense = 4
                player.speed = 10
                player.inventory = ["Small Potion", "Power Elixir", "Hexdust", "Sticky Web", "Haste Potion"]
                break
            else:
                slow_text("Invalid choice! Please choose 1, 2 or 3.")
        return player

def choose_game():
    while True:
        print("1. New Game")
        print("2. Load Game")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            player = create_player()
            return player, 0, False # Start at stage 0
        elif choice == "2":
            player, stage_index, post_battle = load_game()
            if player:
                slow_text(f"{GREEN}Welcome back, {player.name}!{RESET}")
                return player, stage_index, post_battle
            else:
                slow_text(f"No save file found. Starting a new game.")
                player = create_player()
                return player, 0, False
        else:
            clear_screen()
            slow_text("Invalid choice! Please choose again.")

# Save/load game using pickle
def save_game(player, stage_index, post_battle=False):
    with open("save_game.pkl", "wb") as s:
        pickle.dump((player, stage_index, post_battle), s)

def load_game():
    try:
        with open("save_game.pkl", "rb") as s:
            data = pickle.load(s)
            if len(data) == 3:
                return data # player, stage_index, post_battle
            else:
                player, stage_index = data
                return player, stage_index, False
    except FileNotFoundError:
        return None, 0, False


def shop(player, stage_index=0):
    slow_text("🏪 Welcome to the shop!")
    print_divider()
    while True:
        slow_text(f"{YELLOW}You have {player.gold} Gold.{RESET}")
        slow_text("\n Items for Sale: ")
        available_items = get_shop_items(stage_index)
        for name, info in items.items():
            if name not in available_items:
                 continue
            # Only show Mage exclusive items if the player is a Mage
            if info.get("exclusive") == "Mage" and getattr(player, "player_class", "") != "Mage":
                continue
            print(f"{YELLOW}{name}{RESET}: {info['price']}💰 - {info['description']}")
        
        print_divider()
        print()
        print("Options:\n- Type the item name to buy (you'll be asked for quantity)\n- Type 'inventory' to view your inventory\n- Type 'exit' to leave the shop.")
        print()

        choice = input("> ").strip()
        item_lookup = {name.lower(): name for name in available_items}

        if choice.lower() == "exit":
            slow_text("Come back anytime!")
            break

        elif choice.lower() == "inventory":
            view_inventory(player)

        elif choice.lower() in item_lookup:
            choice = item_lookup[choice.lower()]
            item = items[choice]
            if player.gold < item['price']:
                slow_text("Not enough Gold for that item!")
                continue
            while True:
                 qty_input = input(f"How many {choice}s would you like to buy? (type a number or '0' to cancel): ")
                 if qty_input.isdigit():
                      qty = int(qty_input)
                      if qty == 0:
                           slow_text("Purchase cancelled.")
                           break
                      total_price = item['price'] * qty
                      if player.gold >= total_price:
                           player.gold -= total_price
                           player.inventory.extend([choice] * qty)
                           slow_text(f"You have bought {qty} {choice}(s)! You have {player.gold} Gold left.")
                           print()
                           break
                      else:
                           slow_text("Not enough Gold for that many!")

                 else:
                      slow_text("Please enter a valid number.")
        else:
            slow_text("We don't have that item.")

shop_unlocks = [
     # Early game (Stages 1-2)
     ["Small Potion", "Power Elixir", "Iron Skin Tonic", "Haste Potion", "Hexdust", "Shadow Veil", "Sticky Web"],
     # Mid game (Stages 3-5)
     ["Medium Potion", "Fury Draught", "Stonewall Brew", "Gale Essence", "Cursed Ash", "Armour Piercer", "Fire Scroll", "Frost Shard"],
     # Late game (Stages 6-8)
     ["Mega Elixir", "Bullhorn Brew", "Titan's Brew", "Lightning Elixir"]
]

def get_shop_items(stage_index):
     items_available = []

     if stage_index < 2:
          for i in range(1):
               items_available.extend(shop_unlocks[i])
     elif stage_index < 5:
          for i in range(2):
               items_available.extend(shop_unlocks[i])
     else:
          for i in range(3):
               items_available.extend(shop_unlocks[i])
     return items_available

def view_inventory(player):
    print_divider()
    slow_text(f"{CYAN}🎒 Your inventory: {RESET}")
    if not player.inventory:
        slow_text("Your inventory is empty.\n")
    
    else:
        item_counts = Counter(player.inventory)
        for item, count in item_counts.items():
            desc = items[item]["description"] if item in items else ""
            print(f"{YELLOW}{item}{RESET}: x{count} - {desc}")
    print_divider()