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

    return legal_moves[index]

def main(): 


    return     


if __name__ == '__main__':
    main()