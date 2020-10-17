<script>
    import {links} from "svelte-routing";
    import Page from "./Page.svelte";
    import Title from "../highscores/Title.svelte";

    let location = "/highscores"
</script>

<Page>
    <Title />
    <div id="highscore_hub" class="flex_container" use:links>
        <a href="{location}/search" class="highscore_button">
            <div class="image">
                <i class="fa fa-search fa-10x"></i>
            </div>
            <span>Search</span>
        </a>
        <a href="{location}/bestformaps" class="highscore_button">
            <div class="image">
                <img src="/img/4_maps.png"/>
            </div>
            <span>Records per map</span>
        </a>
        <a href="{location}/bestskins" class="highscore_button">
            <div class="image">
                <img src="/img/sonic_tails.png"/>
            </div>
            <span>Best skins</span>
        </a>
        <a href="{location}/leaderboard" class="highscore_button">
            <div class="image">
                <i class="fa fa-user fa-10x"></i>
            </div>
            <span>Best players</span>
        </a>
    </div>
</Page>

<style>
    :global(body) {
        background-image: url("/img/highscores.jpg");
    }
</style>
