# 🏎️ F1 Thermal Control System Simulator

A professional-grade Python simulation of an F1 power unit cooling system.

Built for **performance, fault tolerance, and insight**, this project simulates dynamic thermal behavior with:

* Dual sensor readings
* Fan power control
* State transitions
* Fault detection and escalation
* Data logging and efficiency scoring
* GUI dashboard and full CLI workflow

---

## 📅 Features

* ⚖️ **State Engine**: IDLE, COOLING, WARNING, FAULT, SHUTDOWN
* 🔌 Dual sensor simulation with differential fault detection
* 📈 Real-time GUI dashboard (Tkinter)
* ✅ Full test suite with coverage report
* 📉 Log analyzer with efficiency score
* 🔧 One-click .bat launcher (Windows)
* 🔨 Makefile for macOS/Linux
* ♻️ GitHub Actions-ready CI integration

---

## ✨ Quick Start

### ▶ Run Simulation

```bash
python main.py
```

### 🔹 Launch GUI Dashboard

```bash
python ui/dashboard.py
```

### 📊 Analyze Results

```bash
python scripts/analyze_log.py
```

---

## 🤔 Testing & Coverage

```bash
pytest --cov=core tests/
coverage html
start htmlcov/index.html
```

---

## 📀 One-Click Batch Launcher (Windows)

Run with:

```bash
f1_run.bat
```

Menu options:

* Start Simulation
* Launch GUI
* Run Tests
* View Coverage
* Analyze Log
* Clean Logs

---

## ⚙️ Makefile (Linux/macOS)

```bash
make run         # Run main.py
make gui         # Launch GUI
make test        # Run unit tests
make coverage    # Generate coverage report
make analyze     # Analyze logs
make clean       # Clean logs and coverage
```

---

## 📂 Project Structure

```
f1_thermal_control_sim/
├── core/              # Logic: control, sensors, logger
├── data/              # Output: logs, plots
├── tests/             # Unit tests
├── ui/                # Tkinter GUI
├── scripts/           # Analysis scripts
├── visualisation/     # Extra plots (optional)
├── main.py            # Entry point
├── Makefile
├── f1_run.bat         # Windows menu
└── README.md
```

---

## 📃 Requirements

* Python 3.10+
* `pytest`, `coverage`, `matplotlib`

```bash
pip install -r requirements.txt
```

---

## 💪 Built by Wissal

Designed like an F1 car: precise, efficient, and fault-resilient.

Simulation meets software engineering — because performance matters.

---

## 📘 License

MIT License. Use, share, contribute.
