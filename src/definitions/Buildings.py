# Definición de edificios civiles y militares con parámetros de colisión personalizados (hitboxes parciales)
CIVIL_BUILDINGS = {
    "mill": {
        "texture_id": "buildings",
        "frame_index": 0,
        "width": 416,
        "height": 320,
        "collidable": True,
        "solid": True,
        # Definimos offset y tamaño reducido para que la parte superior/centro sea sólida
        # y la parte inferior (pasto) permita el tránsito de los labourers.
        "collision_offset_x": 40,
        "collision_offset_y": 80,
        "collision_width": 336,
        "collision_height": 200,
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
        "texture_id": "buildings",
        "frame_index": 2,
        "width": 128,
        "height": 128,
        "collidable": True,
        "solid": True,
    },
    "trench": {
        "texture_id": "buildings",
        "frame_index": 3,
        "width": 64,
        "height": 32,
        "collidable": True,
        "solid": True,
    },
}
