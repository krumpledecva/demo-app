from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import httpx
import json

WMO_CODES = {
    0: "Clear sky ☀️", 1: "Mainly clear 🌤", 2: "Partly cloudy ⛅", 3: "Overcast ☁️",
    45: "Fog 🌫", 48: "Icy fog 🌫",
    51: "Light drizzle 🌦", 53: "Moderate drizzle 🌦", 55: "Dense drizzle 🌧",
    61: "Slight rain 🌧", 63: "Moderate rain 🌧", 65: "Heavy rain 🌧",
    71: "Slight snow 🌨", 73: "Moderate snow 🌨", 75: "Heavy snow ❄️", 77: "Snow grains ❄️",
    80: "Slight showers 🌦", 81: "Moderate showers 🌧", 82: "Violent showers ⛈",
    85: "Slight snow showers 🌨", 86: "Heavy snow showers ❄️",
    95: "Thunderstorm ⛈", 96: "Thunderstorm with hail ⛈", 99: "Thunderstorm with heavy hail ⛈",
}


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        city = query.get("city", [""])[0].strip()

        if not city:
            self._respond(400, {"detail": "City name is required."})
            return

        try:
            with httpx.Client(timeout=10) as c:
                geo = c.get(
                    "https://geocoding-api.open-meteo.com/v1/search",
                    params={"name": city, "count": 1, "language": "en", "format": "json"},
                )
                results = geo.json().get("results")
                if not results:
                    self._respond(404, {"detail": f"City '{city}' not found."})
                    return

                loc = results[0]
                w = c.get(
                    "https://api.open-meteo.com/v1/forecast",
                    params={
                        "latitude": loc["latitude"],
                        "longitude": loc["longitude"],
                        "current": (
                            "temperature_2m,apparent_temperature,"
                            "relative_humidity_2m,weather_code"
                        ),
                        "temperature_unit": "celsius",
                    },
                )
                cur = w.json()["current"]
                temp_c = round(cur["temperature_2m"])
                self._respond(200, {
                    "city": f"{loc['name']}, {loc.get('country', '')}",
                    "lat": loc["latitude"],
                    "lon": loc["longitude"],
                    "temp_c": temp_c,
                    "temp_f": round(temp_c * 9 / 5 + 32),
                    "feels_like_c": round(cur["apparent_temperature"]),
                    "humidity": cur["relative_humidity_2m"],
                    "description": WMO_CODES.get(cur["weather_code"], "Unknown"),
                })
        except Exception:
            self._respond(502, {"detail": "Weather service unavailable."})

    def _respond(self, status, body):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())

    def log_message(self, *args):
        pass  # suppress access logs in Vercel
