# RPG Simulation Lite

RPG Simulation Lite is a turn-based combat game inspired by classic JRPGs like Dragon Quest. Play as a Warrior, Mage, or Hunter and battle through a series of unique enemies, using items, buffs, and strategy to win. The game is fully playable in the terminal/command line, written in Python.

---

## Features

- **Turn-based combat** with player and enemy actions.
- **Three player classes**: Warrior, Mage, Hunter, each with unique stats, starting items, defend and attack formula
- **Enemy variety**: Battle through different enemies, each with special AI and strategies.
- **Buffs & Debuffs**: Use items to boost your stats or weaken enemies.
- **In-game shop**: Spend gold earned in battle on useful items in the shop.
- **Inventory management**: Choose when to use healing, buff, debuff, or special items.
- **Save & Load**: Pick up where you left off.
- **Colorful UI**: ASCII/Unicode with colored text and health bars.

---

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/kebabti0/rpg-simulation-lite.git
    cd rpg-simulation-lite
    ```
    
3. **Run the game**:
    ```bash
    python main.py
    ```

   Requires Python 3.7+ (tested on Python 3.11+).

---

## How to Play

- **Start the Game**: Run `main.py` and follow the on-screen prompts.
- **Choose a Class**: Warrior (higher defend mitigation), Mage (exclusive items), or Hunter (crit in damage formula).
- **Battle Enemies**: Each enemy has different behaviours and item usage.
- **Actions**:
    - `1`: Attack
    - `2`: Defend (mitigates damage taken, 75% if Player picks "Warrior" class, else 50%)
    - `3`: Inventory (use potions, buffs, debuffs, special items)
- **Shop**: After each victory (except against the final boss), buy items with gold you’ve earned.
- **Saving/Loading**: After each battle, your progress is saved automatically. You can load your game from the main menu.

---

## Controls

- **During combat**: Enter the number of your chosen action.
- **Using inventory**: Select an item by number or type `n` to go back. (Upon incorrect input in inventory, please enter numbers 1-3 For 1. Attack, 2. Defend, 3. Inventory)
- **In shop**: Type the item name to buy, then specify the quantity, or type `inventory`/`exit`.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Credits & Inspiration

- Inspired by classic JRPGs, especially Dragon Quest.
- Developed by [kebabti0](https://github.com/kebabti0).
- Uses only standard Python, no external dependencies.

---

## Repository

- [@kebabti0/rpg-simulation-lite](https://github.com/kebabti0/rpg-simulation-lite)

---

Enjoy.
