
def pmcgs(board, player):
    for move in range(0,6):
        return

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
        