from random import randint

def Strategy(module, gameState, playerId):
    size = len(gameState.field)
    while True:
        i = randint(0, size - 1) 
        j = randint(0, size - 1)
        if gameState.field[i][j] == '.':
            return module.Turn(i, j)
