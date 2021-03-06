import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import time
from Tkinter import *

def minmax(S, p, depth, maximize=True):
    possibleMove = possibleMoves(S)
    if 0 == depth or 0 == len(possibleMove):
        if maximize:
            return (evaluate(S, p), )
        else:
            return (evaluate(S, -p), )

    if terminalMovement(S, -p):
       if maximize:
           return (-np.inf, )
       else:
           return (np.inf, )

    best_move = possibleMove[0]
    if maximize:
        mmv = -np.inf
        for move in possibleMove:
            next_S = np.copy(S)
            next_S[move] = p
            next_mmv = minmax(next_S, -p, depth - 1, False)[0]
            if mmv < next_mmv:
                best_move = move
                mmv = next_mmv
    else:
        mmv = np.inf
        for move in possibleMove:
            next_S = np.copy(S)
            next_S[move] = p
            next_mmv = minmax(next_S, -p, depth - 1, True)[0]
            if mmv > next_mmv:
                best_move = move
                mmv = next_mmv


    return (mmv, best_move)

class Profiler(object):
    def __enter__(self):
        self._startTime = time.time()
         
    def __exit__(self, type, value, traceback):
        print "Elapsed time: {:.3f} sec".format(time.time() - self._startTime)
        print format(time.time() - self._startTime)

def evaluationFun(line, p):
    new_line = np.copy(line)
    new_line[new_line==0] = p
    if not terminalCheck(new_line, p):
        return 0
    if layerComputation(line, p, 4):
        return 100.0
    elif layerComputation(line, p, 3):
        return 3
    elif layerComputation(line, p, 2):
        return 2
    elif layerComputation(line, p, 1):
        return 1

    return 1.0

def layerComputation(vector, p, n):
    for i in range(vector.size - n + 1):
        if vector[i] == p and vector[i:(i+n)].sum() == n * p:
            return True
    return False

def minmaxMovement(grid, pl, depth):
    grid[minmax(grid, pl, depth)[1]] = pl
    return grid

def evaluate(grid, p):
    value = 0.0
    # count rows
    for rowIdx in range(grid.shape[0]):
        row = grid[rowIdx, :]
        value += evaluationFun(row, p)
        value -= evaluationFun(row, -p)
    # count cols
    for colIdx in range(grid.shape[1]):
        column = grid[:, colIdx]
        value += evaluationFun(column, p)
        value -= evaluationFun(column, -p)
    # count diagonals
    for i in range(-2, 4):
        value += evaluationFun(grid.diagonal(i), p)
        value -= evaluationFun(grid.diagonal(i), -p)
    rotatedgrid = np.rot90(grid)
    for i in range(-3, 3):
        value += evaluationFun(rotatedgrid.diagonal(i), p)
        value -= evaluationFun(rotatedgrid.diagonal(i), -p)

    return value

def checkFullness(grid):
    return not (grid[grid==0].size == 0)

def possibleMoves(grid):
    possibleMoves = []
    for colIdx in range(grid.shape[1]):
        column = grid[:, colIdx]
        zeroIndexes = np.where(column == 0)[0]
        if zeroIndexes.size > 0:
            rowIdx = zeroIndexes.max()
            possibleMoves.append((rowIdx, colIdx))
    return possibleMoves

def randomMovement(grid, p):
    possibleMove = possibleMoves(grid)
    i = np.random.randint(len(possibleMove))
    
    grid[possibleMove[i]] = p

    return grid

def terminalCheck(vector, p):
    return layerComputation(vector, p, 4)

def terminalMovement(grid, p):
    for rowIdx in range(grid.shape[0]):
        row = grid[rowIdx, :]
        if terminalCheck(row, p):
            return True

    for colIdx in range(grid.shape[1]):
        column = grid[:, colIdx]
        if terminalCheck(column, p):
            return True

    for i in range(-2, 4):
        if terminalCheck(grid.diagonal(i), p):
            return True

    rotatedGrid = np.rot90(grid)
    for i in range(-3, 3):
        if terminalCheck(rotatedGrid.diagonal(i), p):
            return True

    return False


symbols = {1:'x', -1:'o', 0:'0'}
def terminalVisualisation(grid):
    board = np.copy(grid).astype(object)
    for n in [-1, 0, 1]:
        board[board==n] = symbols[n]
    print board


def start(playedGames, depth):
    game = {1:0, -1:0, 0:0}
    statistics = np.zeros((6 , 7),dtype=int)
    for epoch in range(playedGames):
        gameState = np.zeros((6, 7), dtype=int)
        player = 1
        counter = 1
        noWinnerYet = True    
        while checkFullness(gameState) and noWinnerYet:
            name = symbols[player]
            if 1 == player:
              gameState =  minmaxMovement(gameState, player,depth)
              #gameState =  randomMovement(gameState, player)
            else:
              gameState =  randomMovement(gameState, player)
            if terminalMovement(gameState, player):
                noWinnerYet = False
                game[player] = game[player]+1
            if player==1:
                player = -1
            else:
                player = 1
            counter =  counter + 1
        if noWinnerYet:
            game[0] = game[0]+1
            print 'draw'
        statistics = statisticsArr(gameState,statistics)
        #terminalVisualisation(gameState)
    graphStart(statistics,playedGames)
    print '\nStatistics after %s sample:' % playedGames
    return game

def statisticsArr(gameState,statistics):
    line_in=0
    column_in=0
    for line_in in range(6):
        for column_in in range(7):
            if gameState[line_in][column_in]==1:
                statistics[line_in][column_in] = statistics[line_in][column_in] + 1
    return statistics

def  graphStart(a,games):
    root=Tk()
    column_coord=np.array([77,104,131,158,185,212])
    line_coord= np.array([102,129,156,183,210])
    text_coord=np.array([67,90,121,145,170,197,227])
    canvas=Canvas(root,width=300,height=300)
    canvas.pack(fill=BOTH)
    z=0
    for el in text_coord:
        canvas.create_text(text_coord[z],65,text=str(z))
        z=z+1
    canvas.create_rectangle(50,75,240,235,outline="black")
    i=0
    for element  in column_coord:
        canvas.create_line(column_coord[i],75,column_coord[i],235,fill="black")
        i =i+1
    j=0
    for elem in  line_coord:
        canvas.create_line(50,line_coord[j],240,line_coord[j],fill="black")
        j=j+1
    line_in=0
    column_in=0
    x_in=50
    y_in=75
    for line_in in range(6):
        for column_in in range(7):
            if a[line_in][column_in]>=0 and a[line_in][column_in]<50:
                canvas.create_oval(x_in+column_in*27,y_in+line_in*27,x_in+(column_in*27)+27,y_in+(line_in*27)+27,fill= "lime")
            if a[line_in][column_in]>=50 and a[line_in][column_in]<100:
                canvas.create_oval(x_in+column_in*27,y_in+line_in*27,x_in+(column_in*27)+27,y_in+(line_in*27)+27,fill="tomato")
            if a[line_in][column_in]>=100 and a[line_in][column_in]<150:
                canvas.create_oval(x_in+column_in*27,y_in+line_in*27,x_in+(column_in*27)+27,y_in+(line_in*27)+27,fill="darkslateblue")
            if a[line_in][column_in]>=150 and a[line_in][column_in]<200:
                canvas.create_oval(x_in+column_in*27,y_in+line_in*27,x_in+(column_in*27)+27,y_in+(line_in*27)+27,fill="darkslategray")
            if a[line_in][column_in]>=200:
                canvas.create_oval(x_in+column_in*27,y_in+line_in*27,x_in+(column_in*27)+27,y_in+(line_in*27)+27,fill="darkgreen")
    root.mainloop()


def proportion(totalNumber,findNumber):
    return (findNumber*100)/totalNumber

def pieWinLostDraw(tour,numberOfGames,threeDepth):
    figure(1, figsize=(6,6))
    ax = axes([0.1, 0.1,0.8, 0.8])

    labels = 'Wins','Losts'
    fracs = [proportion(numberOfGames,tour[1]), proportion(numberOfGames,tour[-1])]
    explode=(0,0)

    pie(fracs, explode=explode, labels=labels,autopct='%1.1f%%', shadow=True, startangle=90)

    title('Statistics after %s games where depth is %s' % (numberOfGames, threeDepth), bbox={'facecolor':'0.8', 'pad':5})

    show()

if __name__ == '__main__':
    playedGames = 5
    result = []
    for depth in range(1, 2):
        print "Starting from depth = ", depth
        with Profiler() as p:
            game = start(playedGames, depth)
            result.append(game)

    print "Results ", result
    playedGames = len(result)
    i = 0

    while i<playedGames:
        pieWinLostDraw(result[i],playedGames,i+1)
        i = i + 1
