import json
from pprint import pprint

from core.Logic.ai_funcs import generate_location
from core.store import locations


def webhook(session):
    action = session['action']

    if action == 'dragon':
        print('Received request from event1 action')
        session['location'] = generate_location(locations['dungeon'])



    else:
        print('Unknown action. Session data:')
        pprint(session)
        action = session['action']

        session['text'] = f'Webhook recieved a request, but couldn\'t handle the action' \
                          f'{action}.'

    return json.dumps(session)
