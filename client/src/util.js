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

export function toISODate(date) {
    let month = '' + (date.getMonth() + 1)
    let day = '' + date.getDate()
    let year = date.getFullYear()

    if (month.length < 2) 
        month = '0' + month
    if (day.length < 2) 
        day = '0' + day

    return [year, month, day].join('-')
}

export function update_background(image) {
    if (image && image != "None") {
        document.body.style.backgroundImage = "url('/img/" + image + "')"
    }
}
