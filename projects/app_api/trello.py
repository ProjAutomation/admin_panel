import requests
from environs import Env
import json


def create_trello_board(token, api_key, name):

    url = "https://api.trello.com/1/boards/"

    query = {
    'name': name,
    'key': api_key,
    'token': token
    }

    response = requests.post(url, params=query)
    print(response.json())
    return response.json()['id']


def delete_trello_board(token, api_key, board_id):

    url = f'https://api.trello.com/1/boards/{board_id}'

    query = {
    'key': token,
    'token': api_key
    }

    response = requests.request(
    "DELETE",
    url,
    params=query
    )

    print(response.text)


def create_trello_invite(token, api_key, board_id, emails):
    url = f'https://api.trello.com/1/boards/{board_id}/members'

    headers = {
    "Content-Type": "application/json"
    }

    for email in emails:

        query = {
        'email': email,
        'key': api_key,
        'token': token
        }

        payload = json.dumps({'fullName': email})
        print(payload)

        response = requests.request(
        "PUT",
        url,
        data=payload,
        headers=headers,
        params=query
        )
        print(response.text)


if __name__ == '__main__':

    env = Env()
    env.read_env()

    emails = ['lamerork@yandex.ru', 'sokolova1133@yandex.ru']

    api_key = env.str('TRELLO_API_KEY')
    token = env.str('TRELLO_API_TOKEN')

    name_board = 'Джуны [12.20 - 12.40]'

    board_id = create_trello_board(token, api_key, name_board)
    create_trello_invite(token, api_key, board_id, emails)