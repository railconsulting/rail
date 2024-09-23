/** @odoo-module **/

import {registry} from "@web/core/registry";
import {Component, useState, onWillStart, onMounted} from "@odoo/owl";
import {loadJS, loadCSS} from "@web/core/assets";


class LeafletMapComponent extends Component {
    setup() {
        this.http = this.env.services.http
        this.state = useState({
            "map": null,
        })
        onWillStart(async () => {
            await loadCSS('https://unpkg.com/leaflet@1.9.4/dist/leaflet.css');
            await loadJS('https://unpkg.com/leaflet@1.9.4/dist/leaflet.js');
        })
        onMounted(async () => {
            this.state.map = this._initMap();
            this.getGeoLocation();
        })
    }

    getGeoLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition((position) => {
                console.log("Latitude: " + position.coords.latitude + "<br>Longitude: " + position.coords.longitude)
                this.showMarker([position.coords.latitude, position.coords.longitude], "<h1>Current Location</h1>")
            });
        }
    }

    _initMap() {
        var map = L.map('map').setView([51.505, -0.09], 13);
        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19, attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);
        return map
    }

    showMarker(location, popup = null) {
        var marker = L.marker(location).addTo(this.state.map);
        if (popup) {
            marker.bindPopup(popup).openPopup();
        }
        marker._icon.color = 'red'; // Change the color here
        return marker;
    }
}

LeafletMapComponent.components = {};
LeafletMapComponent.template = "leaflet_map_simulation.leafletMap";

registry.category("actions").add("leaflet_map_simulation.leafletMap", LeafletMapComponent);
