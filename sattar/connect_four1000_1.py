import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import time
from Tkinter import *

def evaluate_line(line, p):
    new_line = np.copy(line)
    new_line[new_line==0] = p
    if not contains_four_elements_in_row(new_line, p):
        # there is no chance for p to win through this line
        return 0.0

    if contains_n_elements_in_row(line, p, 4):
        # (#rows * 4 + #cols * 4 + #diags*4) * 2
        return 100
    elif contains_n_elements_in_row(line, p, 3):
        return 50
    elif contains_n_elements_in_row(line, p, 2):
        return 20
    elif contains_n_elements_in_row(line, p, 1):
        return 10.0

    return 1.0
   
def evaluate(S, p):
    value = 0.0
    # count rows
    for rowIdx in range(S.shape[0]):
        row = S[rowIdx, :]
        value += evaluate_line(row, p)
        value -= evaluate_line(row, -p)

    # count cols
    for colIdx in range(S.shape[1]):
        column = S[:, colIdx]
        value += evaluate_line(column, p)
        value -= evaluate_line(column, -p)

    # count diagonals
    for i in range(-2, 4):
        value += evaluate_line(S.diagonal(i), p)
        value -= evaluate_line(S.diagonal(i), -p)

    rotatedS = np.rot90(S)
    for i in range(-3, 3):
        value += evaluate_line(rotatedS.diagonal(i), p)
        value -= evaluate_line(rotatedS.diagonal(i), -p)

    return value

def move_still_possible(S):
    return not (S[S==0].size == 0)

def get_possible_moves(S):
    possibleMoves = []
    for colIdx in range(S.shape[1]):
        column = S[:, colIdx]
        zeroIndexes = np.where(column == 0)[0]
        if zeroIndexes.size > 0:
            rowIdx = zeroIndexes.max()
            possibleMoves.append((rowIdx, colIdx))
    return possibleMoves

# find the next best move
def minmax(S, p, depth, maximize=True):
    possibleMoves = get_possible_moves(S)
    if 0 == depth or 0 == len(possibleMoves):
        if maximize:
            return (evaluate(S, p), )
        else:
            return (evaluate(S, -p), )

    if move_was_winning_move(S, -p):
       if maximize:
           return (-np.inf, )
       else:
           return (np.inf, )

    best_move = possibleMoves[0]
    if maximize:
        mmv = -np.inf
        for move in possibleMoves:
            next_S = np.copy(S)
            next_S[move] = p
            next_mmv = minmax(next_S, -p, depth - 1, False)[0]
            if mmv < next_mmv:
                best_move = move
                mmv = next_mmv
    else:
        mmv = np.inf
        for move in possibleMoves:
            next_S = np.copy(S)
            next_S[move] = p
            next_mmv = minmax(next_S, -p, depth - 1, True)[0]
            if mmv > next_mmv:
                best_move = move
                mmv = next_mmv


    return (mmv, best_move)

def move_using_minmax(S, p, depth):
    S[minmax(S, p, depth)[1]] = p
    return S

def move_at_random(S, p):
    possibleMoves = get_possible_moves(S)
    i = np.random.randint(len(possibleMoves))
    
    S[possibleMoves[i]] = p

    return S

def contains_n_elements_in_row(vector, p, n):
    for i in range(vector.size - n + 1):
        if vector[i] == p and vector[i:(i+n)].sum() == n * p:
            return True
    return False

def contains_four_elements_in_row(vector, p):
    return contains_n_elements_in_row(vector, p, 4)

def move_was_winning_move(S, p):
    for rowIdx in range(S.shape[0]):
        row = S[rowIdx, :]
        if contains_four_elements_in_row(row, p):
            return True

    for colIdx in range(S.shape[1]):
        column = S[:, colIdx]
        if contains_four_elements_in_row(column, p):
            return True

    # check diagonals with length at least 4
    for i in range(-2, 4):
        if contains_four_elements_in_row(S.diagonal(i), p):
            return True

    rotatedS = np.rot90(S)
    for i in range(-3, 3):
        if contains_four_elements_in_row(rotatedS.diagonal(i), p):
            return True

    return False



# relate numbers (1, -1, 0) to symbols ('x', 'o', ' ')
symbols = {1:'y', -1:'r', 0:' '}

# print game state matrix using symbols
def print_game_state(S):
    B = np.copy(S).astype(object)
    for n in [-1, 0, 1]:
        B[B==n] = symbols[n]
    print B

def plot_tournament_statistics(tournament, samplingCount, depth):
    data = []
    legends = []
    if tournament[-1]:
        data.append([-1] * tournament[-1])
        legends.append('Player O won')
    if tournament[0]:
        data.append([0] * tournament[0])
        legends.append('Draw')
    if tournament[1]:
        data.append([1] * tournament[1])
        legends.append('Player 1 won')
    n, bins, patches = plt.hist(data, 1)
    plt.ylabel('Number of games')
    plt.title('Tournament result after %s games in total with depth %s' % (samplingCount, depth))
    plt.legend(patches, legends)
    plt.show()
def statisticsArr(gameState,statistics):
    line_in=0
    column_in=0
    for line_in in range(19):
        for column_in in range(19):
            if gameState[line_in][column_in]==1:
                statistics[line_in][column_in] = statistics[line_in][column_in] + 1
    return statistics
def run_tournament(samplingCount, depth,counter):
    # tournament statistics
    tournament = {1:0, -1:0, 0:0}
    statistics = np.zeros((19, 19),dtype=int)

    for epoch in range(samplingCount):
        print counter
        counter = counter + 1

        # initialize 6x7 tic tac toe board
        gameState = np.zeros((19, 19), dtype=int)

        # initialize player number, move counter
        player = 1
        mvcntr = 1

        # initialize flag that indicates win
        noWinnerYet = True
    
        while move_still_possible(gameState) and noWinnerYet:
            # get player symbol
            name = symbols[player]
            # print '%s falls' % name

            if 1 == player:
              # apply depth restricted search to do best move
              gameState = move_using_minmax(gameState, player, depth)
            else:
              # let player move at random
              gameState = move_at_random(gameState, player)

            # print current game state
            #print_game_state(gameState)
        
            # evaluate game state
            if move_was_winning_move(gameState, player):
                # print 'player %s wins after %d moves' % (name, mvcntr)
                noWinnerYet = False

                # update tournament statistics
                # respective to the winner
                tournament[player] += 1
                if player == -1:
                  alma = 1
                    #import sys
                  #sys.exit("Error message")

            # switch player and increase move counter
            player *= -1
            mvcntr +=  1


        if noWinnerYet:
            tournament[0] += 1
            print 'game ended in a draw' 
        statistics = statisticsArr(gameState,statistics)
    graphColors(statistics)
    graphNumbers(statistics)
    print '\nWins and draws after %s sample:' % samplingCount
    return tournament
def proportion(totalNumber,findNumber):
    return (findNumber*100)/totalNumber
class Profiler(object):
    def __enter__(self):
        self._startTime = time.time()
         
    def __exit__(self, type, value, traceback):
        print "Elapsed time: {:.3f} sec".format(time.time() - self._startTime)
        print format(time.time() - self._startTime)
def pieWinLostDraw(tour,numberOfGames,threeDepth):
    figure(1, figsize=(6,6))
    ax = axes([0.1, 0.1,0.8, 0.8])

    labels = 'Wins','Losts'
    fracs = [proportion(numberOfGames,tour[1]), proportion(numberOfGames,tour[-1])]
    explode=(0,0)

    pie(fracs, explode=explode, labels=labels,autopct='%1.1f%%', shadow=True, startangle=90)

    title('Statistics after %s games where depth is %s' % (numberOfGames, threeDepth), bbox={'facecolor':'0.8', 'pad':5})

    show()

def  graphColors(a):
    root=Tk()
    column_coord=np.array([50,77,104,131,158,185,212,239,266,293,320,347,374,401,428,455,482,509,536,563])
    line_coord= np.array([75,102,129,156,183,210,237,264,291,318,345,372,399,426,453,480,507,534,561,588])
    text_coord=np.array([67,90,121,145,170,197,227,253,279,305,330,358,388,410,440,470,500,525,550])
    canvas=Canvas(root,width=1200,height=1200)
    canvas.pack(fill=BOTH)
    z=0
    i=0
    for element  in column_coord:
        canvas.create_line(column_coord[i],75,column_coord[i],588,fill="black")
        i =i+1
    j=0
    for elem in  line_coord:
        canvas.create_line(50,line_coord[j],564,line_coord[j],fill="black")
        j=j+1
    z=0
    for el in text_coord:
        canvas.create_text(text_coord[z],65,text=str(z))
        z=z+1
    z=0
    line_in=0
    column_in=0
    x_in=50
    y_in=75

    for line_in in range(19):
        for column_in in range(19):
            if a[line_in][column_in]>=0 and a[line_in][column_in]<50:
                canvas.create_oval(x_in+column_in*27,y_in+line_in*27,x_in+(column_in*27)+27,y_in+(line_in*27)+27,fill= "lime")
            elif a[line_in][column_in]>=50 and a[line_in][column_in]<100:
                canvas.create_oval(x_in+column_in*27,y_in+line_in*27,x_in+(column_in*27)+27,y_in+(line_in*27)+27,fill="tomato")
            elif a[line_in][column_in]>=100 and a[line_in][column_in]<150:
                canvas.create_oval(x_in+column_in*27,y_in+line_in*27,x_in+(column_in*27)+27,y_in+(line_in*27)+27,fill="darkslateblue")
            elif a[line_in][column_in]>=150 and a[line_in][column_in]<200:
                canvas.create_oval(x_in+column_in*27,y_in+line_in*27,x_in+(column_in*27)+27,y_in+(line_in*27)+27,fill="darkslategray")
            elif a[line_in][column_in]>=200:
                canvas.create_oval(x_in+column_in*27,y_in+line_in*27,x_in+(column_in*27)+27,y_in+(line_in*27)+27,fill="darkgreen")
            else:
                canvas.create_oval(x_in+column_in*27,y_in+line_in*27,x_in+(column_in*27)+27,y_in+(line_in*27)+27,fill="black")
    root.mainloop()
def  graphNumbers(a):
    root=Tk()
    column_coord=np.array([50,77,104,131,158,185,212,239,266,293,320,347,374,401,428,455,482,509,536,563])
    line_coord= np.array([75,102,129,156,183,210,237,264,291,318,345,372,399,426,453,480,507,534,561,588])
    text_coord=np.array([67,90,121,145,170,197,227,253,279,305,330,358,388,410,440,470,500,525,550])
    canvas=Canvas(root,width=1200,height=1200)
    canvas.pack(fill=BOTH)
    z=0
    i=0
    for element  in column_coord:
        canvas.create_line(column_coord[i],75,column_coord[i],588,fill="black")
        i =i+1
    j=0
    for elem in  line_coord:
        canvas.create_line(50,line_coord[j],564,line_coord[j],fill="black")
        j=j+1
    z=0
    for el in text_coord:
        canvas.create_text(text_coord[z],65,text=str(z))
        z=z+1
    z=0
    line_in=0
    column_in=0
    x_in=50
    y_in=75
    for line_in in range(19):
        for column_in in range(19):
            if a[line_in][column_in]!=0:
                canvas.create_text(text_coord[column_in],25+text_coord[line_in],text=str(a[line_in][column_in]))
    root.mainloop()

if __name__ == '__main__':
    samplingCount = 1000
    tournaments = []
    for depth in range(1, 2):
        print "\n using depth = ", depth
        with Profiler() as p:
            tournament = run_tournament(samplingCount, depth,0)
            tournaments.append(tournament)

    print "\nResult ", tournaments
    for i in range(len(tournaments)):
        pieWinLostDraw(tournaments[i],samplingCount,i+1)
