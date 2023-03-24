class Location:
    def __init__(self, name, description, exits=None, items=None, monsters=None):
        self.name = name
        self.description = description
        self.exits = exits or {}
        self.items = items or []
        self.monsters = monsters or []

    def add_exit(self, direction, location):
        self.exits[direction] = location

    def add_item(self, item):
        self.items.append(item)

    def add_monster(self, monster):
        self.monsters.append(monster)
