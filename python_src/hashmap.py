class HashMap:
    def __init__(self):
        self.items = {}
        self.num_items = 0

    def insert(self, state, role, depth, move, value):
        self.items[str(state) + str(role)] = (depth, move, value)
        self.num_items += 1
        if self.num_items > 8 * len(self.items):
            self._rehash()

    def get(self, state, role):
        return self.items[str(state) + str(role)]

    def update(self, state, role, depth, move, value):
        key = str(state) + str(role)

        if key not in self.items:
            self.insert(state, role, depth, move, value)
        else:
            self.items[key] = (depth, move, value)

    def __getitem__(self, state, role):
        return self.get(str(state) + str(role))

    def __setitem__(self, state, role, depth, move, value):
        self.insert(state, role, depth, move, value)

    def _rehash(self):
        new_items = {}
        for k, v in self.items.items():
            new_items[k] = v
        self.items = new_items

    def remove(self, key):
        if key in self.items:
            del self.items[key]
            self.num_items -= 1
