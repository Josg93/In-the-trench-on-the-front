from typing import Any, Dict

from gale.tilemap import load_tiled_map

import settings

class GameBattlefield():
    def __init__(self, map : str ) -> None:
        self.tilemap = load_tiled_map(settings.TILEMAPS[map])
        pass
    pass