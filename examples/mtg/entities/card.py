class Card:

    def __init__(self, name, cost):
        self.name = name
        self.cost = cost
        self.is_tapped = False

    def tap(self):
        self.is_tapped = True

    def untap(self):
        self.is_tapped = False

    def apply(self):
        pass

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)