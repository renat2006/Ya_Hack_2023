from random import randint


class Player:
    def __init__(self, name, race):
        self.name = name
        self.race = race
        self.health = 10 + (race.stats["constitution"] + race.stats["strength"]) / 1.5
        self.stats = race.stats
        self.inventory = []

    def roll_dice(self, sides=6, num_dice=1):

        total = 0
        for i in range(num_dice):
            total += randint(1, sides)
        return total

    def attack(self, target):

        import random
        hit_roll = self.roll_dice(sides=20)
        if hit_roll >= target.armor_class:
            damage_roll = self.roll_dice(sides=self.race.damage_die)
            target.stats['hit_points'] -= damage_roll
            print(f"{self.name} hits {target.name} for {damage_roll} damage!")
        else:
            print(f"{self.name} misses {target.name}.")

    def add_item(self, item):

        self.inventory.append(item)

    def use_item(self, item):

        if item in self.inventory:
            item.use(self)
            self.inventory.remove(item)
        else:
            print(f"{self.name} does not have {item.name} in their inventory.")
