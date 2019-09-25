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
        try:
            script = next(self.script)
            reply = script(message)
            self.buffer.append(reply)
        except StopIteration:
            self.buffer.append(message)


def chose(i=0):
    options_key = 'options'
    return lambda message: message[options_key][i]

def chose_option(message: dict, i=0):
    options_key = 'options'
    return message[options_key][i]
