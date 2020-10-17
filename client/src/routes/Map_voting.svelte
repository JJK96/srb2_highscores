<!--<script src="{{config.static_dir}}/js/map_voting.js"></script>-->
<script>
    import Page from "./Page.svelte";
</script>

<Page>
    <h1>Map voting</h1>
    <h1>List of maps</h1>
    <table border=1>
        <thead>
            <tr>
                <th>Image</th>
                <th>Name</th>
                <th>Votes</th>
                <th></th>
            </tr>
        </thead>
        <!--<tbody>
            {% for map in maps: %}
                <tr>
                    <td> <img src="{{config.static_dir}}/img/{{map['image']}}" width=150 height=100> </td>
                    <td>{{map['name']}}</td>
                    <td>{{map['votes']}}</td>
                    <td>
                        <i class="fa fa-arrow-up clickable" onclick="vote({{map['id']}}, true)"></i>
                        &nbsp;
                        <i class="fa fa-arrow-down clickable" onclick="vote({{map['id']}}, false)"></i>
                    </td>
                </tr>
            {% endfor %}
        </tbody>-->
    </table>
</Page>

<style>
    :global(body) {
        background-image: url("/img/map_voting.jpg");
    }
</style>
