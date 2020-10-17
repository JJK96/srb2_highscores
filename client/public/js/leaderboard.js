function handle_data(data) {
    var scoring = document.getElementById("best_in_data_table")
    scoring.innerHTML = ''
    for (const player of data) {
        var score = document.createElement("tr")
        var tag = document.createElement("td")
        tag.textContent = player.username
        score.appendChild(tag)
        var points = document.createElement("td")
        points.textContent = player.total
        score.appendChild(points)
    scoring.appendChild(score)
    }
}
