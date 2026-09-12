#definicion de los diferentes tipos de entidades

LABOURERS = {
    "Man": {
        "texture_id": "entitys",
        "animations": {
            "idle": {
                "frames": [0],
                "interval": 0.3,
            },
            "walk_left": {
                "frames": [7,8,9,10,11,12,13],
                "interval": 0.2,
            },
            "walk_right": {
                "frames": [1,2,3,4,5,6],
                "interval": 0.2,
            },
            "walk_up": {
                "frames": [1,2,3,4,5,6],
                "interval": 0.3,
            },
            "walk_down": {
                "frames": [1,2,3,4,5,6],
                "interval": 0.3,
            },
            "work": {
                "frames": [9, 10],
                "interval": 4.0,
            },
        }
    },
    "Woman": {
        "texture_id": "entitys",
        "animations": {
            "idle": {
                "frames": [14],
                "interval": 0.3,
            },
            "walk_left": {
                "frames": [21,22,23,24,25,26,27],
                "interval": 0.3,
            },
            "walk_right": {
                "frames": [14,15,16,17,18,19,20],
                "interval": 0.3,
            },
            "walk_up": {
                "frames": [14,15,16,17,18,19,20],
                "interval": 0.3,
            },
            "walk_down": {
                "frames": [14,15,16,17,18,19,20],
                "interval": 0.3,
            },
            "work": {
                "frames": [8, 9,10,11,12],
                "interval": 0.3,
            },
        }
    }
}

SOLDIERS = {
    "Soldier": {
        "texture_id": "entitys",
        "animations": {
            "idle": {
                "frames": [0],
                "interval": 0.1,
            },
            "walk_left": {
                "frames": [1, 2],
                "interval": 0.1,
            },
            "walk_right": {
                "frames": [3, 4],
                "interval": 0.1,
            },
            "walk_up": {
                "frames": [5, 6],
                "interval": 0.1,
            },
            "walk_down": {
                "frames": [7, 8],
                "interval": 0.1,
            },
            "work": {
                "frames": [9, 10],
                "interval": 0.1,
            },
        }
    }
}

MACHINES = {
    # Tank {}
}
