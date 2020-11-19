class Entry:
    def __init__(self):
        self.address = None
        self.confirmed = False
        self.exclusions = []

    def set_addr(self, address):
        self.address = address

    def add_exclusion(self, user):
        self.exclusions.append(user)

    def is_confirmed(self):
        return self.confirmed
