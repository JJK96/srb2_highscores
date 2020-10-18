export const convert_form = (form) => {
    let params = {}
    Object.keys(form).forEach(key => {
        let value = form[key]
        if (value) {
            if (key == 'per_skin' && value === true) {
                value = "off"
            } else if (value === true) {
                value = "on"
            }
            params[key] = value
        }
    })
    return params
}

export function update_background(image) {
    if (image && image != "None") {
        document.body.style.backgroundImage = "url('/img/" + image + "')"
    }
}
