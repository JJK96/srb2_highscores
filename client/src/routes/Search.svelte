<script>
    import Page from "./Page.svelte";
    import Title from "../highscores/Title.svelte";

    let columns = []
    let skins = []
    let maps = []
    let user = ""
    let users = []
</script>
<!--<script src="/js/server_info.js"></script>
<script src="/js/search.js"></script>-->

<Page>
    <Title />
    <form id="highscores_form" action="/api">
        <table>
            <tr>
                <td>
                    <label for="username">Username</label>
                </td>
                <td>
                    <input id="username" list="users" name="username" type="text" />
                    <datalist id="users">
                        {#each users as users}
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
                    <select id="map_id"  name="map_id"  type="select" onchange="map_change(this)">
                        <option value="">All maps</option>
                    {#each maps as map}
                        <option value="{map.id}">{map.name}</option>
                    {/each}
                    </select>
                </td>
            </tr>
            <tr>
                <td>
                    <label for="skin">Skin</label>
                </td>
                <td>
                    <select id="skin" name="skin" type="select" onchange="submit_form()">
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
                    <select id="order" name="order" type="select" onchange="submit_form()">
                        {#each columns as column}
                            <!--<option value="{column}" {#if column == 'time'} selected="selected" {/if}>{column}</option>-->
                        {/each}
                    </select>
                    <select id="descending" name="descending" type="select" onchange="submit_form()">
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
                    <input type="checkbox" id="all_skins" name="all_skins" onchange="submit_form()" />
                </td>
            </tr>
            <tr>
                <td>
                    <label for="all_scores">Get all scores</label>
                </td>
                <td>
                    <input type="checkbox" id="all_scores" name="all_scores" onchange="submit_form()" />
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
            <tr>
                <td>
                    <label for="limit">#Results</label>
                </td>
                <td>
                    <input id="limit" name="limit" type="number" value="20" />
                </td>
            </tr>
            <tr>
                <td>
                    <label for="sync">Synch with SRB2</label>
                </td>
                <td>
                    <input type="checkbox" id="sync" onclick="update_sync(this)" />
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
        </tbody>
    </table>
</Page>
