import random 
import sys
def uniform_random(board, last):
    if last != 0:
        return None

    legal_moves = []
    for col in range(7):
        if board[0][col] == 'O':
            legal_moves.append(col + 1)


    index = random.randint(0,len(legal_moves))

    if len(legal_moves) == 0:
        return None

    return legal_moves[index]


def get_board_and_move(file):
    board = []
    with open(file, 'r') as f:
        last= str(f.readline().strip)
        i = 0
        while i < 6:
            row = list(f.readline().strip)
            board.append(row)
            i+=1
    return board, last
        

def main(): 
    if len(sys.argv) != 4:
        print("Correct Terminal Input: python ur.py file_name.txt output_mode #_of_simulations")
        sys.exit(1)
    file = sys.argv[1]
    output_mode = sys.argv[2]
    num_simulations = int(sys.argv[3])

    if output_mode not in ['None', 'Brief', 'Verbose']:
        print("Error, output mode not in the list of accepted output mode")
        sys.exit(1)
    board, last = get_board_and_move(file)

    move = uniform_random(board, last)

    print(f"FINAL Move selected: {move}")


if __name__ == '__main__':
    main()