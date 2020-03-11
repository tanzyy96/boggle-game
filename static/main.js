// Might want to place routes in another file
var testurl = "http://localhost:5000/games/test";
var newgameurl = "http://localhost:5000/games/";


function createGame() {
    const duration = parseInt(document.getElementById("duration").value)
    const checkbox = document.getElementById("random")
    const board = document.getElementById("board").value

    const random = checkbox.checked

    data = {
        "duration": duration,
        "random": random,
        "board": board
    }

    fetch(newgameurl, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data) // body data type must match "Content-Type" header
      })
      .then((resp) => {
          // console.log(resp)
          alert(resp.token)
      });

}

