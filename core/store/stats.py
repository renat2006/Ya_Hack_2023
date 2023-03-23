import json

stats = {
    "human": {'strength': 4, 'dexterity': 5, 'constitution': 5, 'intelligence': 6, 'wisdom': 6, 'charisma': 8},
    "elf": {'strength': 2, 'dexterity': 7, 'constitution': 3, 'intelligence': 7, 'wisdom': 7, 'charisma': 6},
    "dwarf": {'strength': 8, 'dexterity': 3, 'constitution': 5, 'intelligence': 3, 'wisdom': 3, 'charisma': 4}
}

races_translation = {
    "human": "Человек",
    "elf": "Эльф",
    "dwarf": "Дварф"
}


def return_stats(key):
    return stats[str(key)]


if __name__ == "__main__":
    with open('stats.json', 'w') as f:
        json.dump(stats, f)
