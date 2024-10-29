import sys
import copy
import ur
import random


class Game:
    def __init__(self, board, player):
        self.board = board
        self.current_player = player
    
    def get_valid_moves(self):
        moves = list()
        for col in range(7):
            if self.board[0][col] =='O': #similar to uniform random check
                moves.append(col)
        return moves

    def make_move(self, column):
        for row in range(5, -1, -1): #start at bottom of board 
            if self.board[row][column] == 'O':
                self.board[row][column] = self.current_player
                if self.current_player == 'Y':
                    self.current_player = 'R'
                else: 
                    self.current_player = 'Y'
                return True
        return False
    
    #checks if a player has won
    def check_win(self):
        #check horizontal
        for row in range(6):
            for col in range(4):
                window = self.board[row][col: col+ 4]
                if window.count('R') == 4:
                    return True, 1
                if window.count('Y') == 4:
                    return True, -1
        
        #check vertical 
        for row in range(3):
            for col in range(7):
                window = [
                    self.board[row][col],
                    self.board[row+1][col],
                    self.board[row+2][col],
                    self.board[row+3][col]
                ]
                if window.count('R') == 4:
                    return True, 1
                if window.count('Y') == 4:
                    return True, -1

        #check diag
        for row in range(3):
            for col in range(4):
                window = [
                    self.board[row][col],
                    self.board[row+1][col+1],
                    self.board[row+2][col+2],
                    self.board[row+3][col+3]
                ]
                if window.count('R') == 4:
                    return True, 1
                if window.count('Y') == 4:
                    return True, -1
        
        for row in range(3,6):
            for col in range(4):
                window = [
                    self.board[row][col],
                    self.board[row-1][col+1],
                    self.board[row-2][col+2],
                    self.board[row-3][col+3] 
                ]
                if window.count('R') == 4:
                    return True, 1
                if window.count('Y') == 4:
                    return True, -1
        
        #check for draw
        if not self.get_valid_moves():
            return True, 0 
        
        return False, None

class Node:
    def __init__ (self, game_state, parent = None, move = None):
        self.game_state = copy.deepcopy(game_state) #copy board
        self.parent = parent
        self.move = move
        self.children = {}
        self.wi = 0 #wins
        self.ni = 0 


def pmcgs(board, player, verbose, simulations):
    root = Node(Game(board, player))
    for _ in range(simulations):
        node = root
        game = copy.deepcopy(root.game_state)

        #traverse until terminal state
        while True:
            if game.check_win()[0]:
                break
            valid_moves = game.get_valid_moves()
            if not valid_moves:
                break 

            #check if all valid nodes tried
            untried_moves = list()
            if len(node.children) < len(valid_moves):
                for move in valid_moves:
                    if move not in node.children:
                        untried_moves.append(move)
                move = random.choice(untried_moves) #get random move for player
                
                if verbose:
                    print(f"wi: {node.wi} \nni: {node.ni} \nMove selected: {move + 1}")
                
                #make new child path
                game.make_move(move)
                new_node = Node(game, node, move)
                node.children[move] = new_node

                if verbose:
                    print("NODE ADDED")
                break
            else: #choose random child 
                move = random.choice(valid_moves)
                if verbose:
                    print(f"Move selected: {move + 1}")
                game.make_move(move)
                if move in node.children:
                    node = node.children[move]
                else: 
                    break
            
        while not game.check_win()[0]:
            valid_moves = game.get_valid_moves()
            if not valid_moves:
                break
            move = random.choice(valid_moves)
            if verbose:
                print(f"Move selected: {move + 1}")
            game.make_move(move)
        
        winning_player = game.check_win()[1]
        if verbose:
            print("TERMINAL NODE VALUE:", winning_player)
        
        #update the wi and ni
        while node is not None:
            node.ni += 1
            if winning_player == 1 and player == 'R':
                node.wi += 1
            elif winning_player == -1 and player == 'Y':
                node.wi += 1
            elif winning_player == 0:
                node.wi += 0.5
            
            if verbose:
                print("Updated values:")
                print("wi:", node.wi, "\nni:", node.ni)
            
            node = node.parent
    
    #select best move
    valid_moves = root.game_state.get_valid_moves()
    if not valid_moves:
        print("No valid moves found")
        return None
    
    best_move = None
    best_value = float('-inf')

    #print final move
    if verbose:
        for col in range(7):
            if col in root.children and col in valid_moves:
                value = root.children[col].wi/ root.children[col].ni
                print(f"Column {col + 1}: {value}")
            else: 
                print(f"Column {col + 1}: Null")
    
    #select highest win rate move
    for move in valid_moves:
        if move in root.children:
            value = root.children[move].wi / root.children[move].ni
            if value > best_value:
                best_value = value
                best_move = move
    if verbose:
        print(f"Final Move selected: {best_move + 1}")
    
    return best_move

        


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

    board, player = ur.get_board_and_move(file)
    pmcgs(board, player, output_mode, num_simulations)
    return

if __name__ == '__main__':
    main()
