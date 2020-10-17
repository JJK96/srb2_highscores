<script>
    import Page from "./Page.svelte";
    import Title from "../highscores/Title.svelte";
    import { api_url } from "../config.js";

    let form = {}
    let maps = []

    var submit_form = function() {
        var url = new URL(api_url + '/bestformaps')
        Object.keys(form).forEach(key => {
            let value = form[key]
            if (value) {
                if (value === true) {
                    value = "on"
                }
                url.searchParams.append(key, value)
            }
        })
        fetch(url)
            .then(response => {
                return response.json()
            })
            .then(data => maps = data)
    }

    submit_form()
</script>

<Page>
    <Title />
    <h2>For map and skin</h2>
    <form id="best_for_maps_form" on:change={submit_form}>
        <table>
            <tr>
                <td>
                    <label for="all_skins">Get all skins</label>
                </td>
                <td>
                    <input bind:checked={form.all_skins} type="checkbox" id="all_skins" name="all_skins" />
                </td>
            </tr>
        </table>
    </form>
    <div id="highscores">
        {#each maps as map}
            <div>
                <h3>{map.name}</h3>
                <table>
                    <thead>
                        <tr>
                            <td>Skin</td>
                            <td>Time</td>
                            <td>Username</td>
                            <td>Timestamp</td>
                        </tr>
                    </thead>
                    <tbody>
                        {#each map.skins as skin}
                            <tr>
                                <td>{skin.name}</td>
                                <td>{skin.time_string}</td>
                                <td>{skin.username}</td>
                                <td>{skin.datetime}</td>
                            </tr>
                        {/each}
                    </tbody>
            </div>
        {/each}
    </div>
</Page>
