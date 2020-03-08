# Boggle Game API

A Boggle game built on Flask API using Connexion.

## How to start?
Activate virtualvenv using
```
source venv/bin/activate
```

Then start the server using
```
python main.py
```

Currently, only the backend API exists so the game can only be played using [Postman](https://www.postman.com/).

## How to play?
The API endpoints will be following:

### Create the game
```
POST /games
```

- Parameters:
  + `duration` (required): the time (in seconds) that specifies the duration of
    the game
  + `random` (required): if `true`, then the game will be generated with random
    board.  Otherwise, it will be generated based on input.
  + `board` (optional): if `random` is not true, this will be used as the board
    for new game. If this is not present, new game will get the default board
    from `test_board.txt`

- Response:
  + Success (status 201 Created)

```json
{
  "id": 1,
  "token": "9dda26ec7e476fb337cb158e7d31ac6c",
  "duration": 12345,
  "board": "A, C, E, D, L, U, G, *, E, *, H, T, G, A, F, K"
}
```

### Play the game

```
PUT /games/:id
```

- Parameters:
  + `id` (required): The ID of the game
  + `token` (required): The token for authenticating the game
  + `word` (required): The word that can be used to play the game

- Response:
  + Success (status 200 OK)

```json
{
  "id": 1,
  "token": "9dda26ec7e476fb337cb158e7d31ac6c",
  "duration": 12345,
  "board": "A, C, E, D, L, U, G, *, E, *, H, T, G, A, F, K",
  "time_left": 10000,
  "points": 10
}
```

### Show the game

```
GET /games/:id
```

- Parameters:
  + `id` (required): The ID of the game

- Response:
  + Success (status 200 OK)

```json
{
  "id": 1,
  "token": "9dda26ec7e476fb337cb158e7d31ac6c",
  "duration": 12345,
  "board": "A, C, E, D, L, U, G, *, E, *, H, T, G, A, F, K",
  "time_left": 10000,
  "points": 10
}
```
