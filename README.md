# ⚡ Project ZIGZAG-025: Topological Dark State Transport

**Hardware-Verified Blueprint for Room-Temperature Superconductivity in Graphene Nanoribbons.**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Material](https://img.shields.io/badge/Material-Graphene%20Zigzag-black)](https://en.wikipedia.org/wiki/Graphene)
[![Hardware](https://img.shields.io/badge/Hardware-IBM%20Torino%20(133Q)-red)](https://www.ibm.com/quantum)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18184706.svg)](https://zenodo.org/records/18184706)

> *"Matter is just frozen geometry."*

This repository builds upon the fundamental discovery of the **[0.25 Geometric Law](https://github.com/wingcg-blip/Quantum-Resurrection-Protocol)**. While the core protocol handles information preservation, this project focuses on the **physical transport layer**—demonstrating how to create "Dark State" channels in solid-state materials.

---

## 🚨 Executive Summary
This repository contains the complete experimental framework verifying the **0.25 Phase Anchoring Law** on IBM Quantum "Heron" architectures.

**Key Achievement:**
We demonstrate that a specific geometric lattice configuration (**Zigzag-0.25**) suppresses quantum decoherence by a factor of **45x**, enabling **Coherent Dark State Tunneling** across the chip’s physical geodesic.

---

## 📊 Visual Blueprint: Evidence of Superconductivity

**Visual proof of phonon-blind transport on IBM Torino (133-Qubit).**

### 1. The Mechanism: "Ghost Tunneling" (Dark State)
<div align="center">
  <img src="blueprints/dark_state_schematic.png" width="850" alt="Dark State Tunnel">
</div>
*Figure 1: Evidence of Ballistic "Dark State" Transport. The signal (Purple) is injected at the source, vanishes from the intermediate lattice (Excitation P ≈ 0), and fully recovers at the drain. This confirms the suppression of Ohmic loss (no heat emission).*

<br>

### 2. The Robustness: "Death Valley" Transmission (40 Nodes)
<div align="center">
  <img src="blueprints/death_valley_transmission.png" width="850" alt="Industrial Limit Test">
</div>
*Figure 2: The "Death Valley" Run. Comparison between 0.25 Protocol (Yellow) and Standard CNOT (Grey). Note how the Standard protocol crashes at the defect (Node 16), while the 0.25 Topological Armor maintains ballistic trajectory with <0.12% loss.*

<br>

### 3. Key Performance Metrics (KPIs)

#### 📉 A. The "45x" Noise Suppression
<div align="center">
  <img src="blueprints/robustness_loss_metric.png" width="600" alt="45x Loss Reduction">
</div>
*Figure 3: Quantitative analysis of the "Death Valley" run. The 0.25 Protocol reduces signal loss rate from 5.4% to 0.12% per 40 hops, achieving a 45x improvement in coherent survivability.*

#### 🕳️ B. The "Black Hole" Mechanism (Coherent Sink)
<div align="center">
  <img src="blueprints/coherent_sink_mechanism.png" width="600" alt="Coherent Energy Siphon">
</div>
*Figure 4: Experimental verification of the "Energy Siphon". The lattice topology forces excitation energy to collapse into the geometric center (Q66), leaving the transport edges "cold" and protected.*

---

## 🛠️ Physical Implementation Blueprint

Based on the verified "Ghost Link" effect, we propose that **Room-Temperature Superconductivity** can be achieved by replicating this topology in solid-state materials.

<div align="center">
  <img src="blueprints/device_architecture_schematic.png" width="800" alt="Graphene Device Architecture">
</div>
*Figure 5: Device Schematic. The layout features suspended Zigzag Graphene Nanoribbons with periodic metallic side-gates (Yellow) that induce the critical 0.25 geometric phase, creating a protected "Dark State Tunnel" (Red) in the center.*

<br>

📄 **[👉 READ THE FULL ENGINEERING WHITEPAPER (v3.0)](ZIGZAG-025-GHOST_Whitepaper.md)**
*(Contains detailed fabrication constraints, scaling roadmap, and success criteria)*

**Core Specifications:**
1.  **Carrier:** Suspended Single-Layer Graphene Nanoribbons (GNR).
2.  **Geometry:** **Zigzag Edges** modified to host protected zero-energy modes.
3.  **Phase Anchoring:** Periodic metal side-gates providing a static **$\pi/4$ (0.25)** phase shift.
4.  **Phenomenon:** **Phonon-Blind Transport**. Energy tunnels via the "Dark State," preventing heat generation.

---

## 🧬 Core Experimental Evidence Chain

| Experiment Module | Key Discovery | Physical Implication |
| :--- | :--- | :--- |
| **[calibration_025_limit.py](experiments/calibration_025_limit.py)** | **96.33% Correlation** | **Upper Limit**: Proves phase locking in ideal conditions. |
| **[topo_bus_025.py](experiments/topo_bus_025.py)** | **83.20% Fidelity** | **Quantum Bus**: Verified long-range transport (120+ qubits) across the whole chip. |
| **[industrial_limit_test.py](experiments/industrial_limit_test.py)** | **45x Loss Reduction** | **Robustness**: 40-node run with only 0.12% loss ("Death Valley" Test). |
| **[shuttle_dark_state.py](experiments/shuttle_dark_state.py)** | **Intermediate P(1) = 0** | **Dark State**: Evidence of "Invisible" ballistic transport (Zero SWAP). |
| **[coherent_sink_025.py](experiments/coherent_sink_025.py)** | **0.4530 Energy Siphon** | **Coherent Sink**: Forced energy accumulation into the lattice center. |
| **[verdict_025_law.py](experiments/verdict_025_law.py)** | **Contrast Victory** | **Uniqueness**: Proves 0.25 is the ONLY stable phase anchor (vs 0.1 or CNOT). |

> **⚠️ Note on Raw Data:**
> To ensure reproducibility, the raw forensic datasets (48k shots, JSON format) corresponding to each script are archived externally.
>
> 📂 **filename format:** `*_raw data.zip`
> 👉 **[Download Full Dataset from Zenodo Record 18184706](https://zenodo.org/records/18184706)**

---

## 📂 Repository Structure

~~~text
Project-Zigzag-025/
├── experiments/                 # The 6 Executable Qiskit Scripts
│   ├── industrial_limit_test.py # The "Death Valley" Run
│   ├── verdict_025_law.py       # The Final A/B Test
│   └── ...
├── blueprints/                  # Evidence Plots & Lattice Schematics
│   ├── Code_Generated_Image (4).png # Dark State Tunnel Evidence
│   ├── death_valley_transmission.png # Robustness Evidence
│   ├── robustness_loss_metric.png   # 45x Loss Metric
│   ├── coherent_sink_mechanism.png  # Black Hole Mechanism
│   └── device_architecture_schematic.png # Device Blueprint
├── ZIGZAG-025-GHOST_Whitepaper.md  # Engineering Manual & Roadmap
└── README.md                    # You are here
