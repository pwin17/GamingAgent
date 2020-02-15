import copy

class State:
    def __init__(self, p1, p2, boardSize, turn):
        self.p1 = p1 #list of tuples (row,column)
        self.p2 = p2 #list of tuples
        self.turn = turn 
        self.boardSize = boardSize #(row, column)

def displayState(currentState):
    row, col = currentState.boardSize
    x = ""
    for i in range(row):
        x=""
        for j in range(col):
            if (i,j) in currentState.p1:
                x = x + "O"
            elif (i,j) in currentState.p2:
                x = x + "X"
            else:
                x = x + "."
        print(x)

def initialState(row, col, pieces):
    gameState = State([],[],(row,col),1) ##p1 always start
    for i in range(0,pieces):
        for j in range(col):
            gameState.p1.append((i,j))
    for i in range(row-pieces, row):
        for j in range(col):
            gameState.p2.append((i,j))
    return gameState

def transition(currentState, move, initial_pos):
    newState = copy.deepcopy(currentState)
    if newState.turn == 1:
        newState.turn = 2
        newState.p1.replace(initial_pos,move)
    else:
        newState.turn = 1
        newState.p2.replace(initial_pos, move)
    return newState
    
def p1_oneMoveGenerator(position, boardsize):
    row, col = boardsize
    pos_row, pos_col = position
    possible_new_position = []
    possible_new_position.append((pos_row+1,pos_col)) #go front first
    if pos_row+1 <= row-1:
        newJ = pos_row+1
    if pos_col-1 >=0:
        possible_new_position.append((newJ,pos_col-1))
    if pos_col+1 <=col-1:
        possible_new_position.append((newJ,pos_col+1))
    return possible_new_position

def p2_oneMoveGenerator(position, boardsize):
    row, col = boardsize
    pos_row, pos_col = position
    possible_new_position = []
    possible_new_position.append((pos_row-1,pos_col)) #go front first
    if pos_row-1 >= 0:
        newJ = pos_row-1
    if pos_col-1 >=0:
        possible_new_position.append((newJ,pos_col-1))
    if pos_col+1 <=col-1:
        possible_new_position.append((newJ,pos_col+1))
    return possible_new_position

def moveGenerator(currentState):
    possibleMoves = []
    if currentState.turn == 1:
        for (i,j) in currentState.p1:            
            physicallyPossible = p1_oneMoveGenerator((i,j),currentState.boardSize)
            if physicallyPossible[0] in currentState.p2:
                physicallyPossible.remove(physicallyPossible[0])
            for (ni,nj) in physicallyPossible:
                if (ni,nj) in currentState.p1:
                    physicallyPossible.remove((ni,nj))
            
            for (ni,nj) in physicallyPossible:
                possibleMoves.append([(i,j),(ni,nj)])

    elif currentState.turn == 2:
        for (i,j) in currentState.p2:            
            physicallyPossible = p2_oneMoveGenerator((i,j),currentState.boardSize)
            if physicallyPossible[0] in currentState.p1:
                physicallyPossible.remove(physicallyPossible[0])
            for (ni,nj) in physicallyPossible:
                if (ni,nj) in currentState.p2:
                    physicallyPossible.remove((ni,nj))
            for (ni,nj) in physicallyPossible:
                possibleMoves.append([(i,j),(ni,nj)])

    return possibleMoves

def isGameOver(currentState):
    if currentState.p1 and currentState.p2:
        return (False,"")
    else:
        if not currentState.p1:
            return (True, "p1")
        else:
            return (True, "p2")
    for (x,y) in current.p1:
        if y == row-1:
            return (True, "p1")
    for (x,y) in current.p2:
        if y == 0:
            return (True, "p2")
    return (False, "")



gs = initialState(4,4,1)
displayState(gs)
print(moveGenerator(gs))
print(isGameOver(gs))
