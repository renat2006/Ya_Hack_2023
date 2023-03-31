import json
import random
from pprint import pprint

from core.store import stats, hero_description, locations, enemies, translations


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

        session["cur_loc_enemies"] = enemies_dict
        print(session["cur_loc_enemies"])
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



    else:
        print('Unknown action. Session data:')
        pprint(session)
        action = session['action']

        session['text'] = f'Webhook recieved a request, but couldn\'t handle the action' \
                          f'{action}.'

    return json.dumps(session)
