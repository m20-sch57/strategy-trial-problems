from server.gameStuff import *
from app import app
from flask import render_template
import os
import json
from server.commonFunctions import problemFolder


FIELD_SIZE = 10
MaxScore = 100
TimeLimit = 1
TurnLimit = 1000
DIR = [(0, 1), (1, 0), (-1, 0), (0, -1)]


class GameState:
    def __init__(self):
        self.field = [['.' for i in range(FIELD_SIZE)] for j in range(FIELD_SIZE)]

    def toString(self):
        return json.dumps(self.field)

    def fromString(self, s):
        self.field = json.loads(s)



class FullGameState:
    def __init__(self):
        self.field = [['.' for i in range(FIELD_SIZE)] for j in range(FIELD_SIZE)]

    def correct_cell(self, x, y):
        return x >= 0 and x < FIELD_SIZE and y >= 0 and y < FIELD_SIZE

    def border_cell(self, x, y):
        return x == 0 or x == FIELD_SIZE - 1 or y == 0 or y == FIELD_SIZE - 1
    
    def game_finished(self):
        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                if self.field[i][j] == '.':
                    return False
        return True

    def counter(self):
        score = [0, 0]
        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                if self.field[i][j] == 'R':
                    score[0] += 1
                if self.field[i][j] == 'G':
                    score[1] += 1
        score[0] = (score[0] / (FIELD_SIZE ** 2)) * MaxScore
        score[1] = (score[1] / (FIELD_SIZE ** 2)) * MaxScore
        return score

    def color_area(self, c):
        # c - turn color
        used = [[False for i in range(FIELD_SIZE)] for j in range(FIELD_SIZE)]

        def dfs(x, y):
            if used[x][y] or self.field[x][y] == c:
                return
            used[x][y] = True
            for elem in DIR:
                curx = x + elem[0]
                cury = y + elem[1]
                if self.correct_cell(curx, cury):
                    dfs(curx, cury)
        
        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                if self.border_cell(i, j) and not used[i][j]:
                    dfs(i, j)
        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                if not used[i][j]:
                    self.field[i][j] = c


def gameStateRep(full: FullGameState, playerId: int) -> GameState:
    result = GameState()
    result.field = full.field
    return result


class Logs:
    def __init__(self):
        self.logs = []

    def processResults(self, results):
        self.results = results

    def update(self, game: FullGameState):
        new_field = [['.' for i in range(FIELD_SIZE)] for i in range(FIELD_SIZE)]
        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                new_field[i][j] = [game.field[i][j]]
                # if [i, j] == fullTurn:
                # new_field[i][j].append(1)
        self.logs.append(new_field)
        # print("UPDATED")
        # print(new_field)
        # print()

    def show(self, probId, baseParams):
        # print(self.logs)
        with app.app_context():
            logPath = os.path.join('problems', problemFolder(probId), 'logs.html.j2')
            data = render_template(
                logPath,
                jsonlogs = json.dumps(self.logs), 
                logs = self.logs,
                res1 = self.results[0].goodStr(), 
                res2 = self.results[1].goodStr(), 
                strId = problemFolder(probId), 
                **baseParams
            )
        return data


class Turn:
    def __init__(self, x=0, y=0):
        self.x, self.y = x, y
    
    def toString(self):
        return json.dumps([self.x, self.y])

    def fromString(self, s):
        self.x, self.y = json.loads(s)[0], json.loads(s)[1]


def nextPlayer(playerId: int) -> int:
    return 1 - playerId


def makeTurn(gameState: FullGameState, playerId: int, turn: Turn, logs = None) -> list:
    charList = ['R', 'G']
    x, y = turn.x, turn.y
    if not gameState.correct_cell(x, y):
        return [TurnState.Incorrect]
    if gameState.field[x][y] != '.':
        return [TurnState.Incorrect]
    c = charList[playerId]
    gameState.field[x][y] = c
    gameState.color_area(c)
    if logs != None:
        logs.update(gameState)
    if gameState.game_finished():
        score = gameState.counter()
        return [
            TurnState.Last, 
            [Result(StrategyVerdict.Ok, score[0]), 
            Result(StrategyVerdict.Ok, score[1])]
        ]
    else:
        return [TurnState.Correct, gameState, nextPlayer(playerId)]
    
    