import sys
import copy

class Node:
    def _init_ (self, game_state, parent = None, move = None):
        self.game_state = copy.deepcopy(game_state) #copy board
        self.parent = parent
        self.move = move
        self.children = {}
        self.wi = 0
        self.ni = 0
    
    def root():
        self.parent = None


def uct():
    return 

def pmcgs(board, player):
    root = Node(board, None, player)
    curr = root
    for move in range(0,6):
        t,wins = check_win(board)
        node = Node(board, curr, wins, move)
        
        return

def get_moves(board): 
    #checks for open spots on the board
    #reusing code from the Uniform Random 
    moves = []
    for col in range(7):
        if board[0][col] == 'O':
            moves.append(col + 1)
    if len(moves) == 0:
        return None
    return moves



#checks if a player has won
def check_win(board):
    #check vertical 
    for row in range(6):
        for col in range(4):
            window = board[row][col: col+ 4]
            if window.count('R') == 4:
                return True, 1
            if window.count('Y') == 4:
                return True, -1
    
    #check vertical 
    for row in range(3):
        for col in range(6):
           window = board[row: row + 4][col]
           if window.count('R') == 4:
               return True, 1
           if window.count('Y') == 4:
               return True, -1

    #check diag
    for row in range(3):
        for col in range(4):
            window = board[row: row + 4][col: col + 4]
            if window.count('R') == 4:
               return True, 1
            if window.count('Y') == 4:
               return True, -1
    
    for row in range(3):
        for col in range(6, 2, -1):
            window = board[row: row + 4][col: col - 4]
            if window.count('R') == 4:
               return True, 1
            if window.count('Y') == 4:
               return True, -1
    



def main():
    if len(sys.argv) !=4:
        print("Correct Terminal Input: python ur.py file_name.txt output_mode #_of_simulations")
        sys.exit(1)
    file = sys.argv[1]
    output_mode = sys.argv[2]
    num_simulations = int(sys.argv[3])

    if output_mode not in ['None', 'Brief', 'Verbose']:
        print("Error, output mode not in the list of accepted output mode")
        sys.exit(1)
    return

if __name__ == 'main':
    main()
