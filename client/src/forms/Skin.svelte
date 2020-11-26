<script>
    import api from "../api.js";

    export let value
    export let name = "skin"

    let skins = []

    api.get_skins().then(data => skins = data)
</script>

<select
    type="select"
    bind:value
    on:change
    on:blur
    id={name}
    {name}
>
    <option value="">All skins</option>
    {#each skins as skin}
    <option value="{skin}">{skin}</option>
    {/each}
</select>
