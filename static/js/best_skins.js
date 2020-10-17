function handle_data(data) {
    var scoring = document.getElementById("best_in_data_table")
    scoring.innerHTML = ''
    for (const key in data) {
        var score = document.createElement("tr")
        var tag = document.createElement("td")
        tag.textContent = key
        score.appendChild(tag)
        var points = document.createElement("td")
        points.textContent = data[key]
        score.appendChild(points)
    scoring.appendChild(score)
    }
}
