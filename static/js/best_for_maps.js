var form = document.getElementById("best_for_maps_form");

var submit_form = function() {
    var url = new URL(api_url + '/bestformaps')
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
            var highscores = document.getElementById("highscores")
            highscores.innerHTML = ''
            for (const map of data) {
                var div = document.createElement("div")
                var header = document.createElement("h3")
                header.textContent = map['name']
                var table = document.createElement("table")
                var thead = document.createElement("thead")
                var tr = document.createElement("tr")
                for (const column of ['Skin', 'Time', 'Username', 'Timestamp'] ) {
                    var td = document.createElement("td")
                    td.textContent = column
                    tr.appendChild(td)
                }
                thead.appendChild(tr)
                var tbody = document.createElement("tbody")
                for (const skin of map['skins']) {
                    var tr = document.createElement('tr')
                    for (const column of ['name', 'time_string', 'username', 'datetime'] ) {
                        var td = document.createElement("td")
                        td.textContent = skin[column]
                        tr.appendChild(td)
                    }
                    tbody.appendChild(tr)
                }
                table.appendChild(thead)
                table.appendChild(tbody)
                div.appendChild(header)
                div.appendChild(table)
                highscores.appendChild(div)
            }
        })
}

submit_form()
