<script>
    import Page from "./Page.svelte";
    import { api_url, server_info_update_delay } from "../config.js";
    import { get_server_info, update_background } from "../server_info.js";

    let data;
    let server_ip = "srb2circuit.eu";

    function update_info_page() {
        get_server_info(d => {
            data = d
            update_background(data.map.image)
        })
    }

    update_info_page()
    //Refresh the page
    window.setInterval(update_info_page, server_info_update_delay);
</script>

<Page>
    {#if data}
        <h1 id="server_name">{data.servername}</h1>
        <h2>IP address/hostname: {server_ip}</h2>
        <label>Current map</label>: <span id="map_title">{data.map.name}</span>
        <div class="server_info_players">
            <h2>Online players</h2>
            <table border=1>
                <thead>
                    <tr>
                        <td>Name</td>
                        <td>Skin</td>
                    </tr>
                </thead>
                <tbody>
                    {#each data.players as player}
                    <tr>
                        <td>{player.name}</td>
                        <td>{player.skin}</td>
                    </tr>
                    {/each}
                </tbody>
            </table>
            <h2>Mods</h2>
            <ul id="files_list">
                {#each data.filesneeded as file}
                    <li>{file.name}</li>
                {/each}
            </ul>
        </div>
    {:else}
        Loading...
    {/if}
</Page>

<style>
    :global(body) {
        background-image: url("/img/burning_sands.jpg");
    }
    label {
        font-weight: bold
    }
</style>
