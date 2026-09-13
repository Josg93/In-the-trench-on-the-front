# Definición de edificios civiles y militares con parámetros de colisión personalizados (hitboxes parciales)
CIVIL_BUILDINGS = {
    "mill": {
        "texture_id": "buildings",
        "frame_index": 0,
        "width": 416,
        "height": 320,
        "collidable": True,
        "solid": True,
        "collision_offset_x": 130,
        "collision_offset_y": 150,
        "collision_width": 152,
        "collision_height": 71.4,
    },
    "town": {
        "texture_id": "buildings",
        "frame_index": 1,
        "width": 128,
        "height": 128,
        "collidable": True,
        "solid": True,
    },
}

MILITARY_BUILDINGS = {
    "barracks": {
        "texture_id": "barracks",
        "frame_index": 0,
        "width": 347,
        "height": 321,
        "collidable": True,
        "solid": True,
    },
    "trench": {
        "texture_id": "trench",
        "frame_index": 0,
        "width": 384,
        "height": 672,
        "collidable": True,
        "solid": True,
    },
}
