import sys
import simulation


def main():
    if len(sys.argv) != 3:
        print("Correct Terminal Input: python ur.py file_name.txt output_mode #_of_simulations")
        sys.exit(1)
    algorithm = sys.argv[1]
    simulations = int(sys.argv[2])
    win = simulation.play_game((algorithm, simulations), ("human", None))
    if win == 1:
        print("Computer wins")
    else:
        print("You won!")


if __name__ == "__main__":
    main()