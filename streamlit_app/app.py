import random
import time
import httpx
import streamlit as st

st.set_page_config(page_title="Demo App", page_icon="🎲", layout="centered")
st.title("Demo App")

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

# ── Weather ────────────────────────────────────────────────────────────────────
st.header("🌤 Weather")
city = st.text_input("Enter a city name", placeholder="e.g. Ljubljana")

if st.button("Get temperature"):
    if not city.strip():
        st.warning("Please enter a city name.")
    else:
        with st.spinner("Fetching weather…"):
            try:
                with httpx.Client(timeout=10) as client:
                    geo = client.get(
                        "https://geocoding-api.open-meteo.com/v1/search",
                        params={"name": city.strip(), "count": 1,
                                "language": "en", "format": "json"},
                    )
                    geo.raise_for_status()
                    results = geo.json().get("results")
                    if not results:
                        st.error(f"City '{city}' not found.")
                    else:
                        loc = results[0]
                        lat, lon = loc["latitude"], loc["longitude"]
                        city_label = f"{loc['name']}, {loc.get('country', '')}"

                        w = client.get(
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
                        cur = w.json()["current"]
                        temp_c = round(cur["temperature_2m"])
                        temp_f = round(temp_c * 9 / 5 + 32)
                        desc = WMO_CODES.get(cur["weather_code"], "Unknown")

                        st.success(
                            f"**{city_label}**  \n"
                            f"🌡 {temp_c}°C / {temp_f}°F  \n"
                            f"Feels like {round(cur['apparent_temperature'])}°C  \n"
                            f"💧 Humidity {cur['relative_humidity_2m']}%  \n"
                            f"{desc}"
                        )
            except httpx.RequestError:
                st.error("Weather service unavailable. Try again later.")

st.divider()

# ── Dice ───────────────────────────────────────────────────────────────────────
FACES = ["", "⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]

st.header("🎲 Dice Roller")

if "die1" not in st.session_state:
    st.session_state.die1 = None
    st.session_state.die2 = None

col1, col2 = st.columns(2)
with col1:
    face1 = FACES[st.session_state.die1] if st.session_state.die1 else "⬜"
    st.markdown(f"<div style='font-size:4rem;text-align:center'>{face1}</div>",
                unsafe_allow_html=True)
with col2:
    face2 = FACES[st.session_state.die2] if st.session_state.die2 else "⬜"
    st.markdown(f"<div style='font-size:4rem;text-align:center'>{face2}</div>",
                unsafe_allow_html=True)

label = "🔄 Roll Again" if st.session_state.die1 else "🎲 Roll Dice"
if st.button(label):
    with st.spinner("Rolling…"):
        time.sleep(0.9)
    st.session_state.die1 = random.randint(1, 6)
    st.session_state.die2 = random.randint(1, 6)
    st.rerun()

if st.session_state.die1:
    total = st.session_state.die1 + st.session_state.die2
    st.info(
        f"Die 1: **{st.session_state.die1}** &nbsp;|&nbsp; "
        f"Die 2: **{st.session_state.die2}** &nbsp;|&nbsp; "
        f"Total: **{total}**"
    )
