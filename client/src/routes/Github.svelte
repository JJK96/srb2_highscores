<script>
    import Page from "./Page.svelte";
    import { update_background } from "../util.js";

    update_background("Rainbow_Dash_2.jpg");
</script>

<Page>
    <h1>Github</h1>
    <p>All of the code for this project is open-source and available on Github.</p>
    <p>Feel free to make a pull request for any of these projects</p>

    <ul>
        <li><a href="https://github.com/Meziu/SRB2">SRB2 server</a></li>
        <li><a href="https://github.com/jjk96/srb2_highscores">Website</a></li>
        <li><a href="https://github.com/Meziu/srb2_discordbot">Discord bot</a></li>
        <li><a href="https://github.com/Meziu/SRB2/tree/master/src/luascripts">Lua scripts</a></li>
    </ul>
</Page>
