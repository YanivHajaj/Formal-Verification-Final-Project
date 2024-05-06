import os
import subprocess
import time
import re


def print_board(board):
    print("\n----sokoban board----")
    for row in board:
        print('\t'.join(row))
    print("---------------------\n")


def createSMVfile(board):
    # Specifying the path
    path = r'C:\Users\yaniv\OneDrive - Bar-Ilan University\Desktop\nuXmv-2.0.0-win64\bin'

    # Specifying the filename
    filename = 'sokoban.smv'

    # Specifying the string to be written to the file
    content = f'''MODULE main
    VAR
        board : array 0..{n - 1} of array 0..{m - 1} of {{WarehouseKeeper, KeeperOnGoal, Box, BoxOnGoal, Wall, Goal, Floor}};
        move : {{l, u, r, d}};

    ASSIGN 
    '''

    # Creating the full file path
    file_path = os.path.join(path, filename)

    # Writing the string to the file
    with open(file_path, 'w') as file:
        file.write(content)

    print(f'File {filename} has been created in {path}')

    # Define a dictionary to map board symbols to states
    symbol_to_state = {
        '@': 'WarehouseKeeper',
        '+': 'KeeperOnGoal',
        '$': 'Box',
        '*': 'BoxOnGoal',
        '#': 'Wall',
        '.': 'Goal',
        '-': 'Floor'
    }

    init = "\t"

    for x, row in enumerate(board):
        for y, cell in enumerate(row):
            # Get the state corresponding to the board symbol
            state = symbol_to_state[cell]

            # Add the initialization string for this state
            init += f"init(board[{x}][{y}]) := {state};\n\t\t"

    init += '''
    '''
    # Append the initialization string to the file
    with open(file_path, 'a') as file:
        file.write(init)

    transitions = '\t'
    movements = {
        'l': (0, -1),
        'r': (0, 1),
        'u': (-1, 0),
        'd': (1, 0)
    }

    for i in range(len(board)):
        for j in range(len(board[0])):

            # the current cell is a wall - can't change
            if board[i][j] == '#':
                transitions += f'next(board[{i}][{j}]) := Wall;\n\t\t'
            else:
                transitions += f'\n\t\tnext(board[{i}][{j}]) := \n\t\tcase\n'

                for currentMove, (dx, dy) in movements.items():
                    # the current cell is the WarehouseKeeper or KeeperOnGoal and the next cell is wall
                    transitions += (
                        f'\t\t\t(board[{i}][{j}] = WarehouseKeeper | board[{i}][{j}] = KeeperOnGoal) & move = {currentMove} & board[{i + dx}][{j + dy}] = Wall: board[{i}][{j}];\n')
                    # the current cell is WarehouseKeeper and the next cell is floor or goal
                    transitions += (
                        f'\t\t\tboard[{i}][{j}] = WarehouseKeeper & move = {currentMove} & (board[{i + dx}][{j + dy}] = Floor | board[{i + dx}][{j + dy}] = Goal) : Floor;\n')
                    # the current cell is KeeperOnGoal and the next cell is floor or goal
                    transitions += (
                        f'\t\t\tboard[{i}][{j}] = KeeperOnGoal & move = {currentMove} & (board[{i + dx}][{j + dy}] = Floor | board[{i + dx}][{j + dy}] = Goal) : Goal;\n')
                    # the current cell is Goal and the WarehouseKeeper or KeeperOnGoal go this cell
                    transitions += (
                        f'\t\t\tboard[{i}][{j}] = Goal & move = {currentMove} & (board[{i - dx}][{j - dy}] = WarehouseKeeper | board[{i - dx}][{j - dy}] = KeeperOnGoal)  : KeeperOnGoal;\n')
                    # the current cell is Floor and the WarehouseKeeper or KeeperOnGoa go this cell
                    transitions += (
                        f'\t\t\tboard[{i}][{j}] = Floor & move = {currentMove} & (board[{i - dx}][{j - dy}] = WarehouseKeeper | board[{i - dx}][{j - dy}] = KeeperOnGoal) : WarehouseKeeper;\n')

                    if 0 <= i + 2 * dx < len(board) and 0 <= j + 2 * dy < len(board[0]):
                        # the current cell is the WarehouseKeeper or KeeperOnGoal, the next cell is box or boxOnGoal and the next cell is wall, box or boxOnGoal
                        transitions += (
                            f'\t\t\t(board[{i}][{j}] = WarehouseKeeper | board[{i}][{j}] = KeeperOnGoal) & move = {currentMove} & (board[{i + dx}][{j + dy}] = Box | board[{i + dx}][{j + dy}] = BoxOnGoal) & (board[{i + 2 * dx}][{j + 2 * dy}] = Box | board[{i + 2 * dx}][{j + 2 * dy}] = Wall | board[{i + 2 * dx}][{j + 2 * dy}] = BoxOnGoal) : board[{i}][{j}];\n')
                        # the current cell is the WarehouseKeeper, the next cell is box or boxOnGoal and the next cell is Floor or Goal
                        transitions += (
                            f'\t\t\tboard[{i}][{j}] = WarehouseKeeper & move = {currentMove} & (board[{i + dx}][{j + dy}] = Box | board[{i + dx}][{j + dy}] = BoxOnGoal) & (board[{i + 2 * dx}][{j + 2 * dy}] = Floor | board[{i + 2 * dx}][{j + 2 * dy}] = Goal) : Floor;\n')
                        # the current cell is the KeeperOnGoal, the next cell is box or boxOnGoal and the next cell is Floor or Goal
                        transitions += (
                            f'\t\t\tboard[{i}][{j}] = KeeperOnGoal & move = {currentMove} & (board[{i + dx}][{j + dy}] = Box | board[{i + dx}][{j + dy}] = BoxOnGoal) & (board[{i + 2 * dx}][{j + 2 * dy}] = Floor | board[{i + 2 * dx}][{j + 2 * dy}] = Goal) : Goal;\n')

                    # the previous cell is the WarehouseKeeper or KeeperOnGoal, the current cell is box or boxOnGoal and the next cell is wall, box or boxOnGoal
                    transitions += (
                        f'\t\t\t(board[{i}][{j}] = Box | board[{i}][{j}] = BoxOnGoal) & move = {currentMove} & (board[{i + dx}][{j + dy}] = Box | board[{i + dx}][{j + dy}] = BoxOnGoal | board[{i + dx}][{j + dy}] = Wall) & (board[{i - dx}][{j - dy}] = WarehouseKeeper | board[{i - dx}][{j - dy}] = KeeperOnGoal) : board[{i}][{j}];\n')
                    # the current cell is box, the next cell is floor or goal, and the previous cell is WarehouseKeeper or KeeperOnGoal
                    transitions += (
                        f'\t\t\tboard[{i}][{j}] = Box & move = {currentMove} & (board[{i + dx}][{j + dy}] = Floor | board[{i + dx}][{j + dy}] = Goal) & (board[{i - dx}][{j - dy}] = WarehouseKeeper | board[{i - dx}][{j - dy}] = KeeperOnGoal) : WarehouseKeeper;\n')
                    # the current cell is box on goal, the next cell is floor or goal, and the previous cell is WarehouseKeeper or KeeperOnGoal
                    transitions += (
                        f'\t\t\tboard[{i}][{j}] = BoxOnGoal & move = {currentMove} & (board[{i + dx}][{j + dy}] = Floor | board[{i + dx}][{j + dy}] = Goal) & (board[{i - dx}][{j - dy}] = WarehouseKeeper | board[{i - dx}][{j - dy}] = KeeperOnGoal) : KeeperOnGoal;\n')

                    if 0 <= i - 2 * dx < len(board) and 0 <= j - 2 * dy < len(board[0]):
                        # the current cell is floor, the previous cell is box or boxOnGoal, and the previous cell is keeper
                        transitions += (
                            f'\t\t\tboard[{i}][{j}] = Floor & move = {currentMove} & (board[{i - dx}][{j - dy}] = Box | board[{i - dx}][{j - dy}] = BoxOnGoal) & (board[{i - 2 * dx}][{j - 2 * dy}] = WarehouseKeeper | board[{i - 2 * dx}][{j - 2 * dy}] = KeeperOnGoal) : Box;\n')
                        # the current cell is goal, the previous cell is box or boxOnGoal, and the previous cell is keeper
                        transitions += (
                            f'\t\t\tboard[{i}][{j}] = Goal & move = {currentMove} & (board[{i - dx}][{j - dy}] = Box | board[{i - dx}][{j - dy}] = BoxOnGoal) & (board[{i - 2 * dx}][{j - 2 * dy}] = WarehouseKeeper | board[{i - 2 * dx}][{j - 2 * dy}] = KeeperOnGoal) : BoxOnGoal;\n')

                transitions += f'\t\t\tTRUE: board[{i}][{j}];\n'
                transitions += "\t\tesac;\n\t\t"

    # Append the initialization string to the file
    with open(file_path, 'a') as file:
        file.write(transitions)

    # Define a set of goal symbols
    goal_symbols = {'+', '.', '*'}

    # Initialize an empty list to store the locations of the goals
    goals = []

    for x, row in enumerate(board):
        for y, cell in enumerate(row):
            # If the cell is a goal, add its location to the list
            if cell in goal_symbols:
                goals.append((x, y))

    # Initialize an empty string to store the goal conditions
    goal_conditions = '''
    DEFINE
        winning_state := ('''
    goal_conditions1 = '''winning_state := ('''
    # Iterate over the list of goals
    for goal in goals:
        # Add the condition for this goal to the string
        goal_conditions += f"(board[{goal[0]}][{goal[1]}] = BoxOnGoal) & "
        goal_conditions1 += f"(board[{goal[0]}][{goal[1]}] = BoxOnGoal) & "

    # Remove the trailing ' & ' from the string
    goal_conditions = goal_conditions.rstrip(' & ')
    goal_conditions1 = goal_conditions1.rstrip(' & ')
    print(f"\nthe temporal logic formula used is: {goal_conditions1}\n")
    goal_conditions += ''');

    LTLSPEC !(F(winning_state));
    '''

    # Append the initialization string to the file
    with open(file_path, 'a') as file:
        file.write(goal_conditions)


def run_nuxmv(model_filename, engine=None, k=None):
    timer1 = time.time()
    # Run the command
    os.chdir(r'C:\Users\yaniv\OneDrive - Bar-Ilan University\Desktop\nuXmv-2.0.0-win64\bin')
    # Define the base command
    base_command = [".\\nuXmv.exe"]

    # Check the engine type
    if engine in ["SAT", "BDD"]:
        base_command.extend(["-int", model_filename])
        # Start the nuXmv process
        nuxmv_process = subprocess.Popen(base_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                         universal_newlines=True)

        # Send commands based on the engine type
        if engine == "SAT":
            nuxmv_process.stdin.write("go_bmc\n")
            nuxmv_process.stdin.write(f"check_ltlspec_bmc -k {k}\n")
            output_filename = model_filename.split(".")[0] + "SAT.out"
        elif engine == "BDD":
            nuxmv_process.stdin.write("go\n")
            nuxmv_process.stdin.write("check_ltlspec\n")
            output_filename = model_filename.split(".")[0] + "BDD.out"

        # Quit the nuXmv process
        nuxmv_process.stdin.write("quit\n")
    else:
        # Run the command with the model filename
        nuxmv_process = subprocess.Popen(base_command + [model_filename], stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE, universal_newlines=True)
        output_filename = model_filename.split(".")[0] + ".out"

    stdout, _ = nuxmv_process.communicate()

    # Save output to file
    with open(output_filename, "w") as f:
        f.write(stdout)
    print(f"Output saved to {output_filename}")
    timer2 = time.time()
    if engine is not None:
        print(f"Performance of the {engine} run: {timer2 - timer1} seconds")
    else:
        print(f"Performance of the regular run: {timer2 - timer1} seconds")
    return [output_filename, timer2 - timer1]


def print_solution(filename, mode):
    moves = []
    solvable = 0
    move = None
    with open(filename, 'r') as file:

        for line in file:
            if "is false" in line:
                solvable = 1
                break

        if solvable == 1:
            for line in file:
                if "winning_state = TRUE" in line:
                    break
                if "move = " in line:
                    move = line.split("move = ")[1].strip()
                if "State" in line and move is not None:
                    moves.append(move)

            print(f"\nthe solution of this board for the {mode} run is: {moves}")
        else:
            print(f"there is no solution for the {mode} run")
    return moves


def iterative_solving(board):
    state_to_symbol = {
        'WarehouseKeeper': '@',
        'KeeperOnGoal': '+',
        'Box': '$',
        'BoxOnGoal': '*',
        'Wall': '#',
        'Goal': '.',
        'Floor': '-'
    }
    # Define a set of goal symbols
    goal_symbols = {'+', '.', '*'}
    # Initialize an empty list to store the locations of the goals
    goals = []
    solution = []
    totaltime = 0
    for x, row in enumerate(board):
        for y, cell in enumerate(row):
            # If the cell is a goal, add its location to the list
            if cell in goal_symbols:
                goals.append((x, y))

    # remove goals from the board
    for goal in goals:
        if board[goal[0]][goal[1]] == '+':
            board[goal[0]][goal[1]] = '@'
        elif board[goal[0]][goal[1]] == '.':
            board[goal[0]][goal[1]] = '-'
        elif board[goal[0]][goal[1]] == '*':
            board[goal[0]][goal[1]] = '$'
    index = 1
    for goal in goals:
        print(f"iteration number {index} ")
        index = index + 1
        # add one goal
        if board[goal[0]][goal[1]] == '@':
            board[goal[0]][goal[1]] = '+'
        elif board[goal[0]][goal[1]] == '-':
            board[goal[0]][goal[1]] = '.'
        elif board[goal[0]][goal[1]] == '$':
            board[goal[0]][goal[1]] = '*'
        print_board(board)
        createSMVfile(board)
        outputfile, itertime = run_nuxmv("sokoban.smv", "SAT", 20)
        totaltime = totaltime + itertime
        currentmoves = print_solution(outputfile, "SAT")
        solution.append(currentmoves)
        # update the board
        with open(outputfile, 'r') as file:
            lines = file.readlines()

        # Iterate over each line in the file
        for line in lines:
            # Use regex to find lines that describe the board state
            match = re.search(r'board\[(\d+)\]\[(\d+)\] = (\w+)', line)
            if match:
                # If a match is found, update the board at the specified position
                i, j, state = match.groups()
                symbol = state_to_symbol.get(state, '')  # Get the symbol corresponding to the state
                board[int(i)][int(j)] = symbol

    print(
        f"\n\nthe final solution is: {solution} \ntotal number of iterations is {index - 1} \ntotal time for a given board is {totaltime}")


if __name__ == "__main__":
    # Initialize an empty list to hold the lines of the file
    board = []

    # Define the path to your file
    path = r'C:\Users\yaniv\OneDrive - Bar-Ilan University\Desktop\formal verification\board.txt'

    # Define the set of valid characters
    valid_chars = {'#', '@', '$', '.', '+', '*', '-'}

    # Open the file in read mode ('r')
    with open(path, 'r') as f:
        # Iterate over each line in the file
        for line in f:
            # Strip the newline character from the end of the line and convert the line to a list of characters
            line = list(line.strip('\n'))
            # Filter the list of characters to only include valid characters
            line = [char for char in line if char in valid_chars]
            # Add the list of characters to the board list
            board.append(line)

        # Now board is a 2D array where each element is a list of characters from one line of the file
        print_board(board)
    # Define n and m as the number of rows and columns of the board
    n = len(board)
    m = len(board[0]) if board else 0

    createSMVfile(board)

    # run non interactive mode
    run_nuxmv("sokoban.smv")
    print_solution("sokoban.out", "regular")
    print("\n\n")
    # run BDD mode
    run_nuxmv("sokoban.smv", "BDD")
    print_solution("sokobanBDD.out", "BDD")
    print("\n\n")
    # run SAT mode
    k = input("please enter number of steps for SAT run")
    run_nuxmv("sokoban.smv", "SAT", k)
    print_solution("sokobanSAT.out", "SAT")
    print("\n\n")

    print("***************************** Iteration Mode ******************************")
    iterative_solving(board)
