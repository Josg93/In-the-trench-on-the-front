# CHANGELOG

## [0.6.0] - 2026-09-16
### Added
- **Dynamic Navigation Graph (`GameBattlefield.py`):** Automatic reconstruction of the A* navigation graph (`build_graph()`) when any building or trench is destroyed, allowing advancing enemy waves (e.g., wave 2) to pass smoothly through destroyed trench ruins without getting stuck.
- **Fair 5-Wave System (`PlayState.py`):** Implemented a complete wave progression system with a 30s initial preparation countdown, up to 5 progressive enemy waves, and automatic wave clearance tracking (next wave only starts when all current wave enemies are defeated, leading to a victory screen on wave 5 completion).
- **Enhanced Wave & Combat HUD Panel:** Updated the UI panel in `PlayState` to display current wave progress (`Wave X / 5`), countdown timers, remaining enemy counts, and victory status.
- **Precise Trench Slot Navigation:** Soldiers now pathfind and walk all the way directly to their exact assigned interior work slot (`slot["pos"]`) inside trenches rather than prematurely triggering via outer collision rect bounds.
- **Trench Entry & Exit System:** Soldiers assigned to trenches now pathfind to the nearest entrance door (`get_left_door()` / `get_right_door()`), transition smoothly via `gale.timer.Tween` into trench slots, continue fighting/taking damage while inside, and smoothly tween back out to doors when commanded to move elsewhere.
- **Drag-to-Select Box Selection:** Players can now click and drag on the screen to draw a selection box, selecting multiple allied units at once with a translucent selection rectangle rendered on screen.
- **Barracks Requirement:** Implemented a validation check ensuring allied soldiers can only be generated when at least 1 allied `barracks` building exists.
- **Centralized Combat AI & Target Persistence:** Refactored combat logic into `Soldier.py`, eliminating target oscillation when enemies are at equal distances by making soldiers persist on their chosen target until death.
- **Post-Combat Re-tasking:** Enemy soldiers automatically resume marching toward the map objective (`x = 0`) after eliminating their opponents.
- **Accurate Post-Combat State Restoration:** Soldiers now preserve their exact pre-combat activity state (`idle` or `walk`), returning cleanly to idle when stationary or resuming walking with their waypoints intact once their target is defeated.
- **Advanced Movement Throttling & Debouncing:** Implemented delta-time accumulation timers (`direction_timer`) and state-change debouncing (0.15s interval) in `GameEntity.movement()` to eliminate unit jitter, convulsive direction switching, and animation frame resetting at 60 FPS.
- **Unit-to-Unit Collision & Separation System:** Implemented circular radius-based collision detection and push-apart resolution between entities (`GameEntity._resolve_unit_collisions()`) to prevent units from solapamiento (overlapping) or stacking on top of each other.
- **Optimized Waypoint Arrival Threshold:** Increased arrival threshold to 10.0px to prevent floating-point oscillation near target destinations.

### Fixed
- Fixed issue where subsequent enemy waves (wave 2+) got stuck at destroyed trench ruins due to static, un-updated A* navigation graphs.
- Fixed `AttributeError` / `TypeError` (`NoneType`) when clicking or issuing movement commands with no units selected or interacting with trenches without an active unit reference (`get_distance` and `move_entity` safeguards).
- Fixed premature trench entry teleportation where soldiers snapped to slots before reaching the end of their waypoints.
- Fixed `AttributeError` (`'KeyboardData' object has no attribute 'position'`) when pressing `ENTER` in `PlayState`.
- Fixed `AttributeError` (`'Trench' object has no attribute 'x'`) by correcting initialization order in `Trench.__init__` (`super().__init__()` runs before defining `work_slots`).
- Removed duplicate and conflicting enemy combat loop from `PlayState.update()`.

## [0.5.0] - 2026-09-15
### Added
- Entity-Building interaction system: Labourers can now be assigned to buildings (specifically the Mill) via work slots surrounding the structure.
- Fade-in / Fade-out transition effects between game states using `gale.timer.Tween`.
- Histéresis-based direction change logic to prevent animated sprite flickering.
- Removal of separation/flocking forces between entities to eliminate convulsive movement.
- Bug fixes: corrected slot assignment logic, fixed entity positioning to waypoints (center vs top-left), and centralized work activation in `GameEntity`.

### Changed
- Refactored `PlayState` to remove duplicate work-activation logic, centralizing it in `GameEntity.movement()`.
- Updated `GameBuilding` to manage peripheral `work_slots` for entity assignment.
- Improved collision resolution for entity-slot interaction.

### Fixed
- Labourers staying idle when assigned to a building (pathfinding to center blocked).
- Slot duplication on re-assignment of labourers to the same building.
- Entity direction convulsions/jitter during movement.
- Flickering animation state changes when moving diagonally.

---
