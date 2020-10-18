import {api_url} from './config.js';

function add_params(url, params) {
    Object.keys(params).forEach(key => {
        url.searchParams.append(key, params[key])
    })
    return url
}

function get_maps() {
    let url = new URL(api_url + '/maps')
    return fetch(url).then(response => {
            return response.json()
        })
}

function get_server_info() {
    return fetch(api_url + "/server_info").then(response => {
        return response.json()
    })
}

function search(params) {
    let url = new URL(api_url + '/search')
    url = add_params(url, params)
    return fetch(url).then(response => {
        return response.json()
    })
}

function get_map(id) {
    return fetch(api_url + '/maps/' + id).then(response => {
        return response.json()
    })
}

function get_skins() {
    return fetch(api_url + '/skins').then(response => {
        return response.json()
    })
}

function get_users() {
    return fetch(api_url + '/users').then(response => {
        return response.json()
    })
}

function get_leaderboard(params) {
    let url = new URL(api_url + "/leaderboard")
    add_params(url, params)
    return fetch(url).then(response => {
        return response.json()
    })
}


function get_bestformaps(params) {
    let url = new URL(api_url + '/bestformaps')
    add_params(url, params)
    return fetch(url).then(response => {
        return response.json()
    })
}
function get_bestskins(params) {
    let url = new URL(api_url + "/bestskins")
    add_params(url, params)
    return fetch(url).then(response => {
        return response.json()
    })
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
}
