function vote(map, up) {
    const formData = new FormData();
    formData.append('map', map);
    formData.append('up', up);
    fetch('/map_voting/vote', {
        method: 'POST',
        body: formData
    }).then((response) => {
        if (response.status != 200) {
            response.text().then((text) => {
                alert(text);
            })
        } else {
            location.reload();
        }
    })
}
