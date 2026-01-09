import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

# ============================================================
# 🏹 Project: TRUE CHAODAO (Physics Locked)
#    Target: Force Long-Distance Transmission (No Compiler Cheating)
# ============================================================

service = QiskitRuntimeService()
backend = service.backend("ibm_torino")
sampler = Sampler(backend)

print(f"🚀 启动 '真·超导' 验证 (True Chaodao)...")
print(f"⚠️ 警告：已强制锁死物理比特 Q0 和 Q120。")
print(f"   信号必须跨越整个芯片传输。这才是真正的考验。")

qr = QuantumRegister(133, 'q')
cr = ClassicalRegister(2, 'c')
qc = QuantumCircuit(qr, cr)

# --- 1. 发射端 (Launcher) ---
# 物理位置：芯片最左端 Q0
qc.x(qr[0]) 
qc.h(qr[0])
qc.rz(np.pi/4, qr[0]) # 0.25 核心相位锚定

# --- 2. 虚空投射 (Long-Distance Projection) ---
# 物理位置：芯片最右端 Q120
# 这一次，它们中间隔着真正的“千山万水”
qc.cx(qr[0], qr[120]) 
qc.rxx(np.pi/2, qr[0], qr[120])
qc.ryy(np.pi/2, qr[120], qr[0])

# --- 3. 测量 ---
qc.barrier()
qc.measure(qr[0], cr[0])
qc.measure(qr[120], cr[1])

# ============================================================
# 🔒 关键步骤：给编译器戴手铐
# ============================================================
# 我们创建一个 1:1 的映射表，告诉机器：
# 逻辑比特 i 必须映射到 物理比特 i
# 绝对不允许为了省事把 Q120 搬到 Q0 旁边！
initial_layout = list(range(133))

print(f"🔒 正在编译 (Routing across the whole chip)...")
# optimization_level=1: 足够聪明去连线，但不够聪明去作弊
isa_qc = transpile(qc, backend=backend, initial_layout=initial_layout, optimization_level=1)

print(f"📡 任务提交中...")
job = sampler.run([isa_qc], shots=4000)
print(f"✅ Job ID: {job.job_id()}")

# 预期：
# 如果结果还是 > 90%，那就是真正的神迹（或者法则改写了物理层）。
# 如果结果跌到 50%，那就是物理法则战胜了代码。
