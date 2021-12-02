class Seller:
    def __init__(self, link, amount, price):
        self.link = link
        self.amount = amount
        self.price = price
        self.isSend = False

    def __eq__(self, other):
        return isinstance(other, Seller) and \
               self.link == other.link

    def __hash__(self):
        return hash(self.link)

    def sended(self):
        self.isSend = True
