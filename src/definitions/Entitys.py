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
                "frames": [11,12,13,14,15,16,17],
                "interval": 0.2,
            },
            "walk_right": {
                "frames": [0,1,2,3,4,5,6],
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
                "frames": [7,8,9],
                "interval": 0.3,
            },
        }
    },
    "Woman": {
        "texture_id": "entitys",
        "animations": {
            "idle": {
                "frames": [22],
                "interval": 0.3,
            },
            "walk_left": {
                "frames": [33,34,35,36,37,38,39],
                "interval": 0.3,
            },
            "walk_right": {
                "frames": [22,23,24,25,26,27,28],
                "interval": 0.3,
            },
            "walk_up": {
                "frames": [22,23,24,25,26,27,28],
                "interval": 0.3,
            },
            "walk_down": {
                "frames": [22,23,24,25,26,27,28],
                "interval": 0.3,
            },
            "work": {
                "frames": [29,30,31,32],
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
