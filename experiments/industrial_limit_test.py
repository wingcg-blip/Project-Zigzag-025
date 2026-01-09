import numpy as np
import networkx as nx
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

# ============================================================
# 🏭 PROJECT: INDUSTRIAL LIMIT TEST (The "Death Valley" Run)
#    Target: Maximum Physical Path Length on IBM Torino
# ============================================================

def find_longest_snake_path(backend):
    """
    贪婪算法寻找芯片上的最长物理连通路径（贪吃蛇模式）。
    不保证是绝对最长（NP-hard），但能找到接近极限的长链。
    """
    print("🗺️ 正在扫描芯片架构 (Mapping Topology)...")
    cm = backend.coupling_map
    G = nx.Graph()
    G.add_edges_from(cm)
    
    # 策略：从度数最小的节点（角落）开始，进行深度优先搜索 (DFS)
    # 寻找最深的一条分支
    longest_path = []
    
    # 尝试从所有边缘节点出发，找最长的一条
    degrees = dict(G.degree())
    start_candidates = [n for n, d in degrees.items() if d <= 2] # 边缘节点
    
    print(f"🔍 正在从 {len(start_candidates)} 个边缘点发起寻路探针...")
    
    for start_node in start_candidates:
        # 简单的贪婪 DFS：优先去没去过的邻居
        current_path = [start_node]
        current_node = start_node
        visited = {start_node}
        
        while True:
            neighbors = list(G.neighbors(current_node))
            # 找没去过的邻居
            unvisited = [n for n in neighbors if n not in visited]
            
            if not unvisited:
                break # 走到死胡同了
                
            # 贪婪策略：如果有多个邻居，优先选度数小的（沿着边缘走容易绕得长）
            # 或者选离终点远的？这里简单选第一个
            # 优化：优先选邻居中“未访问邻居数”最少的（避免把路堵死）
            best_next = unvisited[0] 
            
            current_path.append(best_next)
            visited.add(best_next)
            current_node = best_next
            
        if len(current_path) > len(longest_path):
            longest_path = current_path
            
    return longest_path

# 1. 初始化
service = QiskitRuntimeService()
backend = service.backend("ibm_torino")
print(f"🚀 连接后端: {backend.name} (Qubits: {backend.num_qubits})")

# 2. 寻找死亡行军路线
path = find_longest_snake_path(backend)
print(f"🔥 锁定最长路径: {len(path)} 步 (Steps)")
print(f"📍 路径节点: {path}")

if len(path) < 50:
    print("⚠️ 警告：路径长度不足 50，可能无法观测到明显的‘死亡谷效应’。")
else:
    print("✅ 路径长度充足，准备进入‘死亡谷’测试。")

# 3. 定义三种工业协议
def apply_025_law(qc, src, dst):
    # 实验组：拓扑装甲 (Topological Armor)
    qc.cx(src, dst)
    qc.rxx(np.pi/2, src, dst)
    qc.ryy(np.pi/2, dst, src)
    qc.rz(np.pi/4, dst) 

def apply_standard_cnot(qc, src, dst):
    # 对照组 A：裸奔 (Naked Wire)
    qc.cx(src, dst)

def apply_robust_check(qc, src, dst):
    # 对照组 B：宽容度测试 (0.1 Phase)
    qc.cx(src, dst)
    qc.rxx(np.pi/2, src, dst)
    qc.ryy(np.pi/2, dst, src)
    qc.rz(0.1, dst)

# 4. 构建电路
circuits = []
labels = ["0.25 Law (Armor)", "Standard CNOT (Naked)", "Robust 0.1 (Check)"]
modes = [apply_025_law, apply_standard_cnot, apply_robust_check]

for i, mode_func in enumerate(modes):
    qr = QuantumRegister(backend.num_qubits, 'q') # 使用全芯片寄存器
    cr = ClassicalRegister(len(path), 'c') # 只测量路径上的点
    qc = QuantumCircuit(qr, cr)
    
    # 源头点火
    start_node = path[0]
    qc.x(qr[start_node])
    qc.h(qr[start_node])
    if i == 0: qc.rz(np.pi/4, qr[start_node]) # 只有 0.25 组加源头锁
    
    # 传输
    for step in range(len(path) - 1):
        src = path[step]
        dst = path[step+1]
        mode_func(qc, qr[src], qr[dst])
        qc.barrier()
        
    # 测量 (沿途所有点都测，绘制完整衰减曲线)
    for step, node in enumerate(path):
        qc.measure(qr[node], cr[step])
        
    circuits.append(qc)

# 5. 提交任务
print(f"\n📡 正在编译并上传任务 (Shots=4000)...")
# 优化等级设为 1，尽量保留我们的门结构，不让编译器乱动
isa_circuits = [transpile(c, backend=backend, initial_layout=list(range(backend.num_qubits)), optimization_level=1) for c in circuits]

sampler = Sampler(backend)
job = sampler.run(isa_circuits, shots=4000)

print(f"✅ 任务已发射！")
print(f"🆔 Job ID: {job.job_id()}")
print(f"📊 等跑完后，用之前的 Visualization 代码画图，看两条线在哪里分叉！")
