import json
import random
from pprint import pprint

from core.store import stats, hero_description, locations


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
        for player in session["Names"]:
            players[player] = hero_list.pop(random.randrange(len(hero_list)))
        session["players"] = players
        print(session["players"])
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
    else:
        print('Unknown action. Session data:')
        pprint(session)
        action = session['action']

        session['text'] = f'Webhook recieved a request, but couldn\'t handle the action' \
                          f'{action}.'

    return json.dumps(session)
