from game_display import *
from items import *
import random

# Base class for all characters (player and enemies)
class Character:
    def __init__(self, name, health, attack, defense, speed):
        # Basic stats
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        # Buffs and debuffs for each stat
        self.buffs = {"attack": 0, "defense": 0, "speed": 0}
        self.debuffs = {"attack": 0, "defense": 0, "speed": 0}
        self.buff_duration = {"attack": 0, "defense": 0, "speed": 0}
        self.debuff_duration = {"attack": 0, "defense": 0, "speed": 0}
        self.is_defending = False
        self.inventory = []

    # Handles attacking another character, including crits and defense
    def attack_enemy(self, enemy): 
        crit = False
        base_attack = self.get_effective_stat("attack")
        if isinstance(self, Player) and getattr(self, "player_class", "") == "Hunter":
            if random.random() < 0.25:
                base_attack *= 2
                crit = True
        # If enemy is defending, reduce damage based on class
        if enemy.is_defending:
            # Warrior and Knight Aberrant get 75% block, others 50%
            mitigation = 0.25 if (
                (isinstance(enemy, Player) and getattr(enemy, "player_class", "") == "Warrior") or
                (enemy.name == "Knight Aberrant")
            ) else 0.5
            damage = int((base_attack - enemy.get_effective_stat("defense")) * mitigation)
            damage = max(0, damage)
            enemy.is_defending = False # Reset enemy defense after attack
        else:
            damage = max(0, base_attack - enemy.get_effective_stat("defense"))

        enemy.health -= damage
        enemy.health = max(0, enemy.health)
        if crit:
            slow_text(f"{PURPLE}Critical hit!!{RESET}")
        slow_text(f"{RED}{self.name} attacks {enemy.name} for {damage} damage! {RESET}")

    # Sets defending state for this turn
    def defend(self):
        # Defend is a priority action, so it will be used first if the enemy or player chooses to defend and the other attack or inventory
        self.is_defending = True
        if isinstance(self, Player) and getattr(self, "player_class", "") == "Warrior" or self.name == "Knight Aberrant":
            slow_text(f"{CYAN}{self.name} is defending! Incoming damage will be reduced by 75%!{RESET}")
        else:
            slow_text(f"{CYAN}{self.name} is defending! Incoming damage will be reduced by 50%!{RESET}")
    
    # Handles using an item (buff, debuff, heal or special)
    def use_item(self, item_name, target=None):
        if not hasattr(self, "inventory") or item_name not in self.inventory: 
            slow_text(f"{RED}{self.name} has no {item_name}{RESET}!")
            return False
        
        item = items.get(item_name) 
        if not item:
            slow_text("Invalid item!")
            return False
        
        # Mage special items can only be used by the Mage
        if item_name == "Fire Scroll":
            if target is None:
                slow_text("No target to use Fire Scroll on!") # just for safety
                return False
            damage = item.get("damage", 0)
            target.health -= damage
            target.health = max(0, target.health)
            slow_text(f"{PURPLE}{self.name} uses Fire Scroll! {target.name} takes {damage} damage!{RESET}")

        elif item_name == "Frost Shard":
            if target is None:
                slow_text("No target to use Frost Shard on!")
                return False
            damage = item.get("damage", 0)
            speed_debuff = item.get("speed_debuff", 0)
            duration = item.get("duration", 3)
            target.health -= damage
            target.health = max(0, target.health)
            slow_text(f"{PURPLE}{self.name} uses Frost Shard! {target.name} takes {damage} damage and speed is reduced by {speed_debuff} for {duration} turns!{RESET} ")
            # Only apply debuff if not already at max
            if target.debuffs["speed"] < 2 * speed_debuff:
                target.debuffs["speed"] += speed_debuff
                target.debuff_duration["speed"] = duration + 1
            else:
                slow_text(f"{target.name}'s speed is already at maximum debuff!")

        elif item.get("type") == "heal":
            heal_amount = item.get("heal_amount", 0)
            self.health += heal_amount
            self.health = min(self.max_health, self.health)
            slow_text(f"{GREEN}{self.name} uses {item_name}!")

        elif item.get("type") == "buff":
            for stat in ["attack", "defense", "speed"]:
                if f"{stat}_boost" in item:
                    boost = item[f'{stat}_boost']
                    # Only buff if not already at max
                    if self.buffs[stat] < 2 * boost: # Max 2 buffs per stat
                        self.buffs[stat] += boost
                        self.buff_duration[stat] = item["duration"] + 1 
                        slow_text(f"{GREEN}{self.name}'s {stat} increased by {boost} for {item["duration"]} turns!{RESET}")
                    else:
                        slow_text(f"{self.name}'s {stat} is already at maximum buff!")
                    break

        elif item.get("type") == "debuff":
            for stat in ["attack", "defense", "speed"]:
                if f"{stat}_debuff" in item:
                    debuff = item[f'{stat}_debuff']
                    # Only debuff if not already at max
                    if target.debuffs[stat] < 2 * debuff:
                        target.debuffs[stat] += debuff
                        target.debuff_duration[stat] = item["duration"] + 1
                        slow_text(f"{RED}{target.name}'s {stat} decreased by {debuff} for {item["duration"]} turns!{RESET}")
                    else:
                        slow_text(f"{target.name}'s {stat} is already at maximum debuff!")
                    break
        
        else:
            slow_text("This item cannot be used.")
            return False
        
        self.inventory.remove(item_name) 
        return True

    # Returns the stat value after buffs and debuffs
    def get_effective_stat(self, stat):
        base = getattr(self, stat)
        buff = self.buffs.get(stat, 0)
        debuff = self.debuffs.get(stat, 0)
        result = max(0, base + buff - debuff)
        return result
    
    # Returns True if character is alive
    def is_alive(self):
        return self.health > 0
    
    # Returns current speed (used for turn order)
    def get_speed(self):
        return self.speed
    
    # Updates buff/debuff durations each turn and removes them if expired
    def updated_stats(self):
        for stat in self.buff_duration:
            if self.buff_duration[stat] > 0:
                self.buff_duration[stat] -= 1
                if self.buff_duration[stat] == 0:
                    self.buffs[stat] = 0
                    slow_text(f"{YELLOW}{self.name}'s {stat} buff has worn off!{RESET}")

        for stat in self.debuff_duration:
            if self.debuff_duration[stat] > 0:
                self.debuff_duration[stat] -= 1
                if self.debuff_duration[stat] == 0:
                    self.debuffs[stat] = 0
                    slow_text(f"{YELLOW}{self.name}'s {stat} debuff has worn off!{RESET}")

# Player class, inherits from Character
class Player(Character):
    def __init__(self, name, player_class):
        super().__init__(name, 1, 1, 1, 1) #Initialize base Character with placeholder stats (real stats set after class selection)
        self.player_class = player_class
        self.inventory = []
        self.gold = 0
       
# Enemy class, inherits from Character
class Enemy(Character):
    def __init__(self, name, health, attack, defense, speed, gold_drop, inventory):
        super(). __init__(name, health, attack, defense, speed)
        self.gold_drop = gold_drop
        self.inventory = inventory
        
    def __str__(self): # String representation of the character
        return f"{self.name}: Health: {self.health}, Attack: {self.attack}, Defense: {self.defense}, Speed: {self.speed}"