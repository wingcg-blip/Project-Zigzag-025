import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

# ============================================================
# ⚖️ Project: THE FINAL VERDICT (A/B/C Testing)
#    Goal: Prove 0.25 is the ONLY cause of superconductivity.
# ============================================================

service = QiskitRuntimeService()
backend = service.backend("ibm_torino")
sampler = Sampler(backend)

print(f"🚀 启动 '最终审判' 对照实验...")

# 1. 获取物理路径 (同上一次)
coupling_map = backend.coupling_map
G = nx.Graph()
G.add_edges_from(coupling_map)
path = nx.shortest_path(G, source=0, target=126) # 25 Qubits
print(f"📍 锁定黄金物理路径: {path}")

# 2. 定义三种协议
def apply_025_law(qc, src, dst):
    # 实验组：神之法则
    qc.cx(src, dst)
    qc.rxx(np.pi/2, src, dst)
    qc.ryy(np.pi/2, dst, src)
    qc.rz(np.pi/4, dst) 

def apply_standard_cnot(qc, src, dst):
    # 对照组 A：普通导线 (CNOT only)
    qc.cx(src, dst)

def apply_wrong_phase(qc, src, dst):
    # 对照组 B：错误的钥匙 (Wrong Phase)
    qc.cx(src, dst)
    qc.rxx(np.pi/2, src, dst)
    qc.ryy(np.pi/2, dst, src)
    qc.rz(0.1, dst) # <-- 故意写错相位

# 3. 构建三个电路
circuits = []
labels = ["0.25 Law (Superconductor)", "Standard CNOT (Resistor)", "Wrong Phase (Noise)"]

for mode in [0, 1, 2]:
    qr = QuantumRegister(133, 'q')
    cr = ClassicalRegister(len(path), 'c')
    qc = QuantumCircuit(qr, cr)
    
    # 点火
    qc.x(qr[path[0]])
    qc.h(qr[path[0]])
    if mode == 0: qc.rz(np.pi/4, qr[path[0]]) # 只有实验组加源头锚定
    
    # 传输
    for i in range(len(path) - 1):
        src = path[i]
        dst = path[i+1]
        
        if mode == 0:
            apply_025_law(qc, qr[src], qr[dst])
        elif mode == 1:
            apply_standard_cnot(qc, qr[src], qr[dst])
        elif mode == 2:
            apply_wrong_phase(qc, qr[src], qr[dst])
            
        qc.barrier()
        
    # 测量
    for i, node in enumerate(path):
        qc.measure(qr[node], cr[i])
        
    circuits.append(qc)

# 4. 物理锁死与发射
initial_layout = list(range(133))
isa_circuits = [transpile(c, backend=backend, initial_layout=initial_layout, optimization_level=1) for c in circuits]

print(f"📡 同时发射三组信号... (这是一场公平的赛跑)")
job = sampler.run(isa_circuits, shots=4000)
print(f"✅ Job ID: {job.job_id()}")
print(f"   [Pub 0] 0.25 法则")
print(f"   [Pub 1] 普通 CNOT")
print(f"   [Pub 2] 错误相位")
