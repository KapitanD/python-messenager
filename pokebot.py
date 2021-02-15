"""pokebot.py
Модуль бота для ловли покемонов
"""
import random
import time as t
import requests



class PokeBot:
    """PokeBot
    class for catch pokemon logic
    """
    def __init__(self):
        """init PokeBot state:
        catched dict{
            user : list[
                pokemon,
                ...
            ]
        }
        commands - availiable bot commands
        """
        self.catched = {}
        self.commands = {
            "/help": self.handle_help,
            "/catch": self.handle_catch,
            "/list": self.handle_list
        }

    def catch(self, user):
        """Realization of catch method

            Parameters:
                    user (str): User who call catch

            Returns:
                    pokemon (dict): Catched pokemon

            Description:
                    Gets random pokemon from pokeapi.co
                    and add to current user catched
        """
        pokemon_id = random.randint(1, 890)
        pokemon = requests.get(
            f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}").json()
        if user not in self.catched:
            self.catched[user] = []

        self.catched[user].append(pokemon)
        return pokemon

    def handle_catch(self, user):
        """Handler for catch command

            Parameters:
                    user (str): User who call catch

            Returns:
                    message (str): Text of message for chat

            Description:
                    Call inner catch method and form a message for chat
        """
        pokemon = self.catch(user)
        types = [type["type"]["name"] for type in pokemon["types"]]
        stats = {stat["stat"]["name"]: stat["base_stat"]
                 for stat in pokemon["stats"]}
        return f'{user}, вы поймали покемона {pokemon["name"]}, его типы: {types}, его показатели {stats}'

    def handle_list(self, user):
        """Handler for list command

            Parameters:
                    user (str): User who call list

            Returns:
                    message (str): Text of message for chat

            Description:
                    Form a message with all catched pokemons
        """
        if user not in self.catched:
            return f'{user}, вы не поймали еще ни одного покемона :( Попробуйте поймать несколько с помощью команды /catch'
        
        message = f'{user}, вы поймали {len(self.catched[user])} покемонов:\n'
        for pokemon in self.catched[user]:
            message += pokemon["name"] + '\n'

        return message

    def handle_help(self, user):
        """Handler for list command

            Parameters:
                    user (str): User who call help

            Returns:
                    message (str): Text of message for chat

            Description:
                    Form a help message
        """
        return f"""
Привет {user}, на этом сервере можно ловить покемонов! Команды:
    /help - вывести это сообщение
    /catch - поймать покемона
    /list - посмотреть пойманых вами покемонов
"""

    def check_message(self, message, user):
        """Check message for command and call needed handler

            Parameters:
                    user (str): User who call list
                    message (str): Message, where we check command

            Returns:
                    message (dict): Message

            Description:
                    Form a message with all catched pokemons
        """
        if message in self.commands:
            text = self.commands[message](user)
            return {
                "time": t.time(),
                "name": "PokeBot",
                "text": text
            }
        else:
            return None
