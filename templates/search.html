{% extends "highscores.html" %}
{% block content %}
<form id="highscores_form" action="/api">
    <table>
        <tr>
            <td>
                <label for="username">Username</label>
            </td>
            <td>
                <input id="username" list="users" name="username" type="text">
                <datalist id="users">
                    {% for user in users: %}
                    <option value="{{user}}">{{user}}</option>
                    {% endfor %}
                </datalist>
                </input>
            </td>
        </tr>
        <tr>
            <td>
                <label for="map_id">Map</label>
            </td>
            <td>
                <select id="map_id"  name="map_id"  type="select" onchange="map_change(this)">
                    <option value="">All maps</option>
                {% for map in maps: %}
                    <option value="{{map.id}}">{{map.name}}</option>
                {% endfor %}
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
                    {% for skin in skins: %}
                    <option value="{{skin}}">{{skin}}</option>
                    {% endfor %}
                </select>
            </td>
        </tr>
        <tr>
            <td>
                <label for="order">Order by</label>
            </td>
            <td>
                <select id="order" name="order" type="select" onchange="submit_form()">
                    {% for column in columns: %}
                    <option value="{{column}}" {% if column == 'time' %} selected="selected" {% endif %}>{{column}}</option>
                    {% endfor %}
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
                <input type="checkbox" id="all_skins" name="all_skins" onchange="submit_form()"></input>
            </td>
        </tr>
        <tr>
            <td>
                <label for="all_scores">Get all scores</label>
            </td>
            <td>
                <input type="checkbox" id="all_scores" name="all_scores" onchange="submit_form()"></input>
            </td>
        </tr>
        <tr>
            <td>
                <label for="per_skin">One score per user per map</label>
            </td>
            <td>
                <input type="checkbox" id="per_skin" name="per_skin" onchange="submit_form()" value="off"></input>
            </td>
        </tr>
        <tr>
            <td>
                <label for="limit">#Results</label>
            </td>
            <td>
                <input id="limit" name="limit" type="number" value="20"></input>
            </td>
        </tr>
        <tr>
            <td>
                <label for="sync">Synch with SRB2</label>
            </td>
            <td>
                <input type="checkbox" id="sync" onclick="update_sync(this)"></input>
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
{% endblock %}
{% block scripts %}
<script src="{{config.static_dir}}/js/server_info.js"></script>
<script src="{{config.static_dir}}/js/search.js"></script>
{% endblock %}
