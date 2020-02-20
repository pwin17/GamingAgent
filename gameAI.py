import copy
import random

class Node:
    def __init__(self):
        self.parent = None 
        self.position = None
        self.child = []
        self.action = None 
        self.state = None
        self.utility = None

class State:
    def __init__(self, p1, p2, boardSize, turn, opponent):
        self.p1 = p1 #list of tuples (row,column)
        self.p2 = p2 #list of tuples
        self.turn = turn 
        self.opponent = opponent
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
    gameState = State([],[],(row,col),1,2) ##p1 always start
    for i in range(0,pieces):
        for j in range(col):
            gameState.p1.append((i,j))
    for i in range(row-pieces, row):
        for j in range(col):
            gameState.p2.append((i,j))
    return gameState

def transition(currentState, move, initial_pos, actually_change):
    newState = copy.deepcopy(currentState)
    if newState.turn == 1:
        if actually_change:
            newState.turn = 2
            newState.opponent = 1
        newState.p1.remove(initial_pos)
        newState.p1.append(move)
    else:
        if actually_change:
            newState.turn = 1
            newState.opponent = 2
        newState.p2.remove(initial_pos)
        newState.p2.append(move)
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
    for (x,y) in currentState.p1:
        row, col = currentState.boardSize
        if y == row-1:
            return (True, "p1")
    for (x,y) in currentState.p2:
        if y == 0:
            return (True, "p2")
    return (False, "")

def evasiveUtility(currentState):
    if currentState.turn == 1:
        remaining = len(currentState.p1)
    else:
        remaining = len(currentState.p2)
    evasive = remaining + random.randrange(0,1)
    return evasive

def conquerorUtility(currentState):
    if currentState.turn == 1:
        remaining = len(currentState.p2)
    else:
        remaining = len(currentState.p1)
    conqueror = (0-remaining) + random.randrange(0,1)
    return conqueror

def minimax(currentState):
    allMoves = moveGenerator(currentState) #list of list of tuples [ [(,),(,)], ...]
    tree = []
    found = False
    print(allMoves)
    print("____________________")
    for i in allMoves: #starting to branch 1 depth from root
        found = False
        for node in tree:
            if i[0] == node.position:
                node.child.append(i[1])
                found = True
        if not found:
            newNode = Node()
            newNode.position = i[0]
            newNode.child.append(i[1])
            newNode.state = copy.deepcopy(currentState)
            tree.append(newNode)
    mini = []
    maxi = []
    level1 = []
    for i in tree: #1st moves of current player
        for c in i.child:
            newNode = Node() #populate node
            newNode.position = c
            newNode.parent = i.position #link them to tree
            newNode.state = transition(i.state,newNode.position ,i.position, False) #hypothetically moving
            allMoves = moveGenerator(newNode.state) #See possible moves of current position
            for m in allMoves:
                newNode.child.append(m[1]) #Add possible moves to child
            # if child move is going to eat opponent's pawn
            if i.state.opponent == 1: 
                if c in i.state.p1:
                    newNode.state.p1.remove(c)
            else:
                if c in i.state.p2:
                    newNode.state.p2.remove(c)
            #try changing turns
            op = newNode.state.opponent
            newNode.state.opponent = newNode.state.turn
            newNode.state.turn = op 
            allMoves = moveGenerator(newNode.state) #possible moves of opponent's next turn

            # for move in allMoves:
            #     nextPlayer = Node()
            #     nextPlayer.parent = move[0]
            #     nextPlayer.position = move[1]
            #     nextPlayer.state = transition(newNode.state, move[1],move[0], True) #actually moves
            #     nextLevelAllMoves = moveGenerator(nextPlayer.state)


                

            # print("new node and its possible moves")
            # print(newNode.position,allMoves)
            # print("______________")
            

            

    
            





    

        

def playgame(h_white, h_black, gamestate):
    win, winner = isGameOver(gamestate)
    while not win:
         evasiveUtility(gamestate)


gs = initialState(10,2,1)
displayState(gs)

print("All Moves")
print(moveGenerator(gs))
print("___________")
print("Game Over?")
print(isGameOver(gs))
print("_____________")
print("minmax")
minimax(gs)