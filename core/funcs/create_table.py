def create_table(user_id):
    import sqlite3

    conn = sqlite3.connect('../locations.db')
    print(user_id)
    conn.execute(f'''CREATE TABLE IF NOT EXISTS user_{user_id}
                     (id INTEGER PRIMARY KEY,
                     location_name TEXT,
                      game_count_number INTEGER);''')

    conn.close()
