import random
import time
import json
import urllib.request
import urllib.parse
import streamlit as st

st.set_page_config(page_title="Demo App", page_icon="🎲", layout="centered")

# ── Mint green theme ───────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #f0fdfb; }
    h1 { color: #00BFA5 !important; }
    h2, h3 { color: #00BFA5 !important; }
    .stButton > button {
        background-color: #00BFA5 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
    }
    .stButton > button:hover { background-color: #00A693 !important; }
    .stTextInput > div > div > input {
        border: 1.5px solid #80CBC4 !important;
        border-radius: 8px !important;
        color: #134E4A !important;
    }
    .stTextInput > div > div > input:focus { border-color: #00BFA5 !important; }
    .stSuccess { border-left-color: #00BFA5 !important; background-color: #e0f7f4 !important; }
    .stInfo { border-left-color: #00BFA5 !important; }
    [data-testid="stHeader"] { background: transparent; }
    hr { border-color: #b2dfdb !important; }
</style>
""", unsafe_allow_html=True)

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


def fetch_json(url):
    with urllib.request.urlopen(url, timeout=10) as r:
        return json.loads(r.read().decode())


# ── Weather ────────────────────────────────────────────────────────────────────
st.header("🌤 Weather")
city = st.text_input("Enter a city name", placeholder="e.g. Ljubljana")

if st.button("Get temperature"):
    if not city.strip():
        st.warning("Please enter a city name.")
    else:
        with st.spinner("Fetching weather…"):
            try:
                geo_url = (
                    "https://geocoding-api.open-meteo.com/v1/search?"
                    + urllib.parse.urlencode({"name": city.strip(), "count": 1,
                                              "language": "en", "format": "json"})
                )
                geo = fetch_json(geo_url)
                results = geo.get("results")
                if not results:
                    st.error(f"City '{city}' not found.")
                else:
                    loc = results[0]
                    lat, lon = loc["latitude"], loc["longitude"]
                    city_label = f"{loc['name']}, {loc.get('country', '')}"

                    w_url = (
                        "https://api.open-meteo.com/v1/forecast?"
                        + urllib.parse.urlencode({
                            "latitude": lat,
                            "longitude": lon,
                            "current": "temperature_2m,apparent_temperature,relative_humidity_2m,weather_code",
                            "temperature_unit": "celsius",
                        })
                    )
                    w = fetch_json(w_url)
                    cur = w["current"]
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

                    # OpenStreetMap embed
                    map_url = (
                        f"https://www.openstreetmap.org/export/embed.html"
                        f"?bbox={lon-0.4},{lat-0.4},{lon+0.4},{lat+0.4}"
                        f"&layer=mapnik&marker={lat},{lon}"
                    )
                    st.components.v1.iframe(map_url, height=220)

            except Exception as e:
                st.error(f"Could not fetch weather: {e}")

st.divider()

# ── Dice ───────────────────────────────────────────────────────────────────────
FACES = ["", "⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]

st.header("🎲 Dice Roller")

if "die1" not in st.session_state:
    st.session_state.die1 = None
    st.session_state.die2 = None

col1, col2 = st.columns(2)
with col1:
    face1 = FACES[st.session_state.die1] if st.session_state.die1 else "🎲"
    st.markdown(f"<div style='font-size:4rem;text-align:center'>{face1}</div>",
                unsafe_allow_html=True)
with col2:
    face2 = FACES[st.session_state.die2] if st.session_state.die2 else "🎲"
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
