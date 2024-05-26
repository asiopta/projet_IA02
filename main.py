from dodo import *
from gopher import *


def main():
    grid: Environment = state_to_environnement(empty_state(4))
    for cell in grid:
        print(cell)


if __name__ == "__main__":
    main()
