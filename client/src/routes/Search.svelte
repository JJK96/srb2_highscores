<script>
    import Page from "../highscores/Page.svelte";
    import { onDestroy } from "svelte";
    import api from "../api.js";
    import { server_info_update_delay } from "../config.js";
    import { convert_form, update_background } from "../util.js";

    location.search
        .substr(1)
        .split("&")
        .forEach(item => {
            if (item) {
                item = item.split("=");
                document.getElementById(item[0]).value = item[1]
            }
        });

    let highscores = []
    let columns = []
    let skins = []
    let maps = []
    let users = []

    let form = {
        limit: 20,
        order: "time",
    }

    var submit_form = function() {
        api.search(convert_form(form)).then(data => {
            highscores = data
            if (data.length) {
                columns = Object.keys(data[0])
            }
        })
    }


    //Called when map selector is changed
    function map_change() {
        api.get_map(form.map_id)
        .then(data => {
            update_background(data.image)
        })
    }

    function update_map() {
        api.get_server_info().then(data => {
            if (form.map_id != data.map.id) {
                form.map_id = data.map.id
                map_change()
            }
        })
    }

    let synchronization_timer = null

    function update_sync(e) {
        let checkbox = e.target
        if (checkbox.checked) {
            update_map()
            //Refresh the page
            synchronization_timer = window.setInterval(update_map, server_info_update_delay);
        } else {
            window.clearInterval(synchronization_timer)
            synchronization_timer = null
        }
    }

    api.get_skins().then(data => skins = data)
    api.get_maps().then(data => maps = data)
    api.get_users().then(data => users = data)
    submit_form()

    onDestroy(async () => {
        window.clearInterval(synchronization_timer)
    })

</script>

<Page>
    <form id="highscores_form" action="/api" on:submit|preventDefault={submit_form} on:change={submit_form}>
        <table>
            <tr>
                <td>
                    <label for="username">Username</label>
                </td>
                <td>
                    <input bind:value={form.username} id="username" list="users" name="username" type="text" />
                    <datalist id="users">
                        {#each users as user}
                            <option value="{user}">{user}</option>
                        {/each}
                    </datalist>
                </td>
            </tr>
            <tr>
                <td>
                    <label for="map_id">Map</label>
                </td>
                <td>
                    <select bind:value={form.map_id} id="map_id"  name="map_id"  type="select" on:change={map_change}>
                        <option value="" selected>All maps</option>
                        {#each maps as map}
                            <option value={map.id} selected={form.map_id == map.id}>{map.name}</option>
                        {/each}
                    </select>
                </td>
            </tr>
            <tr>
                <td>
                    <label for="skin">Skin</label>
                </td>
                <td>
                    <select bind:value={form.skin} id="skin" name="skin" type="select">
                        <option value="">All skins</option>
                        {#each skins as skin}
                        <option value="{skin}">{skin}</option>
                        {/each}
                    </select>
                </td>
            </tr>
            <tr>
                <td>
                    <label for="order">Order by</label>
                </td>
                <td>
                    <select bind:value={form.order} id="order" name="order" type="select">
                        {#each columns as column}
                            <option value="{column}" selected={column === form.order}>{column}</option>
                        {/each}
                    </select>
                    <select bind:value={form.descending} id="descending" name="descending" type="select">
                        <option value="">Ascending</option>
                        <option value="1">Descending</option>
                    </select>
                </td>
            </tr>
            <tr>
                <td>
                    <label for="all_skins">Get all skins</label>
                </td>
                <td>
                    <input bind:checked={form.all_skins} type="checkbox" id="all_skins" name="all_skins" />
                </td>
            </tr>
            <tr>
                <td>
                    <label for="all_scores">Get all scores</label>
                </td>
                <td>
                    <input bind:checked={form.all_scores} type="checkbox" id="all_scores" name="all_scores" />
                </td>
            </tr>
            <tr>
                <td>
                    <label for="per_skin">One score per user per map</label>
                </td>
                <td>
                    <input bind:checked={form.per_skin} type="checkbox" id="per_skin" name="per_skin"/>
                </td>
            </tr>
            <tr>
                <td>
                    <label for="limit">#Results</label>
                </td>
                <td>
                    <input bind:value={form.limit} id="limit" name="limit" type="number"/>
                </td>
            </tr>
            <tr>
                <td>
                    <label for="sync">Synch with SRB2</label>
                </td>
                <td>
                    <input type="checkbox" id="sync" on:click={update_sync} on:change|stopPropagation="" />
                </td>
            </tr>
            
        </table>
        <button type="submit">Search</button>
    </form>
    <table border=1>
        <thead>
            <tr>
                <th>Username</th>
                <th>Map</th>
                <th>Skin</th>
                <th>Time</th>
                <th>Timestamp</th>
            </tr>
        </thead>
        <tbody id="highscores_table">
            {#each highscores as score}
                <tr>
                    <td>{score.username}</td>
                    <td>{score.mapname}</td>
                    <td>{score.skin}</td>
                    <td>{score.time_string}</td>
                    <td>{score.datetime}</td>
                </tr>
            {/each}
        </tbody>
    </table>
</Page>
