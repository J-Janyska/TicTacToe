import os
import random
import platform
from rules import TICTACTOE_RULES


def init_game() -> None:
    """
    1. Print the rules
    2. Wait for player's confirmation
    3. Launch the game with a random starting player "X" or "O"
    """
    clear_screen()
    print(TICTACTOE_RULES)
    if enumerated_input("\n[S]tart or [Q]uit ?:") == "Q":
        exit()
    starting_player = random.choice("XO")
    tic_tac_toe(starting_player)


def tic_tac_toe(player: str) -> None:
    """
    Game rounds - main loop
    1. Init the grid cells (list) with 9 spaces
    2. Start the game round, {player} begins the round
    3. Increment a stats item according to a result - winner or tie
    4. Print stats and ask if play again
    5. Swap starting player for the next round
    """
    win_stats = {"player X": 0, "player O": 0, "tie": 0}
    play_again = "A"

    while play_again == "A":
        grid = [" "] * 9
        win_stats[game_round(grid, player)] += 1
        print_stats(win_stats)
        play_again = enumerated_input("\nPlay [A]gain or [Q]uit ?:")
        player = "O" if player == "X" else "X"
    else:
        print("Goodbye!")


def game_round(grid: list, player: str) -> str:
    """
    Game round - loop until we have a winner or tie
    1. Get a valid move number from {player}
    2. Fill the grid cell with a {player} mark - "X" or "O"
    3. Print the grid and test if we have a winner
    4. Swap the player for the next turn
    return: "player X" or "player O" or "tie"
    """
    winner = False
    print_grid(grid)

    while not winner and grid.count(" "):
        print(f"It's player {player}'s turn.")
        move_number = get_valid_move_number(grid)
        grid[move_number] = player
        print_grid(grid)
        winner = victory_test(grid, move_number, player)
        player = "O" if player == "X" else "X"

    if winner:
        print("  Player", winner, "wins !")
        return "player " + winner
    else:
        print("This round ended in a tie.")
        return "tie"


def print_grid(grid: list) -> None:
    clear_screen()
    line = "\n+---+---+---+\n"
    grid_content = ["", ""]
    for i in range(0, 3):
        grid_content.insert(
            i + 1,
            " | ".join([''] + grid[i*3: i*3 + 3] + ['']).strip()
        )
    print(line.join(grid_content))


def victory_test(grid: list, last_move_index: int, player: str) -> str or False:
    """
    Test occurrence of ['X', 'X', 'X'] or ['O', 'O', 'O']
    in triplets derived from the last_move_index.
    Return 'X' or 'O' if we have a winner, False otherwise.
    """
    if [player] * 3 in get_affected_triplets(grid, last_move_index):
        return player
    return False


def get_affected_triplets(grid: list, index: int) -> list:
    """
    1. Break the last move index into the grid cell's row & column
    2. Collect & return list of triplets containing the cell
       Example:
         012        index = 2 => row = 0, column = 2
         345        Vert. & horiz.triplet in grid[2::3] & grid[0:3],
         678        one diag.triplet in grid[2:7:2]
    """
    row, column = divmod(index, 3)
    # vertical & horizontal triplet
    triplets = [grid[column::3], grid[row * 3:row*3 + 3]]
    # diagonal triplets
    if index in (0, 4, 8):
        triplets.append(grid[0::4])
    if index in (2, 4, 6):
        triplets.append(grid[2:7:2])
    return triplets


def get_valid_move_number(grid: list) -> int:
    """
    Get a valid move number from a player, which
    1. must be an integer value 1-9 and
    2. the corresponding cell in the grid is free.
    """
    while True:
        free_cells = [i + 1 for i, cell in enumerate(grid) if cell == " "]
        print("Valid moves:", free_cells, "\n")
        inp = input("Your move? :")
        if inp.isnumeric() and (inp := int(inp) - 1) in range(9):
            if grid[inp] == " ":
                return inp
            else:
                print("This cell is not free!")
        else:
            print("You must enter a number btw 1 a 9!")


def enumerated_input(prompt: str) -> str:
    """
    Wait for user input enumerated in square brackets in {prompt}
    Example:
        prompt = "[Y]es or [N]o ?"
        => inputs_allowed = ['Y', 'N']
    """
    inputs_allowed = [
        substr[substr.find("[") + 1:substr.find("]")]
        for substr in prompt.split()
        if "[" in substr and "]" in substr
    ]
    while (inp := input(prompt)) not in inputs_allowed:
        continue
    return inp


def print_stats(stats: dict) -> None:
    line = "+-----------------+"
    print(line, "|  Wins and ties  |", line, sep="\n")
    for stat in stats:
        print(f"| {stat:<8} | {stats[stat]:<5}|")
    print(line)


def clear_screen() -> None:
    if platform.system() in ("Linux", "MacOs"):
        os.system("clear")
    elif platform.system() == "Windows":
        os.system("cls")


if __name__ == "__main__":
    init_game()
