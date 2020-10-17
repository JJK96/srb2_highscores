<script>
    import Page from "./Page.svelte";
    import Title from "../highscores/Title.svelte";
</script>

<!--<script src="{{config.static_dir}}/js/leaderboard.js"></script>
<script src="{{config.static_dir}}/js/best_in_data.js"></script>-->

<Page>
    <Title />
    <h2>Players' leaderboard (following mario kart's scoring system)</h2>
    <form id="best_in_data_form" action="/api">
        <table>
            <tr>
                <td>
                    <label for="all_skins">All skins counted</label>
                </td>
                <td>
                    <input type="checkbox" id="all_skins" name="all_skins" onchange="submit_form()" />
                </td>
            </tr>
            <tr>
                <td>
                    <label for="per_skin">One score per user per map</label>
                </td>
                <td>
                    <input type="checkbox" id="per_skin" name="per_skin" onchange="submit_form()" value="off" />
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
        </tbody>
    </table>
</Page>
