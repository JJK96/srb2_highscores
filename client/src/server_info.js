import { api_url } from "./config.js";
import api from "./api.js";

let assets = ["srb2.pk3", "zones.pk3", "player.dta", "patch.pk3"]

export function get_server_info() {
    return api.get_server_info().then(data => {
        data.filesneeded = data.filesneeded.filter(file => !assets.includes(file.name))
        return data
    })
}
