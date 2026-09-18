# In the Trench on the Front

A tactical 2D strategy and defense video game built with **Python**, **Pygame**, and the **Gale Engine**. Command your labourers and soldiers, manage resources, build and garrison trenches, and survive the onslaught of enemy waves on the front lines.

---

## Features

- **Unit Management & Selection:**
  - Click-to-select individual units or click-and-drag to draw selection boxes.
  - Automatic deselection of previous units when selecting new groups or units.
- **Economy & Resource Gathering:**
  - Train **Labourers** to harvest food/wheat from mills to sustain your population and fund new units.
- **Military & Trench Warfare:**
  - Construct **Barracks** to enable soldier recruitment.
  - Train **Soldiers** and assign them to **Trenches**. Soldiers pathfind to trench doors, tween inside to fight and take cover, and exit smoothly when commanded.
- **Dynamic A\* Navigation & Pathfinding:**
  - Real-time pathfinding across the battlefield using A\*.
  - Automatic graph reconstruction when buildings or trench ruins are destroyed, preventing units from getting stuck.
- **Progressive 5-Wave Combat System:**
  - Survive up to 5 increasingly difficult enemy waves with preparation timers, wave tracking, and victory/defeat states.
- **Advanced Combat & Movement AI:**
  - Persistent target tracking, post-combat state restoration, and anti-jitter movement debouncing.
  - Unit-to-unit collision resolution to prevent stacking.

---

## Tech Stack

- **Language:** Python 3.10+
- **Library/Framework:** Pygame, Gale Engine (`gale-engine`)

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/in-the-trench-on-the-front.git
   cd "in the trench on the front"
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Game

To launch the game, run:
```bash
python main.py
```

---

## Controls

- **Left Click & Drag:** Draw selection box over allied units.
- **Left Click on Unit:** Select a single unit.
- **Right Click / Move Command:** Order selected units to move to a location, enter trenches, or interact with structures.
- **UI Panel:** Click buttons on the bottom control panel to train Labourers (100 food) or Soldiers (200 food, requires Barracks).

---

## Project Structure

```text
in the trench on the front/
├── assets/                  # Graphics, fonts, tilemaps, and audio
├── src/                     # Source code package
│   ├── definitions/         # Building and entity data definitions
│   ├── mixins/              # Drawable, collidable, and animated mixins
│   ├── states/              # Game states (Menu, Play, Victory, Defeat) & entity states
│   ├── GameBattlefield.py   # Main battlefield and pathfinding manager
│   ├── GameBuilding.py      # Building and trench logic
│   ├── GameEntity.py        # Base entity movement and AI logic
│   ├── Labourer.py          # Labourer / economic unit logic
│   └── Soldier.py           # Soldier combat and trench integration logic
├── main.py                  # Entry point
├── requirements.txt         # Dependencies
└── CHANGELOG.md             # Version history
```

---

## License

This project is developed as part of a university video game programming course.
