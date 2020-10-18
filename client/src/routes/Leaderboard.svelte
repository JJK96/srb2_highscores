<script>
    import Page from "../highscores/Page.svelte";
    import api from "../api.js";
    import { convert_form } from "../util.js";

    let players = []
    let form = {}

    var submit_form = function() {
        // get the page endpoint from current pathname to build the api url needed
        let params = convert_form(form)
        api.get_leaderboard(params).then(data => players = data)
    }

    submit_form()
</script>

<Page>
    <h2>Players' leaderboard (following mario kart's scoring system)</h2>
    <form id="best_in_data_form" action="/api" on:change={submit_form}>
        <table>
            <tr>
                <td>
                    <label for="all_skins">All skins counted</label>
                </td>
                <td>
                    <input bind:checked={form.all_skins} type="checkbox" id="all_skins" name="all_skins" onchange="submit_form()" />
                </td>
            </tr>
            <tr>
                <td>
                    <label for="per_skin">One score per user per map</label>
                </td>
                <td>
                    <input bind:checked={form.per_skin} type="checkbox" id="per_skin" name="per_skin" />
                </td>
            </tr>
        </table>
    </form>
    <table border=1>
        <thead>
            <tr>            
                <th>Player</th>
                <th>Points</th>
            </tr>
        </thead>
        <tbody id="best_in_data_table">
            {#each players as player}
                <tr>
                    <td>{player.username}</td>
                    <td>{player.total}</td>
                </tr>
            {/each}
        </tbody>
    </table>
</Page>
