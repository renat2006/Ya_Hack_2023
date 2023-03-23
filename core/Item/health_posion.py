from core.Item import Item


class HealingPotion(Item):
    def __init__(self):
        super().__init__(name="Зелье здоровья", description="Восстанавливает немного здоровья")

    def use(self, player):
        """Restore some of the player's hit points."""
        import random
        heal_amount = random.randint(5, 15)
        player.stats['hit_points'] += heal_amount
        print(f"{player.name} drinks a {self.name} and restores {heal_amount} hit points!")