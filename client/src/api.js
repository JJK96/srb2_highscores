import {api_url} from './config.js';

let assets = ["srb2.pk3", "zones.pk3", "player.dta", "patch.pk3"]

function handle_response(response) {
    return response.json()
}

function add_params(url, params) {
    Object.keys(params).forEach(key => {
        url.searchParams.append(key, params[key])
    })
    return url
}

function get_url(path, params=null) {
    let url = new URL(api_url + path)
    if (params) {
        add_params(url, params)
    }
    return fetch(url).then(handle_response)
}

function get_maps(params=null) {
    return get_url('/maps', params)
}

function get_server_info() {
    return get_url("/server_info").then(data => {
        data.filesneeded = data.filesneeded.filter(file => !assets.includes(file.name))
        return data
    })
}

function search(params) {
    return get_url('/search', params)
}

function get_map(id) {
    return get_url('/maps/' + id)
}

function get_skins() {
    return get_url('/skins')
}

function get_users() {
    return get_url('/users')
}

function get_leaderboard(params) {
    return get_url("/leaderboard", params)
}


function get_bestformaps(params) {
    return get_url('/bestformaps', params)
}
function get_bestskins(params) {
    return get_url("/bestskins", params)
}

export default {
    get_maps,
    get_server_info,
    search,
    get_map,
    get_skins,
    get_users,
    get_leaderboard,
    get_bestformaps,
    get_bestskins,
    get_url,
}
