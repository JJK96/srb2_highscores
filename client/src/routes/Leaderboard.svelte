<script>
    import Page from "../highscores/Page.svelte";
    import api from "../api.js";
    import Skin from "../forms/Skin.svelte";
    import { convert_form, toISODate } from "../util.js";

    let players = []
    let form = {}

    var submit_form = function() {
        // get the page endpoint from current pathname to build the api url needed
        let params = convert_form(form)
        api.get_leaderboard(params).then(data => players = data)
    }

    var get_current_month = function() {
        var d = new Date()
        var year = d.getFullYear()
        var month = d.getMonth()

        var first_day = new Date(year, month, 1)
        var last_day  = new Date(year, month+1, 0)

        form.start_date = toISODate(first_day)
        form.end_date   = toISODate(last_day)
        submit_form()
    }

    submit_form()
</script>

<Page>
    <h2>Players' leaderboard (following mario kart's scoring system)</h2>
    <form id="best_in_data_form" action="/api" on:change={submit_form}>
        <table>
            <tr>
                <td>
                    <label for="all_skins">Include modded skins</label>
                </td>
                <td>
                    <input bind:checked={form.all_skins} type="checkbox" id="all_skins" name="all_skins"/>
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
                    <label for="skin">Skin</label>
                </td>
                <td>
                    <Skin bind:value={form.skin}/>
                </td>
            </tr>
            <tr>
                <td>
                    <label for="start_date">Start Date</label>
                </td>
                <td>
                    <input bind:value={form.start_date} type="date" id="start_date" name="start_date"/>
                </td>
            </tr>
            <tr>
                <td>
                    <label for="end_date">End Date</label>
                </td>
                <td>
                    <input bind:value={form.end_date} type="date" id="end_date" name="end_date"/>
                </td>
            </tr>
        </table>
    </form>
    <label for="current_month">Scores for current month</label>
    <input type="button" id="current_month" name="current_month" value="Set date" on:click={get_current_month}/>
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
