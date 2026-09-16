# CHANGELOG

## [0.6.0] - 2026-09-16
### Added
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
