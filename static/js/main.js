var api_url = window.location.protocol + "//" + window.location.host + '/highscores/api'

var server_info_update_delay = 10000
var static_dir = "/static"

//Prevent XSS
String.prototype.escape = function() {
    var tagsToReplace = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;'
    };
    return this.replace(/[&<>]/g, function(tag) {
        return tagsToReplace[tag] || tag;
    });
};

function toggle_menu(event) {
    var items = document.getElementById("navbar-items");
    items.classList.toggle("show");
}
