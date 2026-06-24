import { useEffect, useRef, useState } from "react";

// Cube face → value + unique pip colour per side
const FACE_ASSIGNMENTS = [
  { side: "front",  value: 1, color: "#e53e3e" }, // red
  { side: "back",   value: 6, color: "#3182ce" }, // blue
  { side: "right",  value: 2, color: "#38a169" }, // green
  { side: "left",   value: 5, color: "#dd6b20" }, // orange
  { side: "top",    value: 3, color: "#805ad5" }, // purple
  { side: "bottom", value: 4, color: "#0987a0" }, // teal
];

// Rotation to bring each face value to the front
const ROTATIONS = {
  1: "rotateX(0deg)   rotateY(0deg)",
  2: "rotateX(0deg)   rotateY(-90deg)",
  3: "rotateX(90deg)  rotateY(0deg)",
  4: "rotateX(-90deg) rotateY(0deg)",
  5: "rotateX(0deg)   rotateY(90deg)",
  6: "rotateX(0deg)   rotateY(180deg)",
};

// 3×3 grid indices that should have pips for each die value
const PIPS = {
  1: new Set([4]),
  2: new Set([2, 6]),
  3: new Set([2, 4, 6]),
  4: new Set([0, 2, 6, 8]),
  5: new Set([0, 2, 4, 6, 8]),
  6: new Set([0, 2, 3, 5, 6, 8]),
};

// The distinct face rotations used during the tumble animation
const TUMBLE_POSES = [
  [0, 0], [90, 0], [-90, 0], [0, 90], [0, -90], [0, 180],
];

function Face({ value, color }) {
  const pips = PIPS[value];
  return (
    <div className="die-face-grid">
      {Array.from({ length: 9 }, (_, i) =>
        pips.has(i)
          ? <div key={i} className="die-pip" style={{ background: color }} />
          : <div key={i} className="die-pip die-pip--empty" />
      )}
    </div>
  );
}

export default function Die3D({ value, rolling }) {
  const [rotation, setRotation] = useState(ROTATIONS[1]);
  const timerRef = useRef(null);
  const poseRef = useRef(0);

  useEffect(() => {
    clearTimeout(timerRef.current);

    if (rolling) {
      const tumble = () => {
        poseRef.current = (poseRef.current + 1) % TUMBLE_POSES.length;
        const [rx, ry] = TUMBLE_POSES[poseRef.current];
        setRotation(`rotateX(${rx}deg) rotateY(${ry}deg)`);
        timerRef.current = setTimeout(tumble, 120);
      };
      tumble();
    } else if (value) {
      setRotation(ROTATIONS[value]);
    }

    return () => clearTimeout(timerRef.current);
  }, [rolling, value]);

  return (
    <div className="die3d-scene">
      <div className="die3d-cube" style={{ transform: rotation }}>
        {FACE_ASSIGNMENTS.map(({ side, value: faceVal, color }) => (
          <div key={side} className={`die3d-face die3d-face--${side}`}>
            <Face value={faceVal} color={color} />
          </div>
        ))}
      </div>
    </div>
  );
}
