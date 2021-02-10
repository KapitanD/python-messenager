import requests
import random
import time as t

class PokeBot:
    def __init__(self):
        self.catched = {}
        self.commands = {
            "/help" : self.handle_help,
            "/catch": self.handle_catch,
            "/list" : self.handle_list
        }

    def catch(self, user):
        pokemon_id = random.randint(1, 890)
        pokemon = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}").json()
        if user not in self.catched:
            self.catched[user] = []

        self.catched[user].append(pokemon)
        return pokemon

    def handle_catch(self, user):
        pokemon = self.catch(user)
        types = [type["type"]["name"] for type in pokemon["types"]]
        stats = {stat["stat"]["name"] : stat["base_stat"] for stat in pokemon["stats"]}
        return f'{user}, вы поймали покемона {pokemon["name"]}, его типы: {types}, его показатели {stats}'

    def handle_list(self, user):
        if user not in self.catched:
            self.catched[user] = []
            return f"{user}, вы не поймали еще ни одного покемона :( Попробуйте поймать несколько с помощью команды /catch"
        message = f'{user}, вы поймали {len(self.catched[user])} покемонов:\n'
        for pokemon in self.catched[user]:
            message += pokemon["name"] + '\n'
        return message

    def handle_help(self, user):
        return f"""
Привет {user}, на этом сервере можно ловить покемонов! Команды:
    /help - вывести это сообщение
    /catch - поймать покемона
    /list - посмотреть пойманых вами покемонов
"""

    def check_message(self, message, user):
        if message in self.commands:
            text = self.commands[message](user)
            return {
                "time": t.time(),
                "name": "PokeBot",
                "text": text
            }
        else:
            return None