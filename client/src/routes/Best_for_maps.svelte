<script>
    import Page from "./Page.svelte";
    import Title from "../highscores/Title.svelte";
</script>

<!--<script src="{{config.static_dir}}/js/best_for_maps.js"></script>-->
<Page>
    <Title />
    <h2>For map and skin</h2>
    <form id="best_for_maps_form">
        <table>
            <tr>
                <td>
                    <label for="all_skins">Get all skins</label>
                </td>
                <td>
                    <input type="checkbox" id="all_skins" name="all_skins" onchange="submit_form()" />
                </td>
            </tr>
        </table>
    </form>
    <div id="highscores">
    </div>
</Page>
