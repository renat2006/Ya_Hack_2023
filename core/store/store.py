stats = {
    "human": {'strength': 5, 'dexterity': 5, 'constitution': 5, 'intelligence': 6, 'wisdom': 6, 'charisma': 8,
              'health': 15, "abilities": "shield"},
    "elf": {'strength': 3, 'dexterity': 7, 'constitution': 3, 'intelligence': 7, 'wisdom': 7, 'charisma': 6,
            'health': 13, "abilities": "fast"},
    "dwarf": {'strength': 7, 'dexterity': 3, 'constitution': 5, 'intelligence': 3, 'wisdom': 3, 'charisma': 4,
              'health': 17, "abilities": "super"},
    "wizard": {'strength': 4, 'dexterity': 5, 'constitution': 4, 'intelligence': 6, 'wisdom': 7, 'charisma': 5,
               'health': 14, "abilities": "healing"},
    "giant": {'strength': 9, 'dexterity': 2, 'constitution': 9, 'intelligence': 2, 'wisdom': 2, 'charisma': 3,
              'health': 22, "abilities": "smash"}
}
hero_attack_prompt = {
    "human": {
        "usual": ["твой меч наносит хлёсткий удар в облать груди",
                  "ты бьёшь врага кулаком со всей силы и видишь как он корчится от боли"],
        "missed": ["к сожалению, твой меч проходит где-то около врага, тебе не удалось попасть по нему"],
        "last": ["смотря, как монстр молит о пощаде, ты отсекаешь ему голову быстрым и резким ударом меча"]

    },
    "elf": {
        "usual": ["стрела твоего лука попадает точно в цель",
                  "твои навыки стрельбы тебя ещё никогда не подводили, ты попал"],
        "missed": ["стрела, выписывая пируэты в воздухе пролетает где-то мимо"],
        "last": [
            "ты быстро подбигаешь к монстру, нанося несколько быстрых ударов клинком по жизненно-важным органам, монстр медленно умирает"]

    },
    "dwarf": {"usual": ["твой топор с размаху бьёт по врагу, попадая прямя по плечу"],
              "missed": ["От твоего топора отлетает искра, он проходит недалеко от врага, задевая его броню"],
              "last": [
                  "ты стоишь и глумишься над беспомощностью этого монста, а потом добиваешь его сильным ударом топора"]},
    "wizard": {"usual": ["Струя магического посоха пронизывает противника"],
               "missed": ["Цель была невосприимчива к такому действию"],
               "last": [
                   "бездыханное тело монстра падает на землю"]},
    "giant": {"usual": ["мощным ударом руки ты откидываешь монстра"],
              "missed": ["монстр успел уклониться от твоего удара"],
              "last": [
                  "последним ударом ты останавливаешь жизнь этого существа"]}
}
abilities = {
    "healing": {
        "description": "Эта способность лечит всех твоих союзников",
        "usage_prompt": "Твой магический посох пополняет здоровье всех игроков",

        "type": "heal_all",
        "max_effect": 2

    },
    "smash": {
        "description": "Эта способность оглушает врагов на один ход",
        "usage_prompt": "Враги падают с ног после твоего удара по земле",
        "type": "stun_all",
        "max_effect": 1
    },
    "fast": {
        "description": "Эта способность наносит всем врагам 3 урона",
        "usage_prompt": "Твои стрелы пронзили противников",
        "type": "attack_all",
        "max_effect": 3
    },
    "shield": {
        "description": "Эта способность делает тебя невосприимчивым к урону на два хода",
        "usage_prompt": "Ты встал в стойку с щитом",
        "type": "attack_block",
        "max_effect": 2
    },
    "super": {
        "description": "Эта способность наносит 15 урона противнику",
        "usage_prompt": "Враг был разрублен пополам",
        "type": "attack",
        "max_effect": 15
    }

}
translations = {
    'strength': 'Сила', 'dexterity': 'Ловкость', 'constitution': 'Массивность', 'intelligence': 'Внимательность',
    'wisdom': 'Мудрость', 'charisma': 'Харизма', 'health': "Здоровье",
    "human": "Человек",
    "elf": "Эльф",
    "dwarf": "Дварф",
    "wizard": "Волшебник",
    "giant": "Гигант",
    "dragon": "Дракон",
    "skeleton": "Скелет",
    "health_posion": "Зелье здоровья",
    "strength_posion": "Зелье силы",
    "dexterity_posion": "Зелье ловкости",
    "loupgarou": "Лугару",
    "troll": "Тролль",
    "spider": "Паук",
    "dragon_amulet": "Драконий Амулет",
    "sands_of_time": "Пески времени",
    "crown_of_mind": "Корона разума",
    "pardise_flower": "Райский цветок",
    "death_worm": "Песчанный червь",
    "zimogor": "Зимогор",
    "ghost": "Призрак",
    "healing": "Лечение природы",
    "smash": "Минута молчания",
    "fast": "Быстрее света",
    "shield": "Живой щит",
    "super": "Сокрушающий удар Саурона"
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
    "troll": {
        "defense": 10,
        "attack": 2,
        "health": 6

    },
    "spider": {
        "defense": 9,
        "attack": 1,
        "health": 8

    },
    "death_worm": {
        "defense": 12,
        "attack": 2,
        "health": 14

    },
    "zimogor": {
        "defense": 10,
        "attack": 1,
        "health": 11

    },
    "ghost": {
        "defense": 10,
        "attack": 1,
        "health": 7

    }
}
enemies_attack_prompt = {
    "usual": ["бьёт по тебе что есть мочи", "с разбегу врезается в тебя", "прыгает на тебя"],
    "missed": ["ударяет со всей силы,  но промахивается"],
    "last": ["добивает тебя, нанося решающий удар"]
}
artefact_effects = {
    "health_posion": [(1, "health")],
    "strength_posion": [(1, "strength")],
    "dexterity_posion": [(1, "dexterity")],
    "dragon_amulet": [(2, "dexterity"), (1, "strength")],
    "gemstone": [(1, "dexterity"), (2, "strength")],
    "sands_of_time": [(4, "strength")],
    "crown_of_mind": [(2, "strength"), (3, "dexterity")],
    "pardise_flower": [(2, "health")]

}
artefact_type = {
    "health_posion": "temporary",
    "strength_posion": "temporary",
    "dexterity_posion": "temporary",
    "dragon_amulet": "all_time",
    "gemstone": "all_time",
    "sands_of_time": "all_time",
    "crown_of_mind": "all_time",
    "pardise_flower": "temporary""temporary"
}
locations_data_files = {
    "dungeon": {
        "sound": '<speaker audio="dialogs-upload/187f71d1-318e-40e1-9000-547de379a961/0a7826e5-7e13-4188-adfc-1714b24b85f3.opus">',
        "image": "https://i.postimg.cc/63qT8BSm/dungeon.jpg"
    },
    "treasury": {
        "sound": '<speaker audio="dialogs-upload/187f71d1-318e-40e1-9000-547de379a961/f61f874f-6f61-4ac8-966f-8002c04971eb.opus">',
        "image": "https://i.postimg.cc/5tLq0qhr/treasuary.jpg"},
    "forest": {
        "sound": '<speaker audio="dialogs-upload/187f71d1-318e-40e1-9000-547de379a961/cfbb5272-e294-4970-8889-b0e16f0642fc.opus">',
        "image": "https://i.postimg.cc/LX4Ypt2L/forest.jpg"},
    "desert": {
        "sound": '<speaker audio="dialogs-upload/187f71d1-318e-40e1-9000-547de379a961/96d61279-180b-450c-97eb-e96ac3bd9e16.opus">',
        "image": "https://i.postimg.cc/W1KJ0FmP/desert.jpg"},
    "ice_world": {
        "sound": '<speaker audio="dialogs-upload/187f71d1-318e-40e1-9000-547de379a961/77b017c8-8f8e-4168-8434-732ebaaf012e.opus">',
        "image": "https://i.postimg.cc/v8N1Jxjx/ice-world.jpg"},
    "castle": {
        "sound": '<speaker audio="dialogs-upload/187f71d1-318e-40e1-9000-547de379a961/8d8ca0b7-00d8-43d6-a156-d1c9ed91a1bc.opus">',
        "image": "https://i.postimg.cc/pLDp5GdK/castle.jpg"}
}
locations = {
    "dungeon": {"description": "это маленькое подземелье, слабо освещено",
                "enemies": [(2, "skeleton"), (1, "loupgarou")],
                "artefacts": [(5, "health_posion"), (3, "strength_posion")], "max_artefacts": 2,
                "prehistory": "После нескольких дней блужданий по пустоши ваша команда находит вход в подземелье. Вот и начало вашего непростого пути. Вы спускаетесь в темную пещеру."},
    "treasury": {"description": "это сокровищница", "enemies": [(2, "skeleton"), (1, "dragon")],
                 "artefacts": [(6, "health_posion"), (2, "strength_posion"), (3, "dexterity_posion"),
                               (1, "dragon_amulet")],
                 "max_artefacts": 5,
                 "prehistory": "После боя команда находит выход из подземелья с драконами. Крушение стены привело их в длинный коридор. Нежданно-негаданно, команда обнаружила проход в сокровищницу. Как только они вошли в темную комнату, им стало ясно, что они здесь не одни."},
    "forest": {"description": "это темный лес, который таит в себе секреты",
               "enemies": [(2, "skeleton"), (1, "troll"), (2, "spider")],
               "artefacts": [(3, "health_posion"), (4, "pardise_flower"), (2, "dexterity_posion"), (3, "gemstone")],
               "max_artefacts": 3,
               "prehistory": "После получения артефактов вы проходите через одну из комнат, которую ранее не видели, в один момент дверь позади вас закрылась, и вы остались запертыми внутри. После тщательного исследования вы поняли, что это был механизм безопасности, который запускался, когда кто-то проходил через дверь в определенное время. Вы осмотрели комнату и нашли панель управления, которой удалось открыть дверь. Вы вышли из нее и обнаружили, что находитесь на поверхности, прямо на опушке леса."},
    "desert": {"description": "это пустыня драконов, где тяжело найти что-то живое",
               "enemies": [(3, "skeleton"), (2, "death_worm")],
               "artefacts": [(3, "health_posion"), (2, "sands_of_time"), (5, "dexterity_posion")],
               "max_artefacts": 4,
               "prehistory": "Вы блуждали в лесу уже несколько дней, пока в конце дня не наткнулись на странную металлическую дверь, которая вела в глубь чащи. Однако, что бы они не делали, они не могли ее открыть. И тогда вы вспомнили про артефакт, который вы нашли в сокровищнице. Вы достали этот красивый камень, приложили его к двери, и услышали резкий щелчок. Дверь начала медленно открываться. Команда решила зайти внутрь, и через пару секунд она оказалась в длинном коридоре, освещенном узкими прожекторами. Коридор заканчивался огромным кружевным порталом с высеченными на нем драконами. Участники команды, ничего не подозревая, решили пройти сквозь портал, и оказались в горячей пустыне драконов."},
    "ice_world": {"description": "это ледяной мир, в котором всё покрыто снегом и льдом",
                  "enemies": [(1, "troll"), (3, "zimogor")],
                  "artefacts": [(5, "strength_posion"), (6, "dexterity_posion"), (1, "crown_of_mind")],
                  "max_artefacts": 3,
                  "prehistory": "Ваш взгляд устремился на что-то, что казалось красивым и магическим издали – древний, освещенный мерцанием света, храм. После исследования храма, вы нашли часть, которая вела внутрь храма. Воздействие таинственных магических слов вызвало загадочный вихрь, который перенес вашу отважную команду путешественников в новое измерение – мир льда и снега."},
    "castle": {"description": "это огромный старинный замок, находящийся на вершине горы",
               "enemies": [(2, "skeleton"), (4, "ghost")],
               "artefacts": [(7, "health_posion"), (2, "strength_posion"), (1, "crown_of_mind")],
               "max_artefacts": 5,
               "prehistory": "Ваша команда бросила вызов ледяным грозам и пересекла заснеженные пустоши. В центре ледяного мира вы обнаружили огромный замок, который находится на горе. Команда, наконец, поняла, что она близка к своей цели. Несколько часов вы блуждали в лабиринте, но в конце концов, вам удалось найти выход и вы оказались перед входом в замок. Вы решили войти в замок."}
}
