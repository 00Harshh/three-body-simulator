
# 🌌 Chaotic-Orbits: A Python 3-Body Problem Simulator

This project simulates the **three-body problem** using **Python**, **NumPy**, and **Matplotlib**, applying the **Runge-Kutta 4th Order Method (RK4)** for numerical integration. It visualizes gravitational interactions and highlights the chaotic nature of multi-body systems.

---

## 🔭 What is the 3-Body Problem?

The **three-body problem** models how three celestial bodies move under mutual gravitational attraction. Unlike two-body systems, which are predictable and solvable analytically, **three-body systems exhibit chaos**—tiny changes in starting conditions result in dramatically different outcomes. No general closed-form solution exists.

> “This problem puzzled minds like Newton, Euler, and Lagrange for centuries.”

---

## 🎯 Features

* ⚙️ **RK4 Integration**: Accurate, stable time stepping.
* 🌠 **Real-time 2D simulation** with trails.
* ♾️ **Energy conservation tracking**.
* 🔀 **Supports different initial conditions & masses**.
* 📉 Optional plots for energy, Lyapunov divergence, and chaos indicators.
* 🖥️ Clean, modular, beginner-friendly Python code.

---

## 🧠 Concepts Covered

* Newtonian gravity
* Differential equations & numerical integration (RK4)
* Chaos theory & sensitivity to initial conditions
* Conservation of energy in physical simulations
* Visualization with `matplotlib`

---

## 🛠 Installation

```bash
git clone https://github.com/your-username/chaotic-orbits.git
cd chaotic-orbits
pip install -r requirements.txt
```

**Requirements:**

* Python 3.8+
* NumPy
* Matplotlib

---

## 🚀 How to Run

```bash
python main.py
```

You can modify the initial positions, velocities, and masses in `main.py` or `config.py` to explore different behaviors.

---

## 🧪 Example Output

* **Orbit trajectories** (animated)
* **Energy conservation plot**
* **Divergence from tiny perturbations**

<p align="center">
  <img src="media/sample_simulation.gif" width="500"/>
</p>

---

## ⚙️ File Structure

```
chaotic-orbits/
├── main.py               # Simulation entry point
├── simulator.py          # RK4 + gravity logic
├── visualizer.py         # Matplotlib animation & plots
├── config.py             # Initial conditions & settings
├── utils.py              # Energy, distance, etc.
├── requirements.txt
└── README.md
```

---

## 📊 Future Features (Planned)

* ✅ Add 3D visualization
* ✅ Include Lyapunov exponent calculation
* ⏳ GPU acceleration (via CuPy or JAX)
* ⏳ Web-based visualization using Plotly or Three.js
* ⏳ Add Poincaré section generator

---

## 👨‍💻 Author

**Harsh Joshi**

> I build physics-inspired simulations, neural nets from scratch, and explore chaos & AI with Python.

* GitHub: [@your-username](https://github.com/your-username)
* Twitter: [@your-handle](https://twitter.com/your-handle) (if any)
* Blog: \[Your Hashnode/Medium link]

---

## 🧠 References

* Newton’s Law of Gravitation
* [Wikipedia - Three-Body Problem](https://en.wikipedia.org/wiki/Three-body_problem)
* [MIT OCW Classical Mechanics](https://ocw.mit.edu)
* [RK4 Method](https://en.wikipedia.org/wiki/Runge–Kutta_methods)

---

## 🌌 License

MIT License — feel free to use and modify this code. Star the repo if it helped you!

---

