<script>
    import { Router, links, Link, Route } from "svelte-routing";
    import Error from "./routes/Error.svelte";
    import Index from "./routes/Index.svelte";
    import ServerInfo from "./routes/Server_info.svelte";
    import Highscores from "./routes/Highscores.svelte";
    import MapVoting from "./routes/Map_voting.svelte";
    import Github from "./routes/Github.svelte";

    let api_url = window.location.protocol + "//" + window.location.host + '/highscores/api'

    let server_info_update_delay = 10000

    function toggle_menu(event) {
        let items = document.getElementById("navbar-items");
        items.classList.toggle("show");
    }

    export let url = "";
</script>

<div class="navbar">
    <div id="imzaq" class="navbar-container">
        <a href="/" id="i2aq8" class="navbar-brand"></a>
        <div id="iylmi" class="navbar-burger" onclick="toggle_menu()">
            <div class="navbar-burger-line"></div>
            <div class="navbar-burger-line"></div>
            <div class="navbar-burger-line"></div>
        </div>
        <div id="navbar-items" class="navbar-items-c">
            <nav data-gjs="navbar-menu" class="navbar-menu" use:links>
                <a href="/" id="i7s3x" class="navbar-menu-link">Home</a>
                <a href="/server_info" class="navbar-menu-link">Server info</a>
                <a href="/highscores" id="i64ju" class="navbar-menu-link">Highscores</a>
                <a href="/map_voting" id="ihy3g" class="navbar-menu-link">Map voting</a>
                <a href="https://discord.gg/wNwg9vk" id="i1g6j" class="navbar-menu-link" native><i class="fab fa-discord"></i> Discord</a>
                <a href="/highscores/api" class="navbar-menu-link" native>API</a>
                <a href="/github" class="navbar-menu-link"><i class="fab fa-github"></i> Github</a>
            </nav>
        </div>
    </div>
</div>
<Router url="{url}">
    <Route path="/"><Index /></Route>
    <Route path="/server_info"><ServerInfo /></Route>
    <Route path="/highscores"><Highscores /></Route>
    <Route path="/map_voting"><MapVoting /></Route>
    <Route path="/github"><Github /></Route>
    <Route path=""><Error /></Route>
</Router>
