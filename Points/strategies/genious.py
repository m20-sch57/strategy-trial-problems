def Strategy(module, gameState, playerId):
    size = len(gameState.field)
    for i in range(size):
        for j in range(i % 2, size, 2):
            if gameState.field[i][j] == '.':
                return module.Turn(i, j)
    for i in range(size):
        for j in range(1 - i % 2, size, 2):
            if gameState.field[i][j] == '.':
                return module.Turn(i, j)
