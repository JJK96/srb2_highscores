<script>
    import Page from "./Page.svelte";
    import Title from "../highscores/Title.svelte";
</script>

<!--<script src="{{config.static_dir}}/js/best_skins.js"></script>
<script src="{{config.static_dir}}/js/best_in_data.js"></script>-->

<Page>
    <Title />
    <h2>Skins ordered by number of best timed tracks</h2>
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
        </table>
    </form>
    <table border=1>
        <thead>
            <tr>            
                <th>Skin</th>
                <th>Best Times</th>
            </tr>
        </thead>
        <tbody id="best_in_data_table">
        </tbody>
    </table>
</Page>
