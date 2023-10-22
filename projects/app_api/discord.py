import requests
from environs import Env
from urllib.parse import urljoin


def create_discord_channel(token, guild_id, channel_name, text):

    url = f'https://discord.com/api/v9/guilds/{guild_id}/channels'

    header = {
        'Authorization': token
    }

    data ={
        'name': channel_name,
        'type': 2, # Голосовой канал
        'topic': text,
        'user_limit': 4
    }

    response = requests.post(url, headers=header, json=data)
    return response.json()['id']


def delete_discord_channel(token, channel_id):

    url = f"https://discord.com/api/v9/channels/{channel_id}"

    header = {
        "Authorization": token
    }

    requests.post(url, headers=header)


def create_discord_invite(token, channel_id):
    url = f"https://discord.com/api/v9/channels/{channel_id}/invites"

    header = {
        "Authorization": token
    }

    data ={
        'max_age': 86400,
        'max_uses': 3,
        'temporary': True,

    }

    response = requests.post(url, headers=header, json=data)
    return urljoin('https://discord.com/invite/', response.json()['code'])


if __name__ == '__main__':

    env = Env()
    env.read_env()

    name_channel = 'Джуны [12.20 - 12.40]'

    token = env.str('DISCORD_TOKEN')
    guild_id = env.str('DISCORD_GUILD_ID')
    channel_id = create_discord_channel(token, guild_id, name_channel, 'Тут описание каннала')

    invite_url = create_discord_invite(token, channel_id)
    
    print(invite_url)