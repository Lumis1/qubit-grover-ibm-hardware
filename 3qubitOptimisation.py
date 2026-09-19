import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

API_TOKEN = "YOUR_IBM_API_TOKEN_HERE"

QiskitRuntimeService.save_account(channel="ibm_quantum_platform", token=API_TOKEN, overwrite=True)
service = QiskitRuntimeService(channel="ibm_quantum_platform")

backend = service.least_busy(operational=True, simulator=False)
print(f"--> Connected! Selected Real Quantum Backend: {backend.name}")


qc = QuantumCircuit(3, 3)


qc.h([0, 1, 2])


qc.ccz(0, 1, 2)


qc.h([0, 1, 2])
qc.x([0, 1, 2])
qc.ccz(0, 1, 2)
qc.x([0, 1, 2])
qc.h([0, 1, 2])


qc.measure([0, 1, 2], [0, 1, 2])

print("--- 3-Qubit Grover Search Circuit ---")
print(qc.draw(output='text'))

pass_manager = generate_preset_pass_manager(
    backend=backend, 
    optimization_level=3,
)
isa_circuit = pass_manager.run(qc)

TARGET_STATE = "111"

print(f"\n--> Submitting circuit to real quantum processor ({backend.name})...")

sampler = Sampler(mode=backend)
sampler.options.dynamical_decoupling.sequence_type = "XY4"


job = sampler.run([isa_circuit])

print(f"--> Job successfully submitted! Job ID: {job.job_id()}")
print("--> Waiting for quantum processor results (retrieving from cloud queue)...")

result = job.result()
pub_result = result[0]

counts = pub_result.data.c.get_counts()

correct_counts = counts.get(TARGET_STATE, 0)
total_shots = sum(counts.values())

fidelity_pct = (correct_counts / total_shots) * 100
error_pct = 100.0 - fidelity_pct

print("\n--- Performance Metrics (Real QPU) ---")
print(f"Backend Used:         {backend.name}")
print(f"Target State:         '{TARGET_STATE}'")
print(f"Total Shots:          {total_shots}")
print(f"Correct Reads ('{TARGET_STATE}'): {correct_counts} ({fidelity_pct:.2f}%)")
print(f"Error Rate (Noise):   {error_pct:.2f}%")


fig = plot_histogram(counts)
plt.title(f"Real QPU ({backend.name}) - 3-Qubit Grover Search (Target: '{TARGET_STATE}')\nFidelity: {fidelity_pct:.2f}% | Error Rate: {error_pct:.2f}%")
plt.tight_layout()
plt.show()