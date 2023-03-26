import random


class Enemy:
    def __init__(self, name, stats):
        self.name = name
        self.stats = stats[name]

