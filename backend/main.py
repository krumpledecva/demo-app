import random
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Demo App API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# WMO weather interpretation codes → human-readable label
WMO_CODES = {
    0:  "Clear sky ☀️",
    1:  "Mainly clear 🌤",
    2:  "Partly cloudy ⛅",
    3:  "Overcast ☁️",
    45: "Fog 🌫",
    48: "Icy fog 🌫",
    51: "Light drizzle 🌦",
    53: "Moderate drizzle 🌦",
    55: "Dense drizzle 🌧",
    61: "Slight rain 🌧",
    63: "Moderate rain 🌧",
    65: "Heavy rain 🌧",
    71: "Slight snow 🌨",
    73: "Moderate snow 🌨",
    75: "Heavy snow ❄️",
    77: "Snow grains ❄️",
    80: "Slight showers 🌦",
    81: "Moderate showers 🌧",
    82: "Violent showers ⛈",
    85: "Slight snow showers 🌨",
    86: "Heavy snow showers ❄️",
    95: "Thunderstorm ⛈",
    96: "Thunderstorm with hail ⛈",
    99: "Thunderstorm with heavy hail ⛈",
}


@app.get("/api/weather")
async def get_weather(city: str):
    city = city.strip()
    if not city:
        raise HTTPException(status_code=400, detail="City name is required.")

    async with httpx.AsyncClient(timeout=10) as client:
        # Step 1 — geocode city name → coordinates
        try:
            geo = await client.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={"name": city, "count": 1, "language": "en", "format": "json"},
            )
            geo.raise_for_status()
        except httpx.RequestError:
            raise HTTPException(status_code=502, detail="Geocoding service unavailable.")

        results = geo.json().get("results")
        if not results:
            raise HTTPException(status_code=404, detail=f"City '{city}' not found.")

        loc = results[0]
        lat, lon = loc["latitude"], loc["longitude"]
        city_label = f"{loc['name']}, {loc.get('country', '')}"

        # Step 2 — fetch current weather from Open-Meteo (no API key needed)
        try:
            w = await client.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "current": (
                        "temperature_2m,apparent_temperature,"
                        "relative_humidity_2m,weather_code"
                    ),
                    "temperature_unit": "celsius",
                },
            )
            w.raise_for_status()
        except httpx.RequestError:
            raise HTTPException(status_code=502, detail="Weather service unavailable.")

    cur = w.json()["current"]
    temp_c = round(cur["temperature_2m"])
    return {
        "city": city_label,
        "lat": lat,
        "lon": lon,
        "temp_c": temp_c,
        "temp_f": round(temp_c * 9 / 5 + 32),
        "feels_like_c": round(cur["apparent_temperature"]),
        "humidity": cur["relative_humidity_2m"],
        "description": WMO_CODES.get(cur["weather_code"], "Unknown conditions"),
    }


@app.get("/api/dice")
async def roll_dice():
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    return {"die1": die1, "die2": die2, "total": die1 + die2}
