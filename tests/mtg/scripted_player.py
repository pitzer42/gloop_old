from gloop.entities.remote_player import RemotePlayer
from examples.mtg.entities.mtg_remote_player import MtgRemotePlayer


class MtgBot(MtgRemotePlayer):

    def __init__(self, *script):
        MtgRemotePlayer.__init__(
            self,
            ScriptedPlayer(*script)
        )


class ScriptedPlayer(RemotePlayer):

    def __init__(self, *script):
        self.script = iter(script)
        self.buffer = list()

    async def receive(self) -> str:
        return self.buffer.pop()

    async def send(self, message):
        script = next(self.script)
        reply = script(message)
        self.buffer.append(reply)


options_key = 'options'


def chose(i=0):
    def _chose(message):
        return message[options_key][i]
    return _chose


def chose_card(card_name):
    def _chose_card_with_cost(message):
        i = 0
        options = message[options_key]
        for option in options:
            if card_name in option:
                return i
            i += 1
    return _chose_card_with_cost

