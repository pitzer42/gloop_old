import random


class Deck(list):

    def draw(self, n=1):
        drawn = list()
        for i in range(n):
            card = self.pop()
            drawn.append(card)
        return drawn

    def shuffle(self):
        random.shuffle(self)
