# CHANGELOG

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