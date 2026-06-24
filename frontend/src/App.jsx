import Weather from "./components/Weather";
import Dice from "./components/Dice";

export default function App() {
  return (
    <div className="app">
      <h1>Demo App</h1>
      <div className="panels">
        <Weather />
        <Dice />
      </div>
    </div>
  );
}
