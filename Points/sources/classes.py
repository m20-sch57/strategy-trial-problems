import json


FIELD_SIZE = 10


class GameState:
    def __init__(self):
        self.field = [['.' for i in range(FIELD_SIZE)] for j in range(FIELD_SIZE)]
    
    def toString(self):
        return json.dumps(self.field)

    def fromString(self, s):
        self.field = json.loads(s)


class Turn:
    def __init__(self, x, y):
        self.x, self.y = x, y
    
    def toString(self):
        return json.dumps([self.x, self.y])

    def fromString(self, s):
        self.x, self.y = json.loads(s)[0], json.loads(s)[1]
