import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

# ============================================================
# 🏹 Project: One-Way Anchoring (The Ballistic Test)
#    Target: Launch at Q0, Measure at Q120. No terminal locking.
# ============================================================

service = QiskitRuntimeService()
backend = service.backend("ibm_torino")

qr = QuantumRegister(133, 'q')
cr = ClassicalRegister(2, 'c')
qc = QuantumCircuit(qr, cr)

# --- 1. 起点：全力注入 (The Launcher) ---
qc.x(qr[0]) 
qc.h(qr[0])
qc.rz(np.pi/4, qr[0]) # 核心 0.25 锚定

# --- 2. 虚空投射 (The Projection) ---
# 直接通过双比特门将相位“甩”出去
qc.cx(qr[0], qr[120]) 
qc.rxx(np.pi/2, qr[0], qr[120])
qc.ryy(np.pi/2, qr[120], qr[0])

# --- 注意：这里没有任何终点锁定，完全看相位的自我维持能力 ---

qc.barrier()

# --- 3. 测量 ---
qc.measure(qr[0], cr[0])
qc.measure(qr[120], cr[1])

# --- 4. 编译与发射 ---
print("🏹 正在执行‘单向锚定’：看 0.25 的几何惯性能飞多远...")
isa_qc = transpile(qc, backend=backend, optimization_level=1)
sampler = Sampler(backend)

job = sampler.run([isa_qc], shots=4000)
print(f"✅ 任务 ID: {job.job_id()}")
