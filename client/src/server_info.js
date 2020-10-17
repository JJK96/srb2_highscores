import { api_url } from "./config.js";

let assets = ["srb2.pk3", "zones.pk3", "player.dta", "patch.pk3"]

export function get_server_info(callback) {
    fetch(api_url + "/server_info")
        .then(response => {
            return response.json()
        }).then(data => {
            data.filesneeded = data.filesneeded.filter(file => !assets.includes(file.name))
            callback(data)
        })
}
