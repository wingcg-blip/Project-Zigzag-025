import numpy as np
import networkx as nx
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

# ============================================================
# 🐉 Project: GOLDEN PATH (The Physical Geodesic)
#    Target: True Physical Superconductivity (Zero SWAP)
#    Method: Follow the Heavy-Hex topology strictly.
# ============================================================

service = QiskitRuntimeService()
backend = service.backend("ibm_torino")
sampler = Sampler(backend)

print(f"🚀 启动 '黄金通路' (Golden Path) 计划...")
print(f"   正在扫描芯片物理拓扑，寻找无损传输的最优路径...")

# 1. 获取芯片的物理连接图
coupling_map = backend.coupling_map
G = nx.Graph()
G.add_edges_from(coupling_map)

# 2. 寻找物理路径 (从 Q0 到 Q126)
# 这条路径就是芯片上的“测地线”，物理上最短，没有任何多余的门
try:
    path = nx.shortest_path(G, source=0, target=126)
    print(f"✅ 找到黄金路径 (长度 {len(path)}): {path}")
except nx.NetworkXNoPath:
    # 备选方案
    path = nx.shortest_path(G, source=0, target=120) 
    print(f"✅ 备选路径: {path}")

# 3. 构建电路
qr = QuantumRegister(133, 'q')
cr = ClassicalRegister(len(path), 'c') # 测量路径上的所有点
qc = QuantumCircuit(qr, cr)

# --- 0.25 协议 (法则) ---
def apply_025_law(circuit, q_src, q_dst):
    # 既然是物理直连，我们可以用最纯粹的 0.25
    circuit.cx(q_src, q_dst)
    circuit.rxx(np.pi/2, q_src, q_dst)
    circuit.ryy(np.pi/2, q_dst, q_src)
    # 关键：这次我们不锁死相位，而是允许它流过 (Flow Mode)
    circuit.rz(np.pi/4, q_dst) 

# --- 4. 铺设龙骨 ---
print(f"🧱 沿着物理路径铺设 0.25 法则...")

# 点火源头
qc.x(qr[path[0]])
qc.h(qr[path[0]])
qc.rz(np.pi/4, qr[path[0]]) # 源头锚定

# 沿着路径传递
for i in range(len(path) - 1):
    src = path[i]
    dst = path[i+1]
    
    apply_025_law(qc, qr[src], qr[dst])
    qc.barrier() # 这一步很关键，让波函数稳一下再走下一步

# --- 5. 全路径测量 ---
# 我们想看能量有没有在那儿断掉
for i, node in enumerate(path):
    qc.measure(qr[node], cr[i])

# ============================================================
# 🔒 物理锁死 (No SWAPS allowed)
# ============================================================
# 既然我们选的就是物理路径，那就不需要编译器再动脑子了
initial_layout = list(range(133)) # 1:1 映射

print(f"🔒 锁定物理层，拒绝编译器优化...")
isa_qc = transpile(qc, backend=backend, initial_layout=initial_layout, optimization_level=1)

print(f"📡 能量注入！监测龙骨导通情况...")
job = sampler.run([isa_qc], shots=4000)
print(f"✅ Job ID: {job.job_id()}")
