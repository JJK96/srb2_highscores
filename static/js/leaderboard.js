var form = document.getElementById("best_in_data_form");
form.addEventListener("submit", function (event) {
    event.preventDefault()
    submit_form()
})

var submit_form = function() {
    // get the page endpoint from current pathname to build the api url needed
    const best_in_data_api_url = api_url + document.location.pathname.split("highscores")[1]
    console.log(best_in_data_api_url)
    var url = new URL(best_in_data_api_url)
    for (const pair of new FormData(form)) {
        if (pair[1] != "") {
            url.searchParams.append(pair[0],pair[1])
        }
    }
    fetch(url)
        .then(response => {
            return response.json()
        })
        .then(data => {
            var scoring = document.getElementById("best_in_data_table")
            scoring.innerHTML = ''
            for (const player of data) {
                console.log(player)
                var score = document.createElement("tr")
                var tag = document.createElement("td")
                tag.textContent = player.username
                score.appendChild(tag)
                var points = document.createElement("td")
                points.textContent = player.total
                score.appendChild(points)
            scoring.appendChild(score)
            }
        })
}

submit_form()
