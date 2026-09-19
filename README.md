# 3-Qubit Grover Search Benchmarking on IBM Quantum Hardware

Benchmarking 3-qubit Grover's search on actual IBM Quantum QPUs with Qiskit.

Empirical Implementation of Grover's Quantum Search Algorithm on Real IBM Quantum QPUs (`ibm_fez` and `ibm_marrakesh`) with Qiskit 1.x and Qiskit Runtime V2.

---

## Project Highlights

* Simulated vs. real hardware performance of 2-qubit and 3-qubit Grover search circuits
* Aggressive CNOT minimization via Level 3 passes
* Suppression of phase decoherence of idle qubit via XY4 Dynamical Decoupling

---

## Key Results Summary

* 2-Qubit Grover (on real QPU): ~92% fidelity, low CNOT depth
* 3-Qubit Grover (common CCZ - Level 3 passes): 71.24% fidelity on `ibm_fez`
* 3-Qubit Grover (topology-dependent CCZ - Level 3 passes): only 56.42% fidelity on `ibm_marrakesh` due to calibration and topology effects
* Relative-phase Toffoli experiment with Margolus Gates: constructive phase interference observed on 011 on uncorrected relative phases

---

## NISQ Limitations & Key Conclusions

1. Multi-controlled `ccz` gates (multi-controlled Toffoli equivalents) decompose into native 2-qubit gates: depth (and error) increases with number of control qubits
2. Automated pass manager layout optimized beyond fixed qubit mapping due to calibration variation
3. QEC scaling to larger registers must occur for larger register sizes!
