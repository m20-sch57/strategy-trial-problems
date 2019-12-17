def Strategy(module, gameState, playerId):
    size = len(gameState.field)
    for i in range(size):
        for j in range(size):
            if gameState.field[i][j] == '.':
                return module.Turn(i, j)
