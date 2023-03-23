class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def use(self, player):
        """Do something when the item is used."""
        pass