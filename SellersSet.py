from Seller import Seller


class SellersSet:
    def __init__(self):
        self.set = set()

    def add(self, seller):
        if isinstance(seller, Seller):
            # To do
            # get old seller from set
            existsSeller = self.get(seller)

            if not existsSeller:
                self.set.add(seller)
            else:
                if existsSeller.price != seller.price or existsSeller.amount != seller.amount:
                    self.updateSeller(seller, existsSeller)

    def remove(self, seller):
        if isinstance(seller, Seller):
            if seller in self.set:
                self.set.remove(seller)

    def get(self, seller):
        for s in self.set:
            if s.link == seller.link:
                return s
        return None

    def updateSeller(self, newSeller, oldSeller):
        oldSeller.price = newSeller.price
        oldSeller.amount = newSeller.amount
        oldSeller.isSend = False

    def clear(self):
        self.set = set()
