import json
import random
from pprint import pprint
import pymorphy3

from core.store import stats, hero_description, locations, enemies, translations, hero_attack_prompt, \
    enemies_attack_prompt, abilities, artefact_type, artefact_effects


def make_agree_with_num(word, num):
    morph = pymorphy3.MorphAnalyzer()
    p = morph.parse(word)[0]
    return p.make_agree_with_number(int(num)).word


def create_table(user_id):
    import sqlite3

    conn = sqlite3.connect('locations.db')
    print(user_id)
    conn.execute(f'''CREATE TABLE IF NOT EXISTS user_{user_id}
                     (id INTEGER PRIMARY KEY,
                     location_name TEXT,
                     description TEXT,
                      game_count_number INTEGER);''')

    conn.close()


# def adds(session):
#     cur_person_stats = session["players_data"][session["cur_person_name"]]["stats"]
#     stats_adds = {}
#     for key in list()
#     inventory = session["players_data"][session["cur_person_name"]]["inventory"]
#     ar_can_use = []
#     for item in inventory:
#         if artefact_type[item] == 'all_time':
#             ar_can_use.append(item)


def enemy_death(session, target_name):
    session["cur_loc_enemies"].pop(target_name)
    print('удалить', target_name)
    session["turns"] = {key: val for key, val in list(session["turns"].items()) if val["name"] != target_name}
    return session


def get_game_count(user_id):
    import sqlite3

    conn = sqlite3.connect('locations.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT game_count_number FROM user_{user_id} WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    return result[0]


def get_location(location_type):
    import sqlite3

    conn = sqlite3.connect('locations.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM locations WHERE location_type = ?", (location_type,))
    result = cursor.fetchall()
    return result


def add_new_location(user_id, location_name, description):
    import sqlite3
    conn = sqlite3.connect('locations.db')

    conn.execute(f"INSERT INTO user_{user_id} (location_name, description, game_count_number) VALUES (?, ?, ?)",
                 (location_name, description, 1))
    conn.commit()
    conn.close()


def callback(future, user_id, location_name):
    result = future.result()
    add_new_location(user_id, location_name, result)


# ---------
def roll_dice(sides=6, num_dice=1):
    total = 0
    for i in range(num_dice):
        total += random.randint(1, sides)
    return total


def make_turns(session):
    turns = {}
    entities = list(session["players"].keys()) + list(session["cur_loc_enemies"].keys())
    print(entities)
    was = False
    nums = list(range(len(entities)))
    for cnt in range(len(entities)):
        if cnt == len(list(session["players"].keys())):
            was = True
        if was:
            turns[str(nums.pop(random.randrange(len(nums))))] = {"name": entities[cnt],
                                                                 "type": str(entities[cnt].split("-")[0])}
        else:
            turns[str(nums.pop(random.randrange(len(nums))))] = {"name": entities[cnt], "type": "player"}

    return dict(sorted(turns.items()))


def update_turns(session):
    turns = {}
    entities = session["turns"]

    for count, name in enumerate(list(entities.values())):
        turns[str(count)] = name
    print("update")
    print(turns)
    return dict(sorted(turns.items()))


def webhook(session):
    action = session['action']
    print('hey')

    if action == 'hero_introduction':
        session["location_number"] = 0
        hero_list = list(stats.keys())
        players = {}
        players_data = {}
        for player in session["Names"]:
            players[player] = hero_list.pop(random.randrange(len(hero_list)))
        session["players"] = players
        for player_name, hero in list(players.items()):
            players_data[player_name] = {
                "health": stats[hero]["health"],
                "hero_type": hero,
                "stats": stats[hero],
                "inventory": [],
                "abilities_left": 2,
                "effects": [],
                "is_dead": False

            }
        session["players_data"] = players_data
        print(session["players_data"])

        hero_prompt = "О, это же мои старые друзья: "
        for name in session["Names"]:
            hero_prompt += f"{name} - {hero_description[players[name]]}, "
        hero_prompt = hero_prompt[:-2]
        hero_prompt += ". Пропусти их (он обращается к охранику) - они со мной."
        session["hero_prompt"] = hero_prompt
    elif action == 'history':
        session["history_part"] = locations[list(locations.keys())[session["location_number"]]]["prehistory"]



    elif action == 'location':
        session["location_env"] = {
            "stun_all": False,
            "artefact_part": False,

        }
        session["effects_running"] = {

        }
        for ability in list(abilities.values()):
            session["effects_running"][ability["type"]] = 0
        print(session["effects_running"])
        locations_data = get_location(list(locations.keys())[session["location_number"]])
        location_data = random.choice(locations_data)
        session["location_description"] = location_data[2]
        session["cur_location_info"] = {
            "location_type": location_data[1],
            "mobs": list(eval(location_data[3])),
            "artefacts": list(eval(location_data[4]))
        }
        print(session["cur_location_info"])
        turns = {}
        enemies_dict = {}
        for count, enemy in eval(location_data[3]):
            for num in range(count):
                enemies_dict[f"{enemy}-{num + 1}"] = enemies[enemy]
        enemies_dict = dict(sorted(enemies_dict.items(), key=lambda item: item[1]["health"]))
        session["cur_loc_enemies"] = enemies_dict

        entities = list(session["players"].keys()) + list(session["cur_loc_enemies"].keys())
        print(entities)
        was = False
        nums = list(range(len(entities)))
        for cnt in range(len(entities)):
            if cnt == len(list(session["players"].keys())):
                was = True
            if was:
                turns[str(nums.pop(random.randrange(len(nums))))] = {"name": entities[cnt],
                                                                     "type": str(entities[cnt].split("-")[0])}
            else:
                turns[str(nums.pop(random.randrange(len(nums))))] = {"name": entities[cnt], "type": "player"}
        turns = dict(sorted(turns.items()))
        session["turns"] = turns

        turns_text = ""
        for i, entity in turns.items():
            if entity["type"] == "player":
                turns_text += f"{int(i) + 1}-ым ходит {entity['name']}, "
            else:
                turns_text += f"{int(i) + 1}-ым ходит {translations[entity['name'].split('-')[0]]}-{entity['name'].split('-')[1]}, "
        session["turns_text"] = turns_text
        session["cur_turn_count"] = 0
    elif action == 'turn':
        print("стата", session["players_data"])
        print('очередь', str(session["cur_turn_count"]))
        print(session["cur_loc_enemies"])
        print(session["turns"])
        session["location_env"]["stun_all"] = session["effects_running"]["stun_all"]
        session["turns"] = update_turns(session)

        session["last_enemies_names"] = list(
            map(lambda x: f'{x.split("-")[0]}-{x.split("-")[1]}', list(session["cur_loc_enemies"].keys())))
        session["last_enemies_names_text"] = '. '.join(session["last_enemies_names"])
        session["cur_person_name"] = session["turns"][str(session["cur_turn_count"])]["name"]
        session["cur_person_type"] = session["turns"][str(session["cur_turn_count"])]["type"]
        # ---------- update effects

        if session["cur_person_type"] == "player":
            for effect in session["players_data"][session["cur_person_name"]]["effects"]:
                if not session["effects_running"][effect]:
                    session["players_data"][session["cur_person_name"]]["effects"].pop(
                        session["players_data"][session["cur_person_name"]]["effects"].index(effect))

        session["cur_loc_enemies"] = dict(
            sorted(session["cur_loc_enemies"].items(), key=lambda item: item[1]["health"]))
        print(session["cur_person_name"], session["cur_person_type"], session["turns"])
        if not session["cur_loc_enemies"]:
            session["location_env"]["artefact_part"] = True






    elif action == 'roll_20_dice':
        session["roll_dice_result"] = roll_dice(20, 1)
    elif action == 'live_check':

        if session["roll_dice_result"] >= 10:
            session["players_data"][session["cur_person_name"]]["health"] = \
                session["players_data"][session["cur_person_name"]]["stats"]["health"] // 2
            live_check_response = 'Поздравляю, вы живы'
        else:
            session["players_data"][session["cur_person_name"]]["health"] = 1
            session["players_data"][session["cur_person_name"]]["inventory"] = []
            live_check_response = 'К сожалению, вы восстаёте из мёртвых'
        session["players_data"][session["cur_person_name"]]["is_dead"] = False
        session["live_check_response"] = live_check_response
    elif action == 'update_turn_count':
        session["new_location"] = 0
        if session['cur_turn_count'] + 1 >= len(list(session["turns"].keys())):
            session['cur_turn_count'] = 0
            for ability in list(abilities.values()):
                session["effects_running"][ability["type"]] = max(0, session["effects_running"][ability["type"]] - 1)
                if session["location_env"]["artefact_part"]:
                    session["new_location"] = 1
                    session["location_number"] += 1
                    if len(list(locations.keys())) == session["location_number"]:
                        session["new_location"] = 2
        else:
            session['cur_turn_count'] += 1
    elif action == 'target_check':
        enemies_intents = set([i.split("-")[0] for i in list(session["cur_loc_enemies"].keys())])
        target_type = 404
        for intent in enemies_intents:
            if translations[intent].lower() in session["target"].lower():
                target_type = intent
        session["target_type"] = target_type
    elif action == 'artefact_check':
        ar_can_use = []
        for item in session["players_data"][session["cur_person_name"]]["inventory"]:
            if artefact_type[item] == 'temporary':
                ar_can_use.append(item)
        artefact_intents = set(ar_can_use)
        artefact_name = 404
        for intent in artefact_intents:
            if translations[intent].lower() in session["artefact_target"].lower():
                artefact_name = intent
        session["artefact_name"] = artefact_name
    elif action == 'artefact_use':
        effects = artefact_effects[session["artefact_name"]]
        ar_text = ""
        for effect, effect_name in effects:
            if effect_name == "health":
                session["players_data"][session["cur_person_name"]]["health"] += effect

            else:
                session["players_data"][session["cur_person_name"]]["stats"][effect_name] += effect
            ar_text += f'{effect} к {make_agree_with_num(translations[effect_name], effect)}, '
        ar_text = ar_text[:-2]
        artefact_use_response = f'{session["cur_person_name"]}, успешно применил артефакт {translations[session["artefact_name"]]} и получил {ar_text}.'
        session['artefact_use_response'] = artefact_use_response
    elif action == 'artefact_part':
        artefact_part_response = ""
        artefacts = list(session["cur_location_info"]["artefacts"])

        if session["roll_dice_result"] + session["players_data"][session["cur_person_name"]]["stats"]["intelligence"] < 12 or not artefacts:
            artefact_part_response += "К сожалению вы не нашли никаких артефактов"
        else:
            found_artefact = random.choice(artefacts)
            artefacts.pop(artefacts.index(found_artefact))
            session["cur_location_info"] = artefacts

            effects = artefact_effects[found_artefact]
            ar_dp = ""
            for effect, effect_name in effects:
                ar_dp += f'{effect} к {make_agree_with_num(translations[effect_name], effect)}, '
            ar_dp = ar_dp[:-2]
            artefact_part_response += f'Поздравляю вы нашли {translations[found_artefact]}, он даёт {ar_dp}.'
            session["artefact_part_response"] = artefact_part_response
    elif action == 'enemy_move':
        print("enemy_move")
        target = random.choice(list(session['players_data'].keys()))
        print(session["effects_running"]["stun_all"])
        if not (session["effects_running"]["stun_all"] or "attack_block" in session["players_data"][target]["effects"]):

            print(target)
            attack_res = random.choices([1, 2], weights=[3, 1])[0]
            print(attack_res)
            if attack_res == 1:
                damage = roll_dice(4, session["cur_loc_enemies"][session["cur_person_name"]]["attack"])
                enemy_move_prompt = f'{target}, {translations[session["cur_person_name"].split("-")[0]]}-{session["cur_person_name"].split("-")[1]} {random.choice(enemies_attack_prompt["usual"])}. Он наносит {damage} урона.'

                session['players_data'][target]["health"] -= damage
                if session['players_data'][target]["health"] < 0:
                    session['players_data'][target]["is_dead"] = True
            else:
                enemy_move_prompt = f'{target}, {translations[session["cur_person_name"].split("-")[0]]}-{session["cur_person_name"].split("-")[1]} {random.choice(enemies_attack_prompt["missed"])}. Он не наносит урона.'
        else:
            if session["effects_running"]["stun_all"]:
                enemy_move_prompt = f'Противники оглушены ещё {session["effects_running"]["stun_all"]} {make_agree_with_num("ход", session["effects_running"]["stun_all"])}. Он ничего не может сделать.'
            elif "attack_block" in session["players_data"][target]["effects"]:
                enemy_move_prompt = f'Щит игрока {target} действует ещё {session["effects_running"]["attack_block"]} {make_agree_with_num("ход", session["effects_running"]["attack_block"])}. Монстр не наносит ему урона.'

        session["move_result"] = enemy_move_prompt

    elif action == 'attack':
        target = [x for x in list(session["cur_loc_enemies"].keys()) if x.split("-")[0] == session["target_type"]][0]
        attack_response = ""
        player_hero_type = session["players"][session["cur_person_name"]]
        if session["roll_dice_result"] + session["players_data"][session["cur_person_name"]]["stats"]["strength"] >= \
                session["cur_loc_enemies"][target]["defense"]:
            damage = roll_dice(8, 1)
            attack_response += f'{session["cur_person_name"]}, {random.choice(hero_attack_prompt[player_hero_type]["usual"])}. Ты нанёс {translations[target.split("-")[0]]}-{target.split("-")[1]} {damage} урона.'
            session["cur_loc_enemies"][target]["health"] -= damage
        else:
            attack_response += f'{session["cur_person_name"]}, {random.choice(hero_attack_prompt[player_hero_type]["missed"])}. Ты не нанёс {translations[target.split("-")[0]]}-{target.split("-")[1]} урона.'
        if session["cur_loc_enemies"][target]["health"] <= 0:
            attack_response += f'{session["cur_person_name"]}, {random.choice(hero_attack_prompt[player_hero_type]["last"])}. {translations[target.split("-")[0]]}-{target.split("-")[1]} повержен. '
            session = enemy_death(session, target)
            if not session["cur_loc_enemies"]:
                attack_response += "Поздравляю герои, все враги повержены. Теперь у вас есть возможность найти артефакты или использовать их. Но у вас есть всего один ход! Так что выбирайте с умом"

        session["attack_response"] = attack_response
    elif action == 'ability_help':
        player_hero_type = session["players"][session["cur_person_name"]]
        ability_name = session["players_data"][session["cur_person_name"]]["stats"]["abilities"]
        abilities_left = session["players_data"][session["cur_person_name"]]["abilities_left"]
        ability = abilities[ability_name]
        if session["players_data"][session["cur_person_name"]]["abilities_left"]:
            session[
                'ability_help_response'] = f'У тебя есть способность {translations[ability_name]}. {ability["description"]}. Будем использовать?'
            session["success_ability_use"] = 1
        else:
            session[
                'ability_help_response'] = f'К сожалению, ты использовал способности максимальное количество раз, попробуй провести обычную атаку. '
            session["success_ability_use"] = 0
    elif action == "inventory":
        if not session["players_data"][session["cur_person_name"]]["inventory"]:
            session["inventory_response"] = "В твоём инвентаре ничего нет, но это не повод растраиваться!"
        else:
            in_text = ""
            for item in session["players_data"][session["cur_person_name"]]["inventory"]:
                in_text += f'{translations[item]}, '
            in_text = in_text[:-2]
            session["inventory_response"] = "В твоём инвентаре лежит:" + in_text + '. '

            if session["location_env"]["artefact_part"]:
                in_text2 = ""
                for item in session["players_data"][session["cur_person_name"]]["inventory"]:
                    if artefact_type[item] == 'temporary':
                        in_text2 += f'{translations[item]}, '
                in_text2 = in_text2[:-2]
                session["inventory_response"] += "Ты можешь использовать:" + in_text2 + '. Так что будешь применять?'

    elif action == 'ability':

        player_hero_type = session["players"][session["cur_person_name"]]
        ability_name = session["players_data"][session["cur_person_name"]]["stats"]["abilities"]
        ability = abilities[ability_name]
        ability_response = f'{session["cur_person_name"]} применил способность {translations[ability_name]}. {ability["usage_prompt"]}. '
        if ability["type"] == "heal_all":
            for p in list(session["players_data"].keys()):
                session["players_data"][p]["health"] += random.randint(1, ability["max_effect"])
            ability_response += f'Он восстанавливает {ability["max_effect"]} здоровья своим союзникам. '
        elif ability["type"] == "stun_all":
            session["effects_running"][ability["type"]] += ability["max_effect"]
        elif ability["type"] == "attack_all":
            ability_response += f'Он наносит {ability["max_effect"]} всем врагам. '
            for e in list(session["cur_loc_enemies"].keys()):

                if session["cur_loc_enemies"][e]["health"] > ability["max_effect"]:
                    session["cur_loc_enemies"][e]["health"] -= ability["max_effect"]

                else:
                    session = enemy_death(session, e)
                    ability_response += f'{session["cur_person_name"]}, {random.choice(hero_attack_prompt[player_hero_type]["last"])}. {translations[e.split("-")[0]]}-{e.split("-")[1]} повержен. '
                    if not session["cur_loc_enemies"]:
                        ability_response += "Поздравляю герои, все враги повержены. Теперь у вас есть возможность найти артефакты или использовать их. Но у вас есть всего один ход! Так что выбирайте с умом"
        elif ability["type"] == "attack_block":
            session["effects_running"][ability["type"]] += ability["max_effect"]

            session["players_data"][session["cur_person_name"]]["effects"].append(ability["type"])
        elif ability["type"] == "attack":
            e = random.choice(list(session["cur_loc_enemies"].keys()))
            ability_response += f'Он наносит {ability["max_effect"]} урона {translations[e.split("-")[0]]}-{e.split("-")[1]}. '

            if session["cur_loc_enemies"][e]['health'] > ability["max_effect"]:
                session["cur_loc_enemies"][e]['health'] -= ability["max_effect"]
            else:
                session = enemy_death(session, e)
                ability_response += f'{session["cur_person_name"]}, {random.choice(hero_attack_prompt[player_hero_type]["last"])}. {translations[e.split("-")[0]]}-{e.split("-")[1]} повержен. '
                if not session["cur_loc_enemies"]:
                    ability_response += "Поздравляю герои, все враги повержены. Теперь у вас есть возможность найти артефакты или использовать их. Но у вас есть всего один ход! Так что выбирайте с умом"
        session["players_data"][session["cur_person_name"]]["abilities_left"] -= 1
        session[
            "ability_response"] = ability_response



    else:
        print('Unknown action. Session data:')

        action = session['action']

        session['text'] = f'Webhook recieved a request, but couldn\'t handle the action' \
                          f'{action}.'

    return json.dumps(session)
