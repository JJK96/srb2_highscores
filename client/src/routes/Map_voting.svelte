<script>
    import Page from "./Page.svelte";
    import api from "../api.js";
    import { update_background } from "../util.js";

    let maps = []

    function get_maps() {
        let params = {
            "order": "votes",
            "descending": true
        }
        api.get_maps(params).then(data => maps = data)
    }

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
                get_maps()
            }
        })
    }

    get_maps()

    update_background("map_voting.jpg");
</script>

<Page>
    <h1>Map voting</h1>
    <h1>List of maps</h1>
    <table border=1>
        <thead>
            <tr>
                <th>Image</th>
                <th>Name</th>
                <th>Votes</th>
                <th></th>
            </tr>
        </thead>
        <tbody>
            {#each maps as map}
                <tr>
                    <td> <img alt={map.name} src="/img/{map.image}" width=150 height=100> </td>
                    <td>{map.name}</td>
                    <td>{map.votes}</td>
                    <td>
                        <a href="#" on:click={() => vote(map.id, true)}><i class="fa fa-arrow-up" ></i></a>
                        &nbsp;
                        <a href="#" on:click={() => vote(map.id, false)}><i class="fa fa-arrow-down" ></i></a>
                    </td>
                </tr>
            {/each}
        </tbody>
    </table>
</Page>
