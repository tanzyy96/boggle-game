import random, string, datetime
from collections import defaultdict
from flask import jsonify

local_id = 0

GAMES = { }


def create_new_game(start_time, end_time, duration, board, token, id):
    global GAMES
    if GAMES.get(id):
        return False
    new_game = {
        "start_time": start_time,
        "end_time": end_time,
        "duration": duration,
        "board": board,
        "token": token,
        "wordsUsed": [],
        "points": 0
    }
    GAMES[id] = new_game
    print("Creating new game of id:{}\n{}".format(id, GAMES[id]))
    return True

def get_game(id):
    global GAMES
    return GAMES.get(id)


def generate_id():
    global local_id
    local_id = local_id + 1
    return local_id

def generate_board():
    """ Generate random 4x4 board with minimum of 2 * in the format eg. A, C, E, D, L, U, G, *, E, *, H, T, G, A, F, K"""
    board = ""
    letters = string.ascii_uppercase[:28]
    star_1 = random.randrange(0,15)
    star_2 = random.randrange(0,15)
    for i in range(16):
        if (i == star_1) or (i == star_2):
            board = board + "*"
        else:
            letter = random.choice(letters)
            board = board + letter
        if i != 15:    
            board = board + ", "
    print(board)
    return board

def generate_token(length=20):
    """ Generate game token """
    lettersAndDigits = string.ascii_lowercase + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(length))

def get_time_left(end_time):
    """ Return time left in seconds. If time's up, return 0 """
    now = datetime.datetime.now()
    timeleft = int((end_time-now).total_seconds())
    if timeleft < 0:
        return 0
    else:
        return timeleft

def check_valid_word(word):
    """ Check if word exists in dictionary """
    with open("dictionary.txt","r") as f:
        lines = f.readlines()
        for line in lines:
            if word.lower() == line.strip():
                return True
        return False 

def searchFor(matrix, letter):
    for row in matrix:
        for element in row:
            if element == letter:
                return row, element
    return None

def check_board_for_word(boardString, word):
    """ Check if word lies on board e.g. T, A, P, *, E, A, K, S, O, B, R, S, S, *, X, D
    T A P *
    E A K S
    O B R S
    S * X D
    """
    # Fit board into a 2D array
    boardArray = boardString.split(", ")
    b = [[],[],[],[]]
    k = 0
    for i in range(4):
        for j in range(4):
            b[i].append(boardArray[k])
            k = k + 1
       
    print(b)

    word = word.upper()

    starts = get_possible_start_spot(b, word[0])

    for start_spot in starts:
        if get_surrounding_letters(b, word, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]] , start_spot):
            print("THE WORD EXISTS.")
            return True
        else:
            print("FAILED.")
    
    return False

def get_possible_start_spot(matrix, letter):
    options = []
    # find the possible start letters
    for row in range(4):
        for col in range(4):
            if matrix[row][col] == letter or matrix[row][col] == '*':
                # if not visited[row][col]:
                    location = [row, col]
                    options.append(location)
    return options



def get_surrounding_letters(matrix, word, visited, location):
    if len(word) == 1:
        return True
    letter = word[0]
    next_letter = word[1]
    print("Visiting '{}' at {}".format(letter, location))
    visited[location[0]][location[1]] = 1

    print(visited)
    # if completed the word

    # find their surrounding letters
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            if x == 0 and y == 0:
                continue
            new_x = location[0] + x
            new_y = location[1] + y
            if (0 <= new_x <= 3) and (0 <= new_y <= 3):
                # valid surrounding letter
                # if that's the next letter we're looking for
                if matrix[new_x][new_y] == next_letter or matrix[new_x][new_y] == '*':
                    if not visited[new_x][new_y]:
                        visited[new_x][new_y] = 1
                        if get_surrounding_letters(matrix, word[1:], visited, [new_x, new_y]):
                            return True


def get_word_points(word):
    """ Get points for word. This assumes all words in dictionary are 3 or more letters."""
    if 3 <= len(word) <= 4:
        return 1
    elif len(word) == 5:
        return 2
    elif len(word) == 6:
        return 3
    elif len(word) == 7:
        return 5
    else:
        return 11

# Helper function to return a response with status code and CORS headers
def prepare_response(res_object, status_code):
    response = jsonify(res_object)
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST')
    return response, status_code

    