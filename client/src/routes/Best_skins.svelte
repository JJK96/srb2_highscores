<script>
    import Page from "../highscores/Page.svelte";
    import { api_url } from "../config.js";
    import { add_params } from "../util.js";

    let skins = {}
    let form = {}

    var submit_form = function() {
        // get the page endpoint from current pathname to build the api url needed
        const best_in_data_api_url = api_url + "/bestskins"
        var url = new URL(best_in_data_api_url)
        fetch(add_params(url, form))
            .then(response => {
                return response.json()
            })
            .then(data => skins = data)
    }

    submit_form()
</script>

<Page>
    <h2>Skins ordered by number of best timed tracks</h2>
    <form id="best_in_data_form" action="/api" on:change={submit_form}>
        <table>
            <tr>
                <td>
                    <label for="all_skins">All skins counted</label>
                </td>
                <td>
                    <input bind:checked={form.all_skins} type="checkbox" id="all_skins" name="all_skins" />
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
            {#each Object.keys(skins) as skin}
                <tr>
                    <td>{skin}</td>
                    <td>{skins[skin]}</td>
                </tr>
            {/each}
        </tbody>
    </table>
</Page>
