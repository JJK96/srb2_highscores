var form = document.getElementById("highscores_form");
form.addEventListener("submit", function (event) {
    event.preventDefault()
    submit()
})

var submit = function() {
    var url = new URL(form.action)
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
            var highscores = document.getElementById("highscores_table")
            highscores.innerHTML = ''
            for (const row of data) {
                var score = document.createElement("tr")
                for (const column of ['username', 'mapname', 'skin', 'time_string']) {
                    var td = document.createElement("td")
                    td.textContent = row[column]
                    score.appendChild(td)
                }
                highscores.appendChild(score)
            }
        })
}

submit()
