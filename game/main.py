from core.Race import Race
from core.Player import Player
from core.store import stats
elf = Race("Elf", stats["elf"])
player = Player("Ренат", elf)
print(player.stats["strength"])