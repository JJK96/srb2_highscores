import {api_url} from './config.js';

export function get_maps(callback) {
    var url = new URL(api_url + '/maps')
    return fetch(url)
        .then(response => {
            return response.json()
        })
}
