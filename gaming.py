import copy
import random 

#COEFFICIENT FOR CUSTOMIZED UTILITY
PAWN_COEFFICIENT = 2 # points per pawn
ROW_COEFFICIENT = 2 # points for expanding forward
FAKE_INFINITY = 9999 
SUPPORT_COEFFICIENT = 1 

"""
Representation & convention
position: tuples (row position, column position)
board size: tuples (number of rows, number of columns)
player: 1, 2
player 1 always goes first for a new game
"""

class State:
    def __init__(self, p1, p2, boardSize, turn):
        self.p1 = p1 #list of tuples (row,column)
        self.p2 = p2 #list of tuples
        self.turn = turn 
        self.boardSize = boardSize #(row, column)

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

def transition(currentState, position_before, position_after):
    newState = copy.deepcopy(currentState)
    if newState.turn == 1:
        newState.turn = 2
        newState.p1.remove(position_before) 
        newState.p1.append(position_after)
        if position_after in newState.p2:
            newState.p2.remove(position_after)
    else:
        newState.turn = 1
        newState.p2.remove(position_before)
        newState.p2.append(position_after)
        if position_after in newState.p1:
            newState.p1.remove(position_after)
    return newState
    
def p1_oneMoveGenerator(position, boardsize): 
    row, col = boardsize
    pos_row, pos_col = position
    possible_new_position = []
     #go front first
    if pos_row +1 <= row-1:
        newJ = pos_row+1
        possible_new_position.append((pos_row+1,pos_col))
        if pos_col-1 >=0:
            possible_new_position.append((newJ,pos_col-1))
        if pos_col+1 <=col-1:
            possible_new_position.append((newJ,pos_col+1))
    return possible_new_position #return a list of 2 to 3 tuples with front move first

def p2_oneMoveGenerator(position, boardsize):
    row, col = boardsize
    pos_row, pos_col = position
    possible_new_position = []
     #go front first
    if pos_row -1 >= 0:
        possible_new_position.append((pos_row-1,pos_col))
        newJ = pos_row-1
        if pos_col-1 >=0:
            possible_new_position.append((newJ,pos_col-1))
        if pos_col+1 <=col-1:
            possible_new_position.append((newJ,pos_col+1))
    return possible_new_position #return a list of 2 to 3 tuples with front move first

def moveGenerator(currentState):
    possibleMoves = []
    if currentState.turn == 1:
        for pawn_position in currentState.p1:            
            physicallyPossible = p1_oneMoveGenerator(pawn_position,currentState.boardSize)
            if physicallyPossible[0] in currentState.p2:
                physicallyPossible.remove(physicallyPossible[0])
            for new_pawn_position in physicallyPossible:
                if new_pawn_position in currentState.p1:
                    physicallyPossible.remove(new_pawn_position)
                else:
                    possibleMoves.append([pawn_position,new_pawn_position])

    elif currentState.turn == 2:
        for pawn_position in currentState.p2:            
            physicallyPossible = p2_oneMoveGenerator(pawn_position,currentState.boardSize)
            if physicallyPossible[0] in currentState.p1:
                physicallyPossible.remove(physicallyPossible[0])
            for new_pawn_position in physicallyPossible:
                if new_pawn_position in currentState.p2:
                    physicallyPossible.remove(new_pawn_position)
                else:
                    possibleMoves.append([pawn_position,new_pawn_position])

    return possibleMoves

def isGameOver(currentState):
    row, col = currentState.boardSize
    if len(currentState.p1) == 0 or len(currentState.p2) ==0:
        if len(currentState.p1) != 0:
            return (True, "p1")
        else:
            return (True, "p2")
    for (x,y) in currentState.p1:
        if x == row-1:
            return (True, "p1")
    for (x,y) in currentState.p2:
        if x == 0:
            return (True, "p2")
    return (False, "")

def evasiveUtility(currentState, player):
    if player == 1:
        remaining = len(currentState.p1)
    elif player == 2:
        remaining = len(currentState.p2)
    else: 
        raise ValueError
    return remaining + random.random()

def conquerorUtility(currentState, player):
    if player == 1:
        opp_remaining = len(currentState.p2)
    elif player ==2:
        opp_remaining = len(currentState.p1)
    return random.random() - opp_remaining

def heightisgoalUtility(currentState, player):
    utility = 0 
    if player == 1:
        utility += len(currentState.p1)*PAWN_COEFFICIENT #remaining
        utility -= len (currentState.p2)*PAWN_COEFFICIENT #opp remaining
        for (row_pos, col_pos) in currentState.p1:
            if row_pos == currentState.boardSize[0]-1:
                utility += FAKE_INFINITY
            utility += row_pos**2*ROW_COEFFICIENT 
            if (row_pos+1, col_pos+1) in currentState.p1:
                utility += SUPPORT_COEFFICIENT
            if (row_pos+1, col_pos-1) in currentState.p1:
                utility += SUPPORT_COEFFICIENT
        for (row_pos, col_pos) in currentState.p2:
            if row_pos == 0:
                utility -= FAKE_INFINITY
            utility -= (currentState.boardSize[0]-1-row_pos)**2*ROW_COEFFICIENT
    elif player ==2:
        utility += len(currentState.p2)*PAWN_COEFFICIENT #remaining
        utility -= len (currentState.p1)*PAWN_COEFFICIENT #opp remaining
        for (row_pos, col_pos) in currentState.p2:
            if row_pos == 0:
                utility += FAKE_INFINITY
            utility +=(currentState.boardSize[0]-1-row_pos)**2*ROW_COEFFICIENT 
            if (row_pos-1, col_pos+1) in currentState.p2:
                utility += SUPPORT_COEFFICIENT
            if (row_pos-1, col_pos-1) in currentState.p2:
                utility += SUPPORT_COEFFICIENT
        for (row_pos, col_pos) in currentState.p1:
            if row_pos == currentState.boardSize[0]-1:
                utility -= FAKE_INFINITY
            utility -= row_pos**2*ROW_COEFFICIENT
    
    return utility + random.random()

def decideBestUtility(currentState, player):
    #decide which heuristic to use depending on the number of pawns left of the player and that of the opponent
    if player == 1:
        if len(currentState.p1) > len(currentState.p2):
            return conquerorUtility(currentState, player)
        else:
            return evasiveUtility(currentState, player)
    else:
        if len(currentState.p2) > len(currentState.p1):
            return conquerorUtility(currentState, player)
        else:
            return evasiveUtility(currentState, player)

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
                else: 
                    node.utility =float('-inf') 
            else: 
                if len(node.children) != 0:
                    node.utility = min([children_node.utility for children_node in node.children])
                else: 
                    node.utility = float('inf')
    # find and return the best move from the children of the root
    for root_child in rootNode.children:
        if rootNode.utility == root_child.utility:
            return root_child.action

def playgame(heuristic_p1, heuristic_p2, board_state,max_depth):
    win, winner = isGameOver(board_state)
    print("board size: " + str(board_state.boardSize))
    print("minimax depth: " + str(max_depth))

    # displayState(board_state)
    move = 0
    while not win:
        if board_state.turn == 1:
            next_move = minimax(board_state, max_depth, heuristic_p1)
        else:
            next_move = minimax(board_state, max_depth, heuristic_p2)
        # print(next_move)
        board_state = transition(board_state, next_move[0], next_move[1])
        # displayState(board_state)
        # print('------------------------')
        win, winner = isGameOver(board_state) 
        move += 1
    print("#p1 left: " + str(len(board_state.p1)))
    print("#p2 left: " + str(len(board_state.p2)))
    print('total moves: '+ str(move))
    displayState(board_state)   
    print(winner +'won')
    print('___________________')






for i in range(5):
    start_state = initialState(8,8,2)
    playgame(heightisgoalUtility,evasiveUtility, start_state,3)
