
function getGames() {
    fetch('assets/games.json')
        .then((response) => response.json())
        .then((json) => console.log(json));
}

getGames()