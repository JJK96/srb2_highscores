<script>
    import Page from "./Page.svelte";

    let srb2_server = "srb2circuit.eu"
</script>
<Page>
    <h1 id="server_name"></h1>
    <h2>IP address/hostname: {srb2_server}</h2>
    <label>Current map</label>: <span id="map_title"></span>
    <div class="server_info_players">
        <h2>Online players</h2>
        <table border=1>
            <thead>
                <tr>
                    <td>Name</td>
                    <td>Skin</td>
                </tr>
            </thead>
            <tbody id="players_table">
            </tbody>
        </table>
        <h2>Mods</h2>
        <ul id="files_list">
        </ul>
    </div>
</Page>

<!--<script src="{{config.static_dir}}/js/server_info.js"></script>-->
<!--<script>
update_info_page()

//Refresh the page
window.setInterval(update_info_page, server_info_update_delay);
</script>-->

<style>
    :global(body) {
        background-image: url("/img/burning_sands.jpg");
    }
    label {
        font-weight: bold
    }
</style>
