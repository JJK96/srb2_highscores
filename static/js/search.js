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
                for (const column of ['username', 'mapname', 'skin', 'time_string', 'datetime']) {
                    var td = document.createElement("td")
                    td.textContent = row[column]
                    score.appendChild(td)
                }
                highscores.appendChild(score)
            }
        })
}

submit_form()

var synchornisation_timer = null

function update_map() {
    get_server_info(data => {
        var map_select = document.getElementById('map_id')
        var new_value = data.map.num-1
        if (map_select.value != new_value) {
            map_select.value = new_value
            submit_form()
        }
    })
}

function update_sync(checkbox) {
    if (checkbox.checked) {
        update_map()
        //Refresh the page
        synchornisation_timer = window.setInterval(update_map, server_info_update_delay);
    } else {
        window.clearInterval(synchornisation_timer)
        synchornisation_timer = null
    }
}

