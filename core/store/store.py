import random

stats = {
    "human": {'strength': 4, 'dexterity': 5, 'constitution': 5, 'intelligence': 6, 'wisdom': 6, 'charisma': 8},
    "elf": {'strength': 2, 'dexterity': 7, 'constitution': 3, 'intelligence': 7, 'wisdom': 7, 'charisma': 6},
    "dwarf": {'strength': 7, 'dexterity': 3, 'constitution': 5, 'intelligence': 3, 'wisdom': 3, 'charisma': 4},
    "wizard": {'strength': 3, 'dexterity': 5, 'constitution': 4, 'intelligence': 6, 'wisdom': 7, 'charisma': 5},
    "giant": {'strength': 9, 'dexterity': 2, 'constitution': 9, 'intelligence': 2, 'wisdom': 2, 'charisma': 3}
}

translations = {
    "human": "Человек",
    "elf": "Эльф",
    "dwarf": "Дварф",
    "wizard": "Волшебник",
    "giant": "Гигант",
    "dragon": "Дракон",
    "skeleton": "Скелет",
    "health_posion": "Зелье здоровья",
    "strength_posion": "Зелье силы"
}
enemies = {
    "dragon": {
        "defense": 16,
        "attack": 3,
        "health": 18

    },
    "skeleton": {
        "defense": 12,
        "attack": 1,
        "health": 5

    },
}
artefacts = {
    "health_posion": 2,
    "strength_posion": 1
}
locations = {
    "dungeon": {"description": "это маленькое подземелье, слабо освещено", "enemies": [(random.randint(1, 3), "skeleton")],
                "artefacts": set(random.choice(list(artefacts.keys())) for i in range(random.randint(1, 2)))}
}
