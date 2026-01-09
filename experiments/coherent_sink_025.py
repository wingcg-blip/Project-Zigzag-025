import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

# ============================================================
# 🕳️ Project: BLACK HOLE VERIFICATION (Re-Run)
#    Target: Re-verify the 0.0000 quenching effect on Q0
# ============================================================

service = QiskitRuntimeService()
backend = service.backend("ibm_torino")
sampler = Sampler(backend)

print(f"🚀 启动 '5点骨架' 复刻实验 (The Black Hole Re-run)...")

# --- 0.25 Protocol Function ---
def apply_025_connection(qc, center, anchor):
    qc.cx(center, anchor)
    qc.rxx(np.pi/2, center, anchor)
    qc.ryy(np.pi/2, anchor, center)
    qc.rz(np.pi/4, anchor)

# ============================================================
# 🧪 Circuit 1: 实验组 (The Black Hole)
#    Q0 点火，且连接在 0.25 骨架上 -> 预期被淬灭 (0.0)
# ============================================================
qr1 = QuantumRegister(133, 'q_exp')
cr1 = ClassicalRegister(133, 'c_exp')
qc_exp = QuantumCircuit(qr1, cr1, name="Black_Hole_Exp")

center = 66
anchors = [0, 24, 109, 126] # Q0 在骨架内！

# 1. 点火 Q0
qc_exp.x(qr1[0])
qc_exp.h(qr1[0])

# 2. 施加骨架 (吸能网络)
for anchor in anchors:
    apply_025_connection(qc_exp, qr1[center], qr1[anchor])

qc_exp.barrier()
qc_exp.measure(qr1, cr1)

# ============================================================
# 🏳️ Circuit 2: 对照组 (Control)
#    Q0 点火，但【没有】骨架连接 -> 预期正常发光 (0.5)
# ============================================================
qr2 = QuantumRegister(133, 'q_ctrl')
cr2 = ClassicalRegister(133, 'c_ctrl')
qc_ctrl = QuantumCircuit(qr2, cr2, name="Control_No_Skeleton")

# 1. 点火 Q0 (完全一样的点火)
qc_ctrl.x(qr2[0])
qc_ctrl.h(qr2[0])

# 2. 无骨架 (孤立)
# Q0 是自由的，没有连接 Q66

qc_ctrl.barrier()
qc_ctrl.measure(qr2, cr2)

# ============================================================
# 🚀 提交任务
# ============================================================
# 强制指定物理比特映射，确保 Q0 就是物理上的 Q0
layout = list(range(133)) 
isa_qc_exp = transpile(qc_exp, backend=backend, initial_layout=layout, optimization_level=1)
isa_qc_ctrl = transpile(qc_ctrl, backend=backend, initial_layout=layout, optimization_level=1)

print(f"📡 正在提交双对比实验...")
job = sampler.run([isa_qc_exp, isa_qc_ctrl], shots=4000)
print(f"✅ Job ID: {job.job_id()}")
print(f"   [PUB 0] 实验组: 有骨架 (预期 Q0 ≈ 0.0)")
print(f"   [PUB 1] 对照组: 无骨架 (预期 Q0 ≈ 0.5)")
