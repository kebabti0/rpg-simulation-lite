import os
import time

# ANSI colour codes for coloured terminal texts
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
PURPLE = "\033[95m"
RESET = "\033[0m"

# Clear terminal screen for readability (works on Windows and Unix)
def clear_screen():
     os.system('cls' if os.name == 'nt' else 'clear')

# Prints text slowly for typical JRPG-effect
def slow_text(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def print_divider():
    print(CYAN + "\n" + "=" * 40 + "\n" + RESET)

def get_health_colour(character):
    health_ratio = character.health / character.max_health
    if health_ratio > 0.6:
        return GREEN
    elif health_ratio > 0.3:
        return YELLOW
    else:
        return RED

def display_health(player, enemy):
    max_name_len = max(len(player.name), len(enemy.name), 12)
    print(f"{CYAN}Player:{RESET}")
    health = player.health
    max_health = player.max_health
    total_bars = 20 
    filled_bars = int((health / max_health) * total_bars)
    empty_bars = total_bars - filled_bars
    health_bar = "█" * filled_bars + "-" * empty_bars
    colour = get_health_colour(player)
    name_field = player.name.ljust(max_name_len)
    print(f"{colour}{name_field}  ♥  [ {health_bar} ]   {str(health).rjust(3)}/{str(max_health).ljust(3)}{RESET}")

    print(f"{CYAN}Enemy:{RESET}")
    health = enemy.health
    max_health = enemy.max_health
    filled_bars = int((health / max_health) * total_bars)
    empty_bars = total_bars - filled_bars
    health_bar = "█" * filled_bars + "-" * empty_bars
    colour = get_health_colour(enemy)
    name_field = enemy.name.ljust(max_name_len)
    print(f"{colour}{name_field}  ♥  [ {health_bar} ]   {str(health).rjust(3)}/{str(max_health).ljust(3)}{RESET}")

