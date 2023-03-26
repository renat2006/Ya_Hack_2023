import os
import random

import openai
import re

from core.store import locations, translations

openai.api_key = os.getenv('GPT3TOKEN')


def generate_location(location):
    enemies_list = location["enemies"]
    artefact_list = location["artefacts"]
    enemies_prompt = ""
    artefact_prompt = ""
    for enemy in enemies_list:
        enemies_prompt += f"{translations[enemy[1]]} - {enemy[0]} штуки, "
    for artefact in artefact_list:
        artefact_prompt += f"{translations[artefact]}, "

    prompt = f"Сгенерируй описание локации для квеста по следующим характеристикам: {location['description']}, на " \
             f"этой локации будут такие враги: {enemies_prompt} и такие артефакты: {artefact_prompt}"
    print('Запрос:')
    print(prompt)
    print()
    messages = [{"role": "system", "content": "Ты гейм-мастер в игре подземелья и драконы"},
                {"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    description = response.choices[0].message.content

    return description
