import requests
import json


def create_trello_board(token, api_key, name):

    url = "https://api.trello.com/1/boards/"

    query = {
    'name': name,
    'key': api_key,
    'token': token
    }

    response = requests.post(url, params=query)
    return response.json()['id'], response.json()['url']


def delete_trello_board(token, api_key, board_id):

    url = f'https://api.trello.com/1/boards/{board_id}'

    query = {
    'key': token,
    'token': api_key
    }

    requests.request(
    "DELETE",
    url,
    params=query
    )


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

        requests.request(
        "PUT",
        url,
        data=payload,
        headers=headers,
        params=query
        )
