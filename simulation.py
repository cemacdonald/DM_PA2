import copy
import pandas as pd
import ur, uct, pmcgs


def play_game(algorithm_1, algorithm_2):
    board = [['O' for _ in range(7)] for _ in range(6)]
    current_board = copy.deepcopy(board)
    curr_player = 'R'

    while True:
        if curr_player == "R":
            move = player_move(current_board, curr_player, algorithm_1[0], algorithm_1[1])
        else:
            move = player_move(current_board, curr_player, algorithm_2[0], algorithm_2[1])
        if move is None: #draw
            return 0
        #place move on board
        for row in range(5,-1,-1):
            if board[row][move - 1] == 'O': #have to minus 1 to account for +1 before
                board[row][move - 1] = curr_player
                break
        
        if algorithm_2[0] == "human":
            print(f"{curr_player} placed in column {move}")
            print_board(board) 
        
        win = uct.check_win(board)
        if win[0]:
            return win[1] 
        curr_player = 'Y' if curr_player == 'R' else 'R'

def print_board(board):
    print("Current board:")
    for row in board: print(row)
    print()

def player_move(board, curr_player, algorithm, simulations = None):
    if algorithm == "UR":
        return ur.uniform_random(board, curr_player)
    elif "PMCGS" in algorithm:
        return pmcgs.pmcgs(board, curr_player, None, simulations)
    elif algorithm == "human":
        while True:
            try:
                move = int(input("Select a column for your move. (1 - 7)\n"))
                if move < 1 or move > 7:
                    print("Input should be a valid column number. Try again")
                elif board[0][move - 1] != 'O': #check if able to place token there
                    print("Do not pick a full column. Try again")
                else:
                    return move
            except:
                print("input should be a number")
    else:
        return uct.uct_algorithm(board, curr_player, simulations, None)

def run_tournament(algorithms):

    results= {
        "UR": list(),
        "PMCGS500": list(),
        "PMGCS10K": list(),
        "UCT500": list(),
        "UCT10K": list()
    }

    for algo1 in algorithms:
        print("new algo 1")
        print(algo1)
        for algo2 in algorithms:
            print(algo2)
            if algo1 == algo2:
                results[algo1[0]].append('-')
                continue
            wins = 0
            for _ in range(100):
                winner = play_game(algo1, algo2)
                if winner == 1:
                    wins +=1
            results[algo1[0]].append(wins / 100) 
    return results

def main():
    algorithms = [
        ("UR", None),
        ("PMCGS500", 500),
        ("PMCGS10K", 10000),
        ("UCT500", 500),
        ("UCT10K", 10000)
    ]

    results = run_tournament(algorithms)
    df = pd.DataFrame(results, index = ['UR', 'PMCGS500', 'PMCGS10K', 'UCT500', 'UCT10K'])
    print(df)

if __name__ == "__main__":
    main()