import sys
import math
import random
import copy

WORST_VAL = float('-inf')
BEST_VAL = float('inf')
IS_BETTER = lambda a, b: a > b

class Node:
    def __init__(self, game_state, player, parent=None, move=None):
        self.game_state = copy.deepcopy(game_state)  # Copy of the board state
        self.player = player  # Player to move at this node
        self.parent = parent
        self.move = move
        self.children = {}  # Dictionary to store child nodes by move
        self.wi = 0         # Win count for this node
        self.ni = 0         # Visit count for this node

    def is_leaf_node(self):
        # Check if all possible moves have been expanded
        return len(self.children) == len(get_legal_moves(self.game_state))

    def expand(self, detail):
        if detail:
            print("NODE	ADDED\n")
        for move in get_legal_moves(self.game_state):
            # Expand a new child node for the given move
            new_state = make_move(self.game_state, move, self.player)
            next_player = 'Y' if self.player == 'R' else 'R'
            child_node = Node(new_state, next_player, parent=self, move=move)
            self.children[move] = child_node

    def best_uct_child(self, player, detail=False):
        # Select the child with the highest UCB value
        best_score = WORST_VAL
        best_child = None
        best_move = None
        total_visits = sum(child.ni for child in self.children.values())
        
        if detail:
            print(f"wi: {self.wi}")
            print(f"ni: {self.ni}")
            

        for move, child in self.children.items():
            ucb_value = ((child.wi / child.ni) + 1.41 * math.sqrt(math.log(total_visits) / child.ni)) if child.ni > 0 else BEST_VAL
            if detail:
                print(f"V{move}: {ucb_value}")
                
            if IS_BETTER(ucb_value, best_score):
                best_score = ucb_value
                best_child = child
                best_move = move
                
        if detail:
            print(f"Move selected: {best_move}\n")
        return best_child

def make_move(board, col, player):
    col -= 1
    # Make a move by dropping a piece in the specified column
    new_board = copy.deepcopy(board)
    for row in range(5, -1, -1):
        if new_board[row][col] == 'O':
            new_board[row][col] = player
            break
    return new_board

def uct_algorithm(board, player, num_simulations, detail):
    root = Node(board, player)
    root.expand(False)
    
    for _ in range(num_simulations):
        node = root
        
        # Selection
        while node.children:
            node = node.best_uct_child(player, detail)
        
        # Expansion
        if node and node.ni != 0:
            node.expand(detail)
        
        # Simulation (random rollout)
        result = simulate_random_game(node.game_state, node.player, detail)

        # Backpropagation
        backpropagate(node, result, detail)
    
    best_move = None
    best_val = WORST_VAL
    for move, child in root.children.items():
        val = child.wi / child.ni if child.ni > 0 else WORST_VAL
        if detail:
            print(f"Column{move}: {val}")
        if IS_BETTER(val, best_val):
            best_move = move
            best_val = val
        
    # Select move with the highest win rate
    print("FINAL Move selected:", best_move)

def simulate_random_game(state, player, detail):
    # Plays random moves until reaching a terminal state
    current_state = copy.deepcopy(state)
    current_player = player
    result = 0
    while True:
        moves = get_legal_moves(current_state)
        if not moves:
            result = 0
            break
        move = random.choice(moves)
        if detail:
            print(f"Move selected: {move}")
        current_state = make_move(current_state, move, current_player)
        won, result = check_win(current_state)
        if won:
            break
        current_player = 'Y' if current_player == 'R' else 'R'
        
    if detail:
        # print_board(current_state)
        print(f"TERMINAL NODE VALUE: {result}\n")
    return result

def backpropagate(node, result, detail):
    # Propagate the result up the tree, updating win counts
    while node is not None:
        node.ni += 1
        if result == 1:
            node.wi += 1
        elif result == -1:
            node.wi -= 1
        if detail:
            print("Updated values:")
            print(f"wi: {node.wi}")
            print(f"ni: {node.ni}\n")
        node = node.parent

def get_legal_moves(board): 
    # Checks for open spots on the board
    moves = []
    for col in range(7):
        if board[0][col] == 'O':
            moves.append(col + 1)
    return moves

def check_win(board):
    # Checks if a player has won
    for row in range(6):
        for col in range(4):
            window = board[row][col:col + 4]
            if window.count('R') == 4:
                return True, -1
            if window.count('Y') == 4:
                return True, 1

    for row in range(3):
        for col in range(7):
            window = [board[row + i][col] for i in range(4)]
            if window.count('R') == 4:
                return True, -1
            if window.count('Y') == 4:
                return True, 1

    for row in range(3):
        for col in range(4):
            window = [board[row + i][col + i] for i in range(4)]
            if window.count('R') == 4:
                return True, -1
            if window.count('Y') == 4:
                return True, 1

    for row in range(3):
        for col in range(3, 7):
            window = [board[row + i][col - i] for i in range(4)]
            if window.count('R') == 4:
                return True, -1
            if window.count('Y') == 4:
                return True, 1

    return False, 0

def print_board(board): 
    for row in board:
        for val in row:
            print(val, end=' ')
        print()

def main():
    global IS_BETTER, WORST_VAL, BEST_VAL
    if len(sys.argv) != 4:
        print("Correct Terminal Input: python uct.py file_name.txt output_mode #_of_simulations")
        sys.exit(1)

    file = sys.argv[1]
    output_mode = sys.argv[2]
    num_simulations = int(sys.argv[3])
    detail = False

    if output_mode not in ['None', 'Brief', 'Verbose']:
        print("Error, output mode not in the list of accepted output mode")
        sys.exit(1)
        
    detail = (output_mode == 'Verbose')
    
    # Load board from file
    board, player = load_board_from_file(file)
    if player == 'R':
        WORST_VAL, BEST_VAL = BEST_VAL, WORST_VAL
        IS_BETTER = lambda a, b: a < b        
        
    # print_board(board)

    uct_algorithm(board, player, num_simulations, detail)

def load_board_from_file(file_path):
    # Load board state from the specified file
    with open(file_path, 'r') as file:
        lines = file.readlines()
    player = lines[1].strip()
    board = [list(line.strip()) for line in lines[2:8]]  # Board starts from line 3
    return board, player

if __name__ == "__main__":
    main()
