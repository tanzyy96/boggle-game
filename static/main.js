// Might want to place routes in another file
const url = "http://localhost:5000/games/"
var testurl = url + "test";
var newgameurl = url;
var getgameurl = url;
const size = 50

createGrid(size, "T, A, P, *, E, A, K, S, O, B, R, S, S, *, X, D");
createPoints()

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
    }).then((resp) => {
        return resp.json()
    }).then((data) => {
        console.log("ID:", data.id)
        console.log("TOKEN:", data.token)
        console.log("BOARD:", data.board)

        var respID = document.getElementById("resp_id")
        var respToken = document.getElementById("resp_token")
        respID.innerHTML = data.id
        respToken.innerHTML = data.token
        reloadGrid(data.board)
        document.getElementById("id").value = data.id
        document.getElementById("token").value = data.token
    });

}

function reloadGrid(board) {
    var array = board.split(", ")
    var j = 0

    var grid = document.getElementById('grid')
    var children = grid.childNodes // returns nodelist
    for (let i = 0; i < children.length; i++) {
        let item = children[i]
        item.innerHTML = array[j++]
    }
}

function createGrid(size, board) {
    // var ratioW = Math.floor((window.innerWidth || document.documentElement.offsetWidth) / size),
    //     ratioH = Math.floor((window.innerHeight || document.documentElement.offsetHeight) / size);
    var ratioW = 4,
        ratioH = 4;

    var parent = document.createElement('div');
    parent.id = 'grid';
    parent.className = 'grid';
    parent.style.width = (ratioW * size) + 'px';
    parent.style.height = (ratioH * size) + 'px';

    var array = board.split(", ");
    var j = 0;

    for (var i = 0; i < ratioH; i++) {
        for (var p = 0; p < ratioW; p++) {
            var cell = document.createElement('div');
            cell.innerHTML = array[j++];
            cell.style.height = (size - 1) + 'px';
            cell.style.width = (size - 1) + 'px';
            parent.appendChild(cell);
        }
    }

    document.body.appendChild(parent);
}

function createPoints() {
    var points = document.createElement('div');
    points.id = "points";
    points.className = "points";
    points.innerHTML = "POINTS:"

    var pointsOutput = document.createElement('output');
    pointsOutput.id = "pointsOutput";
    pointsOutput.className = "pointsOutput";
    pointsOutput.value = 0;

    document.body.appendChild(points);
    points.appendChild(pointsOutput);
}

function getGame() {
    var id = document.getElementById("id").value

    getgameurl = url + id

    fetch(getgameurl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then((resp) => {
        return resp.json().then((data => ({status: resp.json, body: data})))
    }).then((obj) => {
        console.log(obj.body)

        if (obj.status >= 400) {
            alert(obj.body)
        } else {
            successMessage(obj.body)
            reloadGrid(obj.body.board)
            loadPoints(obj.body.points)
        }
    });

}

function submitWord() {
    var word = document.getElementById("word").value
    var token = document.getElementById("token").value
    var id = parseInt(document.getElementById("id").value)

    console.log(typeof id)

    getgameurl = url + id

    data = {
        "id": id,
        "token": token,
        "word": word
    }

    fetch(getgameurl, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then((resp) => {
        return resp.json().then((data => ({status: resp.status, body: data})))
    }).then((obj) => {
        console.log(obj.body)

        if (obj.status >= 400) {
            alert(obj.body)
        } else {
            successMessage(obj.body)
            loadPoints(obj.body.points)
        }
    })
}

function loadPoints(points) {
    document.getElementById("pointsOutput").value = points
}

function successMessage(resp) {
    var points = resp.points
    alert(`Correct word! You got ${points} point(s)!`)
}
