import copy
import random
import time

class Node:
    def __init__(self, state, parent, children, action,utility):
        self.state = state
        self.parent = parent
        self.children = children
        self.action = action 
        self.utility = utility
        if parent is None: 
            self.depth = 0
        else:
            self.depth = self.parent.depth + 1
    def get_p1_positions(self):
        return self.state.p1
    def get_p2_positions(self):
        return self.state.p2
    def get_turn(self):
        return self.state.turn

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

def transition(currentState, move, initial_pos):
    newState = copy.deepcopy(currentState)
    if currentState.turn == 1:
        if move in newState.p2:
            newState.p2.remove(move)
        newState.turn = 2
        newState.opponent = 1
        newState.p1.remove(initial_pos)
        newState.p1.append(move)
    else: 
        if move in newState.p1:
            newState.p1.remove(move)
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
    evasive = remaining + random.random()
    return evasive

def conquerorUtility(currentState):
    if currentState.turn == 1:
        remaining = len(currentState.p2)
    else:
        remaining = len(currentState.p1)
    conqueror = (0-remaining) + random.random()
    return conqueror

def minimax(currentState, max_depth, utility_function):
    """Input: current state of the board, depth for minimax algorithm, utility function
    Output: the move (whose turn, from position, to position)"""

    #create the trees and a list of all nodes
    #the list of all nodes contains the lists of all nodes in each level of the trees
    player = currentState.turn
    rootNode = Node(currentState,None, [], None, 0)

    all_nodes = []
    all_nodes.append([rootNode])
    current_depth = 0
    while current_depth < max_depth:
        current_level_node_list =[]
        current_depth +=1 
        for parent_node in all_nodes[-1]: ###traversing through the leaves of the tree and generate its children
            if isGameOver(parent_node.state)[0] != True:
                possible_moves = moveGenerator(parent_node.state)
                for move in possible_moves:
                    newState = transition(parent_node.state, move[0], move[1])
                    child_node = Node(newState, parent_node, [], move, 0)
                    parent_node.children.append(child_node)
                    current_level_node_list.append(child_node)
        all_nodes.append(current_level_node_list)
    # for i in all_nodes:
        # print(len(i))
    
    # calculating the utility of all the leaf nodes:
    for leaf_node in all_nodes[max_depth]:
        leaf_node.utility = utility_function(leaf_node.state, player)
    # calculating the utility of the upper level nodes:
    for depth in range(max_depth-1, -1, -1): #from level of parents of the leaves to root level
        for node in all_nodes[depth]:
            if node.get_turn() == player:
                if len(node.children) != 0:
                    node.utility = max([children_node.utility for children_node in node.children])
                # else: 
                #     node.utility =float('-inf') # When the player's next move is in the winning state, there will be no leaf nodes
            else: 
                if len(node.children) != 0:
                    node.utility = min([children_node.utility for children_node in node.children])
                # else: 
                #     node.utility = float('inf')
    # find and return the best move from the children of the root
    for root_child in rootNode.children:
        if rootNode.utility == root_child.utility:
            return root_child.action

def playgame(heuristic_p1, heuristic_p2, board_state,max_depth):
    win, winner = isGameOver(board_state)
    # displayState(board_state)
    while not win:
        if board_state.turn == 1:
            next_move = minimax(board_state, max_depth, heuristic_p1)
        else:
            next_move = minimax(board_state, max_depth, heuristic_p2)
        # print(next_move)
        board_state = transition(board_state, next_move[0], next_move[1])
        # displayState(board_state)
        win, winner = isGameOver(board_state) 

    # displayState(board_state)   
    print(win, winner)


gs = initialState(8,8,2)
displayState(gs)

# print("All Moves")
# print(moveGenerator(gs))
# print("___________")
# print("Game Over?")
# print(isGameOver(gs))
# print("_____________")
print("minmax")
s = time.time()
minimax(gs)
e = time.time()
print(e-s)