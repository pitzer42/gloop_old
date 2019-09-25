class Deck(list):

    def draw(self, n=1):
        drawn = list()
        for i in range(n):
            card = self.pop()
            drawn.append(card)
        if n == 1:
            return drawn[0]
        return drawn
