
function get_random (list) {
    return list[Math.floor((Math.random()*list.length))];
  }

async function getGames() {
    const response = await fetch('assets/games.json');
    const json = await response.json();
    return json;
}

function openFile(file) {
    window.open(file, 'blank');
}

function openGame(game) {
    window.open("game.html?game="+game, 'blank');
}

function openPager(page) {
    window.open("index.html?"+page, 'blank');
}

async function gamePager() {
    let games = await getGames()
    let queryString = window.location.search.replace("?", "");
    if (queryString == "") {
        queryString=0
    }

    let pages = Math.ceil((games["games"].length+1) / 4)

    let Pager = document.getElementById("gamePager")
    for (let i = 0; i < pages; i++) {
        let Myli = document.createElement("li")
        Myli.className = "page-item"
        if (i==queryString) {
            Myli.className = "page-item active"
        }

        let Mya = document.createElement("a")
        Mya.className = "page-link"
        Mya.innerText = i+1
        Mya.onclick = function(){openPager(i)};
        Myli.appendChild(Mya)
        
        Pager.appendChild(Myli)
    }
}

async function printGames() {
    let games = await getGames()

    let queryString = window.location.search.replace("?", "");
    if (queryString == "") {
        queryString=0
    }
    
    let mainGameDiv = document.getElementById("mainGameDiv")
    mainGameDiv.className = "flex-direction-game"
    games["games"].forEach((game, ind) => {
        if (ind>=parseInt(queryString)*4 && ind<=parseInt(queryString)*4+3) {
            let gameDiv = document.createElement("div")
            gameDiv.className = "w-game"
            gameDiv.onclick = function(){openGame(ind)};

            let gameName = document.createElement("h1")
            gameName.innerText = game["game_name"]["en"]
            gameDiv.appendChild(gameName)

            let recordName = document.createElement("h2")

            let hiscore = 0
            let player = ""
            game["hall_of_fame"].forEach(record => {
                if (hiscore < record["score"]) {
                    hiscore = record["score"]
                    player = record["username"]
                }
            });

            recordName.innerText = hiscore+" by "+player
            gameDiv.appendChild(recordName)

            mainGameDiv.appendChild(gameDiv)
        }
    });
}

function randomImage() {
    let mainImage = document.getElementById("mainImage")

    let ImageSet = ["assets/images/carl-raw-m3hn2Kn5Bns-unsplash.jpeg", "assets/images/pexels-mikebirdy-114820.jpeg", "assets/images/rivage-By-tZImt0Ms-unsplash.jpeg", "assets/images/pexels-fotios-photos-4511372.jpeg"]

    let choseImage = get_random(ImageSet)

    mainImage.style = "background-image: url('"+choseImage+"'); width: 100%; height:450px; background-size: cover; margin: 8px"
}

async function showGameInfo() {
    let mainDiv = document.getElementById("mainDiv")
    let queryString = window.location.search;
    queryString = queryString.replace("?game=", "")

    let games = await getGames()

    let gameName = document.createElement("h1")
    gameName.innerText = games["games"][queryString]["game_name"]["en"]
    mainDiv.appendChild(gameName)

    let gameMaker = document.createElement("h2")
    gameMaker.innerText = games["games"][queryString]["maker"]
    mainDiv.appendChild(gameMaker)

    let gameGenre = document.createElement("h2")
    gameGenre.innerText = games["games"][queryString]["genre"]
    mainDiv.appendChild(gameGenre)

    let hallOfFame = document.createElement("h1")
    hallOfFame.innerText = "Hall of Fame"
    mainDiv.appendChild(hallOfFame)

    let hallOfFameDiv = document.createElement("div")

    let ScoresList = games["games"][queryString]["hall_of_fame"]

    ScoresList.sort(function (a, b) {
        return a.score - b.score;
    });

    ScoresList.forEach(score => {
        let ScoreDiv = document.createElement("div")
        ScoreDiv.className = "d-flex flex-row justify-content-between"

        let Mytext = document.createElement("h2")
        Mytext.innerText = score["username"]
        ScoreDiv.appendChild(Mytext)
        Mytext = document.createElement("h2")
        Mytext.innerText = score["score"]
        ScoreDiv.appendChild(Mytext)
        Mytext = document.createElement("h2")
        const date = new Date(score["date_time"]);
        const formattedDate = date.toISOString().split('T')[0].replace(/-/g, '.');
        Mytext.innerText = formattedDate
        ScoreDiv.appendChild(Mytext)
        hallOfFameDiv.appendChild(ScoreDiv)
    });

    mainDiv.appendChild(hallOfFameDiv)
}