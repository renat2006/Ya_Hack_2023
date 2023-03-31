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
    "strength_posion": "Зелье силы",
    "loupgarou": "Лугару",
    "dragon_amulet": "Драконий Амулет"
}
hero_description = {
    "human": "человек, готовый защищать свою семью и соратников, даже ценой своей жизни",
    "elf": "древесный эльф, чей род славится свой ловкостью и мудростью",
    "dwarf": "дварф, чей рост не мешает ему расправляться с полчищами монстров",
    "wizard": "волшебник, чьи заклинания наводят ужас на врагов",
    "giant": "гигант, при виде которого, противники разбегаются в страхе"
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
    "loupgarou": {
        "defense": 14,
        "attack": 1,
        "health": 10

    },
}

artefact_effects = {
    "health_posion": [(1, "health")],
    "strength_posion": [(1, "strength")],
    "dexterity_posion": [(1, "dexterity")],
    "dragon_amulet": [(1, "dexterity"), (1, "strength")]

}

locations = {
    "dungeon": {"description": "это маленькое подземелье, слабо освещено",
                "enemies": [(3, "skeleton"), (1, "loupgarou")],
                "artefacts": [(10, "health_posion")], "max_artefacts": 2, "prehistory": "test1"},
    "treasury": {"description": "это сокровищница", "enemies": [(2, "skeleton")],
                 "artefacts": [(10, "health_posion"), (5, "strength_posion"), (5, "dexterity_posion"),
                               (1, "dragon_amulet")],
                 "max_artefacts": 4, "prehistory": "test2"},
    "forest": {"description": "....", "enemies": [(2, "skeleton")],
               "artefacts": [(10, "health_posion"), (5, "strength_posion"), (5, "dexterity_posion"),
                             (1, "dragon_amulet")],
               "max_artefacts": 4, "prehistory": "test3"},
    "desert": {"description": "....", "enemies": [(2, "skeleton")],
               "artefacts": [(10, "health_posion"), (5, "strength_posion"), (5, "dexterity_posion"),
                             (1, "dragon_amulet")],
               "max_artefacts": 4, "prehistory": "test4"},
    "ice_world": {"description": "....", "enemies": [(2, "skeleton")],
                  "artefacts": [(10, "health_posion"), (5, "strength_posion"), (5, "dexterity_posion"),
                                (1, "dragon_amulet")],
                  "max_artefacts": 4, "prehistory": "test5"},
    "castle": {"description": "....", "enemies": [(2, "skeleton")],
               "artefacts": [(10, "health_posion"), (5, "strength_posion"), (5, "dexterity_posion"),
                             (1, "dragon_amulet")],
               "max_artefacts": 4, "prehistory": "test6"}
}
