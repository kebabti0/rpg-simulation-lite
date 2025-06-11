from game_display import *
from characters import *
from enemies import *
from game_logic import *

def start_screen():
    width = 31
    print(f"{CYAN}")
    print("╔" + "═" * width + "╗")
    print("║" +    "RPG SIMULATION LITE".center(width)  + "║")
    print("║" +    "Turn-Based Combat".center(width) + "║")
    print("╚" + "═" * 31 + "╝")
    print(f"{RESET}")
    input("Press Enter to start the game...")

# Main function to run the game
def main():
    start_screen()
    slow_text("Welcome to the RPG Simulation Lite!")
    slow_text(f"{YELLOW}Defeat all enemies in turn-based battles. Use your items and strategy to win each stage!{RESET}")
    slow_text(f"{CYAN}Experiment with buffs, debuffs etc to beat your opponents.{RESET}")
    player, stage_index, post_battle = choose_game()

    while stage_index < len(enemy_order):
        if not post_battle:
            enemy = create_enemy(stage_index)
            # Save inventory before battle
            inventory_backup = list(player.inventory)
            battle(player, enemy, stage_index)

            if not player.is_alive():
                retry = input("You were defeated! Try again? (y/n): ").lower()
                if retry == "y":
                    player.health = player.max_health
                    player.inventory = list(inventory_backup) # Restore inventory, incase player loses and tries again
                    continue  # Restart the stage
                else:
                    slow_text("Thanks for playing!")
                    return  # Exit the game
            post_battle = True
            save_game(player, stage_index, post_battle)

        # Recreate enemy for post-battle menu if needed
        if post_battle and stage_index < len(enemy_order):
            enemy = create_enemy(stage_index)

        while post_battle and stage_index < len(enemy_order):
            slow_text("What do you want to do next? ")
            if stage_index < len(enemy_order) - 1:
                # Any stage except the last one
                slow_text("1. Continue to next stage")
                slow_text(f"2. Fight {enemy.name} again")
                slow_text("3. Exit the game")
                choice = input("> ").strip()
                if choice == "1":
                    stage_index += 1
                    post_battle = False
                    if stage_index < len(enemy_order):
                        slow_text(f"Moving to stage {stage_index + 1}...")
                        save_game(player, stage_index, post_battle)
                    break
                elif choice == "2":
                    post_battle = False
                    save_game(player, stage_index, post_battle)
                    break
                elif choice == "3":
                    save_game(player, stage_index, post_battle)
                    slow_text("Thanks for playing!")
                    return
                else:
                    clear_screen()
                    slow_text("Invalid choice. Please try again.")
            else:
                # Last boss defeated
                slow_text("1. Retry the game")
                slow_text("2. Exit the game")
                choice = input("> ").strip()
                if choice == "1":
                    stage_index = 0
                    player = create_player()
                    post_battle = False
                    continue
                elif choice == "2":
                    slow_text("Thanks for playing!")
                    save_game(player, stage_index, post_battle)
                    break
                else:
                    clear_screen()
                    slow_text("Invalid choice. Please try again.")
                    
# Run the main function to start the game
if __name__ == "__main__":  
    main() 
