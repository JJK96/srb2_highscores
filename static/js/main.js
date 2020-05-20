var api_url = window.location.protocol + "//" + window.location.host + '/api'

var form = document.getElementById("highscores_form");
form.addEventListener("submit", function (event) {
    event.preventDefault()
    submit_form()
})

location.search
    .substr(1)
    .split("&")
    .forEach(item => {
        if (item) {
            item = item.split("=");
            document.getElementById(item[0]).value = item[1]
        }
    });

var submit_form = function() {
    var url = new URL(api_url + '/search')
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

submit_form()
