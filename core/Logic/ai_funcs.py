

import openai
from core.store import locations, translations

openai.api_key = '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'



def generate_location(location):
    enemies_list = location["enemies"]

    enemies_prompt = ""

    for enemy in enemies_list:
        enemies_prompt += f"{translations[enemy[1]]} - {enemy[0]} штуки, "

    prompt = f"Сгенерируй описание локации для квеста по следующим характеристикам: {location['description']}, на " \
             f"этой локации будут такие враги: {enemies_prompt}."
    print('Запрос:')
    print(prompt)
    print()
    messages = [{"role": "system", "content": "Ты гейм-мастер в игре подземелья и драконы"},
                {"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,

    )
    description = response.choices[0].message.content

    return description
