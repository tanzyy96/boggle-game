import datetime
import string
import random
from helper import create_new_game, check_valid_word, check_board_for_word, generate_board, generate_id, generate_token, get_game, get_time_left, get_word_points

def test():
    return {"result": "testok"}, 200

def start(input):
    """
    /games/
     POST method for creating a game
     Parameters:
      + `duration` (required): the time (in seconds) that specifies the duration of
         the game
      + `random` (required): if `true`, then the game will be generated with random
         board.  Otherwise, it will be generated based on input.
      + `board` (optional): if `random` is not true, this will be used as the board
         for new game. If this is not present, new game will get the default board
         from `test_board.txt`
     Response:
     type: object
         properties:
           id:
             type: integer
           token:
             type: string
           duration:
             type: integer
           board:
             type: string
    """
    duration = input.get("duration")
    random = input.get("random")
    board = input.get("board", None)
    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(seconds=duration)
    id = generate_id()
    token = generate_token()
    if random:
        board = generate_board()
    else:
        board = "T, A, P, *, E, A, K, S, O, B, R, S, S, *, X, D"

    create_new_game(start_time, end_time, duration, board, token, id)
   
    result = {
            'id': id,
            'token': token,
            'duration': duration,
            'board': board
    }

    return result, 201

def submit_word(id, input):
    """
    /games/{id}
     Parameters:
     - name: id
        in: path
     - name: input
        in: body
        type: object
        required:
            - id
            - token
            - word
     Response:
        type: object
        properties:
            id:
                type: integer
            token:
                type: string
            duration:
                type: integer
            board:
                type: string
            time_left:
                type: integer
            points:
                type: integer
    """
    if input.get("id") != id:
        return None, 403
    token = input.get("token")
    word = input.get("word")

    game = get_game(id)
    if (not game) or (game["token"] != token):
        print("Incorrect id or token")
        return "Non-matching game IDs, please check your input.", 406

    time_left = get_time_left(game["end_time"])
    points = game["points"]

    result = {
            "id": id,
            "token": game["token"],
            "duration": game["duration"],
            "board": game["board"],
            "time_left": time_left,
            "points": points
        }

    if time_left == 0:
        return "This game has run out of time.", 406

    # 1. Check word if valid in dict
    if not check_valid_word(word):
        return "The word does not exist in the dictionary.", 406

    # 2. Check word if used
    if word in game["wordsUsed"]:
        return "This word has already been used.", 406

    # 3. Check word if available in board
    if not check_board_for_word(game['board'], word):
        return "Word not found", 406

    # 4. Count points
    points = points + get_word_points(word)

    # 5. Update points
    result["points"] = points
    return result, 200


def show(id):
    """
    /games/{id}
    Parameters:
   + `id` (required): The ID of the game
    Response:
     type: object
     properties:
        id:
           type: integer
        token:
            type: string
        duration:
            type: integer
        board:
            type: string
        time_left:
            type: integer
        points:
            type: integer
    """
    game = get_game(id)
    if not game:
        return None, 403
    result = {
        "id": id,
        "token": game["token"],
        "duration": game["duration"],
        "board": game["board"],
        "time_left": get_time_left(game["end_time"]),
        "points": game["points"]
    }

    return result, 200