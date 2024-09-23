import json

from odoo import http


class WebsocketController(http.Controller):
    @http.route('/api/leaflet_map/send-location', type="json", auth="public", cors="*", csrf=False)
    def api_leaflet_map_send_location(self, **kwargs):
        channel = "leaflet_map"
        event = "leaflet_map/update-location"
        http.request.env['bus.bus']._sendone(channel, event, json.dumps(kwargs))
