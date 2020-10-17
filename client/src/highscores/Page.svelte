<script>
    import { update_background } from "../util.js";
    import Page from "../routes/Page.svelte";

    update_background('highscores.jpg');
</script>

<Page>
    <h1>Leaderboards/highscores</h1>
    <slot></slot>
</Page>
