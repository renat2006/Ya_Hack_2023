import json
import random
from pprint import pprint

from core.store import stats, hero_description, locations, enemies, translations, hero_attack_prompt, \
    enemies_attack_prompt


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


def update_turns(session):
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
                "inventory": []

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
        print(session["cur_loc_enemies"])
        turns = update_turns(session)
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
        turns = update_turns(session)
        session["turns"] = turns
        session["last_enemies_names"] = list(
            map(lambda x: f'{x.split("-")[0]}-{x.split("-")[1]}', list(session["cur_loc_enemies"].keys())))
        session["last_enemies_names_text"] = '. '.join(session["last_enemies_names"])
        session["cur_person_name"] = session["turns"][str(session["cur_turn_count"])]["name"]
        session["cur_person_type"] = session["turns"][str(session["cur_turn_count"])]["type"]
        session["cur_loc_enemies"] = dict(
            sorted(session["cur_loc_enemies"].items(), key=lambda item: item[1]["health"]))
    elif action == 'roll_20_dice':
        session["roll_dice_result"] = roll_dice(20, 1)
    elif action == 'target_check':
        enemies_intents = set([i.split("-")[0] for i in list(session["cur_loc_enemies"].keys())])
        target_type = 404
        for intent in enemies_intents:
            if translations[intent].lower() in session["target"].lower():
                target_type = intent
        session["target_type"] = target_type
    elif action == 'enemy_move':
        target = random.choice(list(random.choice(session['players_data'].keys())))
        attack_res = random.choices([1, 2], weights=[3, 1])
        if attack_res == 1:
            damage = roll_dice(4, session["cur_loc_enemies"][session["cur_person_name"]]["attack"])
            enemy_move_prompt = f'{target}, {session["cur_person_name"]} {enemies_attack_prompt["usual"]}. Он наносит {damage} урона.'
            session['players_data'][target]["health"] -= damage
        else:
            enemy_move_prompt = f'{target}, {session["cur_person_name"]} {enemies_attack_prompt["missed"]}. Он не наносит урона.'

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
            attack_response += f'{session["cur_person_name"]}, {random.choice(hero_attack_prompt[player_hero_type]["last"])}. {translations[target.split("-")[0]]}-{target.split("-")[1]} повержен'
            session["cur_loc_enemies"].pop(target)

        session["attack_response"] = attack_response
    elif action == 'ability':
        ability = session["players_data"][session["cur_person_name"]]["stats"]["abilities"]
        if ability["type"] == "heal_all":
            for p in session["players_data"]:
                p["stats"]["health"] += random.randint(1, ability["max_effect"])
        elif ability["type"] == "stun_all":
            pass
        elif ability["type"] == "attack_all":
            for e in session["cur_loc_enemies"].items():
                if e[1]["health"] > 2:
                    e[1]["health"] -= 2
                else:
                    del session["cur_loc_enemies"][e[0]]
        elif ability["type"] == "attack_block":
            pass
        elif ability["type"] == "attack":
            e = list(session["cur_loc_enemies"].keys())[0]
            if session["cur_loc_enemies"][e]['health'] > 15:
                session["cur_loc_enemies"][e]['health'] -= 15
            else:
                del session["cur_loc_enemies"][e[0]]
        session[
            "ability_response"] = f'{session["cur_person_name"]} применил способность {ability}. {ability["usage_prompt"]}'



    else:
        print('Unknown action. Session data:')
        pprint(session)
        action = session['action']

        session['text'] = f'Webhook recieved a request, but couldn\'t handle the action' \
                          f'{action}.'

    return json.dumps(session)
