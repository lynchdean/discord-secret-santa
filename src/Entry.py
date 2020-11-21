class Entry:
    def __init__(self, id):
        self.id = id
        self.address = None
        self.confirmed_addr = False
        self.confirmed_all = False
        self.exclusions = []

    def set_addr(self, address):
        self.address = address

    def add_exclusion(self, user):
        self.exclusions.append(user)

    def confirm_addr(self):
        self.confirmed_addr = True

    def confirm_all(self):
        self.confirmed_all = True

    def is_complete(self):
        return self.confirmed_all
