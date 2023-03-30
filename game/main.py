import random

class Player:
    def __init__(self, name, character_class, level, hp, mp, attack, defense, spells, items):
        self.name = name
        self.character_class = character_class
        self.level = level
        self.hp = hp
        self.mp = mp
        self.attack = attack
        self.defense = defense
        self.spells = spells
        self.items = items

    def attack_enemy(self, enemy):
        damage = self.attack - enemy.defense
        if damage < 0:
            damage = 0
        enemy.hp -= damage
        print(f"{self.name} атакует {enemy.character_class}а и наносит {damage} урона")

    def use_spell(self, enemy):
        if len(self.spells) == 0:
            print(f"{self.name} не знает заклинаний")
            return
        spell = input("Какое заклинание использовать: ")
        if spell not in self.spells:
            print(f"{self.name} не знает такого заклинания")
            return
        spell_damage = random.randint(1, 10)
        enemy.hp -= spell_damage
        self.mp -= 1
        print(f"{self.name} использует заклинание {spell} и наносит {spell_damage} урона")

    def use_item(self, item):
        if len(self.items) == 0:
            print(f"{self.name} не имеет предметов")
            return
        if item not in self.items:
            print(f"{self.name} не имеет такого предмета")
            return
        self.items.remove(item)
        self.hp += 10
        print(f"{self.name} использует {item} и восстанавливает 10 единиц здоровья")

    def defend(self):
        self.defense += 2
        print(f"{self.name} защищается и повышает свою защиту на 2 единицы")

def start_game(players_count):
    print("Инициализация игры...")
    # Создание игроков
    players = []
    for i in range(players_count):
        name = input(f"Введите имя {i+1}-го игрока: ")
        character_class = input("Введите класс персонажа: ")
        level = 1
        hp = 20
        mp = 5
        attack = random.randint(1, 10)
        defense = 0
        spells = ["fireball", "ice bolt", "lightning strike"]
        items = ["potion", "elixir", "antidote"]
        player = Player(name, character_class, level, hp, mp, attack, defense,
                        spells, items)
        players.append(player)

        # Создание врага
    enemy = Player("Дракон", "Дракон", 1, 50, 10, 10, 5, [], [])

    print("Игра начинается!")
    return players, enemy


def game_turn(player, enemy):
    print(f"\nХод игрока {player.name}")
    print(f"Здоровье: {player.hp}")
    print(f"Мана: {player.mp}")
    print(f"Атака: {player.attack}")
    print(f"Защита: {player.defense}")
    print(f"Заклинания: {player.spells}")
    print(f"Предметы: {player.items}")

    action = input("Выберите действие: 1 - атака, 2 - использовать заклинание, 3 - использовать предмет, 4 - защита\n")
    if action == "1":
        player.attack_enemy(enemy)
    elif action == "2":
        player.use_spell(enemy)
    elif action == "3":
        item = input("Какой предмет использовать: ")
        player.use_item(item)
    elif action == "4":
        player.defend()
    else:
        print("Неверный ввод")

    if enemy.hp <= 0:
        print(f"{enemy.character_class} повержен!")
        return "win"

    enemy.attack_enemy(player)
    if player.hp <= 0:
        print("Игра окончена")
        return "lose"

    return "continue"