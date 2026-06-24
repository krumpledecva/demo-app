import { useState } from "react";
import Die3D from "./Die3D";

export default function Dice() {
  const [die1, setDie1] = useState(null);
  const [die2, setDie2] = useState(null);
  const [rolling, setRolling] = useState(false);
  const [error, setError] = useState("");

  async function roll() {
    setRolling(true);
    setError("");
    setDie1(null);
    setDie2(null);

    await new Promise((r) => setTimeout(r, 1000));

    try {
      const res = await fetch("/api/dice");
      if (!res.ok) throw new Error("Server error");
      const data = await res.json();
      setDie1(data.die1);
      setDie2(data.die2);
    } catch {
      setError("Could not roll dice. Is the backend running?");
    } finally {
      setRolling(false);
    }
  }

  return (
    <div className="card">
      <h2>🎲 Dice Roller</h2>

      <div className="dice-row">
        <Die3D value={die1} rolling={rolling} />
        <Die3D value={die2} rolling={rolling} />
      </div>

      {die1 && die2 && !rolling && (
        <div className="dice-total">
          Die 1: {die1} &nbsp;|&nbsp; Die 2: {die2} &nbsp;|&nbsp; Total: {die1 + die2}
        </div>
      )}

      {error && <div className="error">⚠ {error}</div>}

      <button onClick={roll} disabled={rolling} style={{ width: "100%" }}>
        {rolling ? "Rolling…" : die1 ? "Roll Again" : "Roll Dice"}
      </button>
    </div>
  );
}
