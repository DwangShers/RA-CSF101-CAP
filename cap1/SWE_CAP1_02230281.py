####################################################################
# Dechen Wangdra Sherpa
# SWE
# 02230281
####################################################################
# REFERENCES
# https://chat.openai.com/
# https://stackoverflow.com/questions/50115873/how-do-i-create-a-scoring-system-in-python
# https://github.com/laurentg/pyscoring
####################################################################
# SOLUTION
# Solution Score: 
# 51188
####################################################################


# Define the scoring system
shapes = {'A': 1, 'B': 2, 'C': 3}
outcomes = {'X': 0, 'Y': 3, 'Z': 6}

def read_input(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            rounds = [(line.split()[0], line.split()[1]) for line in lines]
        return rounds
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def calculate_total_score(rounds):
    total_score = 0
    for round in rounds:
        opponent_move, outcome = round
        if opponent_move == 'A' and outcome == 'Y':
            player_move = 'A'
        elif opponent_move == 'B' and outcome == 'X':
            player_move = 'A'
        elif opponent_move == 'C' and outcome == 'Z':
            player_move = 'A'
        elif opponent_move == 'A' and outcome == 'X':
            player_move = 'C'
        elif opponent_move == 'B' and outcome == 'Y':
            player_move = 'B'
        elif opponent_move == 'C' and outcome == 'X':
            player_move = 'B'
        else:
            player_move = 'C'
        total_score += shapes[player_move] + outcomes[outcome]
    return total_score

# Specify the file path
file_path = 'input_1_cap1.txt' 

# Try to read data from the file
rounds = read_input(file_path)
if rounds is not None:
    # Print the calculated total score
    print(calculate_total_score(rounds))

