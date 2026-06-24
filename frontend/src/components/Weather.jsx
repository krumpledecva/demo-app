import { useState } from "react";

export default function Weather() {
  const [city, setCity] = useState("");
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function fetch_weather() {
    if (!city.trim()) return;
    setLoading(true);
    setError("");
    setData(null);
    try {
      const res = await fetch(`/api/weather?city=${encodeURIComponent(city)}`);
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Unknown error");
      }
      setData(await res.json());
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="card">
      <h2>🌤 Weather</h2>
      <input
        type="text"
        placeholder="Enter city name…"
        value={city}
        onChange={(e) => setCity(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && fetch_weather()}
      />
      <button onClick={fetch_weather} disabled={loading}>
        {loading ? "Loading…" : "Get temperature"}
      </button>

      {error && <div className="error">⚠ {error}</div>}

      {data && (
        <div className="result">
          <strong>{data.city}</strong><br />
          🌡 {data.temp_c}°C / {data.temp_f}°F<br />
          Feels like {data.feels_like_c}°C<br />
          💧 Humidity {data.humidity}%<br />
          {data.description}
        </div>
      )}
    </div>
  );
}
