class Entry:
    def __init__(self, id_):
        self.id = id_
        self.address = None
        self.confirmed = False
        self.exclusions = []

    def set_addr(self, address):
        self.address = address

    def add_exclusion(self, user):
        self.exclusions.append(user)

    def confirm(self):
        self.confirmed = True
