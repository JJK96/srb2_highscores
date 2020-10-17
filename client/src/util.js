export const add_params = (url, form) => {
    Object.keys(form).forEach(key => {
        let value = form[key]
        if (value) {
            if (value === true) {
                value = "on"
            }
            url.searchParams.append(key, value)
        }
    })
    return url
}

export function update_background(image) {
    if (image && image != "None") {
        document.body.style.backgroundImage = "url('/img/" + image + "')"
    }
}

