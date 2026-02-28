import streamlit as st
import pandas as pd
import random
import time
import math
import plotly.graph_objects as go

# --- 1. 页面与全局配置 ---
st.set_page_config(
    page_title="SDE 核心人才资产引擎",
    page_icon="💠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. 殿堂级 UI 引擎与动效注入 ---
st.markdown("""
<style>
    /* 1. 沉浸式深空背景 */
    [data-testid="stAppViewContainer"] { 
        background-color: #050a15 !important; 
        background-image: 
            radial-gradient(circle at 50% 0%, #112240 0%, #050a15 60%),
            linear-gradient(0deg, rgba(0,243,255,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0,243,255,0.03) 1px, transparent 1px) !important;
        background-size: 100% 100%, 30px 30px, 30px 30px !important;
    }
    
    /* 强制高对比度文本，告别模糊 */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp p, .stApp span, .stApp div { color: #f8fafc; }
    
    /* 2. 封面与标题高定光感 */
    .hero-title { 
        font-size: 38px !important; font-weight: 900 !important; text-align: center; 
        color: #ffffff !important; letter-spacing: 3px; margin-bottom: 10px;
        text-shadow: 0 0 20px rgba(0,243,255,0.8), 0 0 40px rgba(0,243,255,0.4);
    }
    .hero-subtitle {
        text-align: center; color: #00f3ff !important; font-size: 14px; 
        letter-spacing: 4px; opacity: 0.8; margin-bottom: 40px; font-family: monospace;
    }
    .hero-desc {
        background: rgba(15, 23, 42, 0.8); border-left: 4px solid #00f3ff;
        padding: 25px; border-radius: 12px; line-height: 1.8; font-size: 15px;
        color: #e2e8f0; box-shadow: 0 10px 30px rgba(0,0,0,0.5); margin-bottom: 40px;
    }

    /* 3. 互动感拉满的启动按钮 */
    .start-btn > div > button {
        width: 100% !important; height: 75px !important; font-size: 22px !important;
        font-weight: 900 !important; border-radius: 16px !important; color: #050a15 !important;
        background: linear-gradient(90deg, #00f3ff, #00b7ff) !important;
        border: none !important; transition: all 0.2s ease !important;
        box-shadow: 0 0 20px rgba(0,243,255,0.4), inset 0 0 10px rgba(255,255,255,0.5) !important;
        letter-spacing: 2px !important;
    }
    .start-btn > div > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 0 40px rgba(0,243,255,0.8), inset 0 0 15px rgba(255,255,255,0.8) !important;
    }
    .start-btn > div > button:active { transform: scale(0.95) !important; }

    /* 4. 答题界面的阻尼感选项按钮 */
    .question-btn > button {
        width: 100% !important; min-height: 65px !important; border-radius: 12px !important;
        background: rgba(15, 23, 42, 0.85) !important;
        border: 1px solid rgba(0, 243, 255, 0.2) !important;
        color: #ffffff !important; font-size: 16px !important; text-align: left !important;
        transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1) !important;
        padding: 12px 20px !important; line-height: 1.6 !important; font-weight: 500 !important;
    }
    .question-btn > button:hover { 
        border-color: #00f3ff !important; background: rgba(0, 243, 255, 0.15) !important;
        box-shadow: 0 0 15px rgba(0,243,255,0.3) !important; transform: translateX(5px);
    }
    .question-btn > button:active { background: #00f3ff !important; color: #050a15 !important; transform: scale(0.98); }

    /* 5. 高对比度结果视窗 (解决看不清痛点) */
    .result-card {
        padding: 40px 25px; border-radius: 20px; 
        background: #0f172a; /* 深渊曜黑底色，确保文字对比度 */
        border: 1px solid #334155; border-top: 6px solid #ffd700;
        text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.8); margin-bottom: 30px;
    }
    .mbti-code { font-size: 80px; font-weight: 900; color: #ffd700 !important; line-height: 1.1; letter-spacing: 2px; text-shadow: 0 0 30px rgba(255,215,0,0.5); margin: 0;}
    .mbti-post { font-size: 24px; font-weight: bold; color: #00f3ff !important; margin: 15px 0; }
    .mbti-desc { color: #ffffff !important; font-size: 16px; line-height: 1.8; opacity: 0.95; margin-bottom: 20px;}
    .cyber-tag { background: #1e293b; color: #00f3ff !important; border: 1px solid #00f3ff; padding: 5px 14px; border-radius: 6px; font-size: 13px; font-weight: 700; margin: 4px; display: inline-block; }

    /* 6. 超新星中心炸裂动画 (重构物理引擎) */
    .firework-center { 
        position: fixed; top: 50%; left: 50%; z-index: 99999; pointer-events: none;
        font-weight: 900; color: transparent; -webkit-text-stroke: 2px #00f3ff;
        text-shadow: 0 0 20px #00f3ff, 0 0 40px #ffffff;
        animation: supernova 2s cubic-bezier(0.1, 0.9, 0.2, 1) forwards;
    }
    @keyframes supernova { 
        0% { transform: translate(-50%, -50%) scale(0.1) rotate(0deg); opacity: 1; filter: brightness(2); } 
        20% { opacity: 1; filter: brightness(3); }
        100% { transform: translate(calc(-50% + var(--tx)), calc(-50% + var(--ty))) scale(var(--s)) rotate(var(--rot)); opacity: 0; filter: brightness(1) hue-rotate(90deg); } 
    }
</style>
""", unsafe_allow_html=True)

# --- 物理引擎级爆炸生成器 ---
def trigger_supernova():
    html_str = ""
    for _ in range(80): 
        # 使用极坐标计算爆炸落点，确保360度无死角炸裂
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(300, 1000) # 爆炸半径
        tx = distance * math.cos(angle)
        ty = distance * math.sin(angle)
        scale = random.uniform(1.5, 4.0)
        rot = random.randint(-360, 360)
        delay = random.uniform(0, 0.3) # 缩短延迟，增强爆发感
        html_str += f'<div class="firework-center" style="--tx:{tx}px; --ty:{ty}px; --s:{scale}; --rot:{rot}deg; animation-delay:{delay}s; font-size:28px;">666</div>'
    st.markdown(html_str, unsafe_allow_html=True)

# --- 3. 专家级题库库 (全 40 道) ---
questions = [
    {"q": "面对数商生态中各方利益的博弈冲突，我倾向于亲自到现场进行高频次的调解与游说。", "dim": "E"},
    {"q": "代表交易所进行政策咨询时，我享受通过专业表达输出机构影响力的过程。", "dim": "E"},
    {"q": "相比审阅合同，我更擅长通过“头脑风暴”快速萃取业务协同方案。", "dim": "E"},
    {"q": "我习惯于维护庞大的人脉网络，并定期主动激活其中的潜在业务价值。", "dim": "E"},
    {"q": "处理突发声誉风险时，我倾向于迅速发声而非长时间闭门研判。", "dim": "E"},
    {"q": "在大型业务路演中，我发现自己能激发出比独处时更多的创新灵感。", "dim": "E"},
    {"q": "新政策出台后，我会第一时间在专业群组发起讨论而非独自研读。", "dim": "E"},
    {"q": "面对跨部门协作壁垒，我倾向于用非正式的社交手段来打破僵局。", "dim": "E"},
    {"q": "我能适应高强度的商务谈判频率，并从中获得极大的成就感。", "dim": "E"},
    {"q": "在推行规则时，我坚信“现场宣贯”的效果远优于“文件下发”。", "dim": "E"},
    {"q": "即使是宏大的项目，我也会先死磕会计科目调整的每一个底层逻辑。", "dim": "S"},
    {"q": "我更信任成交曲线和合规存证等量化数据，而非定性的趋势预判。", "dim": "S"},
    {"q": "面对新名词（如隐私计算），我首先关注其具体的技术落地路径。", "dim": "S"},
    {"q": "我认为交易所的核心任务是把确权、存证、结算动作做到零差错。", "dim": "S"},
    {"q": "撰写报告时，我习惯于堆叠详实的事实证据，而非过多的战略隐喻。", "dim": "S"},
    {"q": "相比于预测十年规划，我更关心下个季度的结算效率如何提升。", "dim": "S"},
    {"q": "成熟的交易所应当像精密机器，规则的稳定性优于频繁的创新。", "dim": "S"},
    {"q": "在法律文本面前，我总能敏锐捕捉到导致实操失败的措辞隐患。", "dim": "S"},
    {"q": "我偏好有明确时间节点的阶段性产出，即使只是流程的微小改良。", "dim": "S"},
    {"q": "对于审核上架，我倾向于依赖标准清单而非主观的价值评估。", "dim": "S"},
    {"q": "即使影响交易额，我也会关停任何存在合规瑕疵的高收益项目。", "dim": "T"},
    {"q": "评估数商信用时，我只看客观履约数据，不看行业内的情感口碑。", "dim": "T"},
    {"q": "交易所职责应当职责分明、冷酷高效，过度人情味会损伤公平。", "dim": "T"},
    {"q": "面对跨部门争议，我倾向于寻找逻辑最优解，而非寻求情感平衡。", "dim": "T"},
    {"q": "当下属工作出现失误，我会直接指出逻辑谬误，认为这是最高效的。", "dim": "T"},
    {"q": "我倾向于通过智能合约等技术手段替代人工审核，确保绝对公平。", "dim": "T"},
    {"q": "在收益分配中，我坚信“贡献度量化”应绝对优于“生态扶持”。", "dim": "T"},
    {"q": "面对不合理的业务要求，我会列举逻辑障碍回绝，而非婉转迁就。", "dim": "T"},
    {"q": "合规官应当像法官一样理智，不被外界的业务热潮所干扰。", "dim": "T"},
    {"q": "处理投诉时，我关注问题的本质技术原因，而非投诉者的情绪。", "dim": "T"},
    {"q": "我会为重大项目建立多级倒排计划，并极其反感进度失去控制。", "dim": "J"},
    {"q": "我的云盘文件夹拥有严密的分类逻辑，索引缺失会让我感到不适。", "dim": "J"},
    {"q": "如果没有形成明确的决议和责任人，我会认为这场会议是失败的。", "dim": "J"},
    {"q": "我倾向于在项目初期锁定所有需求，对中途变卦持排斥态度。", "dim": "J"},
    {"q": "即便再忙碌，我也坚持每日进行工作复盘并更新待办任务清单。", "dim": "J"},
    {"q": "交易所运营应当“重制度设计、轻即兴发挥”，哪怕牺牲反应速度。", "dim": "J"},
    {"q": "我几乎从不拖延，因为待办清单的存在会带给我无形的心理压力。", "dim": "J"},
    {"q": "我更喜欢节奏稳定、可预测的环境，而非每天处理突发任务。", "dim": "J"},
    {"q": "为了确保最终交付质量，我会提前预留出至少20%的缓冲时间。", "dim": "J"},
    {"q": "面对多线任务，我必须先梳理优先级并获得确认，才能安心执行。", "dim": "J"}
]

mbti_details = {
    "INTJ": {"role": "首席制度架构师 / CSO", "desc": "数据要素世界的“造物主”，致力于构建严密的数据治理公理体系。你坚信系统大于个人。", "tags": ["逻辑闭环", "顶层设计", "制度自信"]},
    "INTP": {"role": "风控模型专家 / 首席科学家", "desc": "穿透迷雾，寻找业务背后底层的逻辑漏洞与算力平衡。你是极客精神的代表。", "tags": ["黑客思维", "算法驱动", "极致解构"]},
    "ISTJ": {"role": "首席合规审查官 / 运营基石", "desc": "交易所的守夜人，你的名字本身就是安全、严谨、零失误的代名词。", "tags": ["绝对合规", "程序正义", "数据护法"]},
    "ESTJ": {"role": "业务统筹总监 / COO", "desc": "无可争议的项目推进器，擅长将复杂的国家政策转化为可落地的KPI体系。", "tags": ["统帅力", "结果主义", "流程大师"]},
    "INFJ": {"role": "产业生态智库 / 战略合伙人", "desc": "具备极强的行业共情能力，能精准预判数据流通对未来文明产生的深远变革。", "tags": ["远见卓识", "使命驱动", "人文视角"]},
    "INFP": {"role": "品牌价值主张官 / 文化引领", "desc": "数据背后的灵魂捕捉者，擅长构建不仅专业而且动人的数商生态故事。", "tags": ["感召力", "价值观构建", "组织粘合"]},
    "ENTJ": {"role": "市场开拓领军人 / 核心合伙人", "desc": "天生的掠夺者与建设者，在数据资源化、产品化的无人区中强势开路。", "tags": ["开疆拓土", "战略铁腕", "极速成交"]},
    "ENTP": {"role": "产品创新顾问 / 业务极客", "desc": "交易规则的调皮破坏者，致力于通过跨界思维寻找下一代交易范式。", "tags": ["模式创新", "辩才无碍", "思维跳变"]},
    "ENFJ": {"role": "数商成功与生态总监", "desc": "数交所的魅力中心，能通过卓越的共识构建能力，将竞争对手转化为盟友。", "tags": ["关系枢纽", "温情领导力", "利益协调"]},
    "ENFP": {"role": "资源链接大使 / 活动策划主管", "desc": "充满感染力的生态火苗，让每一场路演都变成数据要素市场的信仰充值。", "tags": ["无限创意", "跨界纽带", "热情驱动"]},
    "ISFJ": {"role": "高级行政主管 / 内部运营", "desc": "最坚韧的底层支点，于无声处通过极致细节支撑起整个平台的信誉。", "tags": ["利他主义", "执行力巅峰", "运营专家"]},
    "ESFJ": {"role": "商务关系主管 / 渠道主管", "desc": "超级连接器，擅长经营多维度的商务关系，是前台业务的最强润滑剂。", "tags": ["协作典范", "细节控制", "社会化支撑"]},
    "ISTP": {"role": "危机管理专家 / 技术压舱石", "desc": "数据底座的拆弹专家，只对事实和逻辑负责，是突发故障时的唯一指望。", "tags": ["极简实干", "危机直觉", "技术硬核"]},
    "ISFP": {"role": "视觉交互与品牌设计专家", "desc": "赋予枯燥数据以美学价值，致力于提升资产评估与路演的颜值与质感。", "tags": ["审美溢价", "感官叙事", "独立纯粹"]},
    "ESTP": {"role": "大客户成交官 / 谈判先锋", "desc": "数据交易的猎手，嗅觉极其灵敏，能捕捉到转瞬即逝的市场红利与空间。", "tags": ["现场感", "博弈高手", "结果收割"]},
    "ESFP": {"role": "公共关系与外联大使", "desc": "交易所形象代言人，天生具备将复杂的业务逻辑转化为大众传播话术的天赋。", "tags": ["表现力", "当下主义", "快乐源泉"]}
}

job_models = {
    "首席合规官 (CCO)": {"E": -2, "S": 5, "T": 5, "J": 5},
    "数商关系总监": {"E": 6, "S": 1, "T": -2, "J": 0},
    "数据产品架构师": {"E": 2, "S": 3, "T": 3, "J": 2},
    "战略发展专家": {"E": 0, "S": -4, "T": 4, "J": 1},
    "清算结算总监": {"E": -4, "S": 6, "T": 4, "J": 6}
}

# --- 4. 状态路由管理 ---
if 'started' not in st.session_state: st.session_state.started = False
if 'current_q' not in st.session_state: st.session_state.current_q = 0
if 'total_scores' not in st.session_state: st.session_state.total_scores = {"E": 0, "S": 0, "T": 0, "J": 0}
if 'start_time' not in st.session_state: st.session_state.start_time = None
if 'end_time' not in st.session_state: st.session_state.end_time = None

def start_assessment():
    st.session_state.started = True
    st.session_state.start_time = time.time()

def answer_clicked(val, dim):
    st.session_state.total_scores[dim] += (val - 3)
    st.session_state.current_q += 1
    if st.session_state.current_q == 40:
        st.session_state.end_time = time.time()

# --- 5. 渲染引擎 ---
if not st.session_state.started:
    # ====== 殿堂级封面页 ======
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 class='hero-title'>上海数据交易所<br>人才资产管理系统</h1>", unsafe_allow_html=True)
    st.markdown("<div class='hero-subtitle'>SDE ELITE DNA MATRIX v13.0</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='hero-desc'>
        <b>欢迎接入 SDE 核心神经元网络。</b><br><br>
        在数据要素化的高速演进中，系统规则与创新博弈并存。本终端基于前沿行为心理学与决策算力模型，旨在深度扫描您的<b>确权思维、合规直觉与生态构建潜能</b>。<br><br>
        这不是一次普通的问卷，这是您在数字经济浪潮中的<b>个人资产确权</b>。
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='start-btn'>", unsafe_allow_html=True)
    if st.button("启动核心测算终端 INIT_SYSTEM()", use_container_width=True):
        start_assessment()
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center; color:#475569; font-size:12px; margin-top:50px;'>内部授权使用 · 全程加密传输</div>", unsafe_allow_html=True)

elif st.session_state.current_q < 40:
    # ====== 高级互动答题页 ======
    q_data = questions[st.session_state.current_q]
    
    st.markdown("<div style='padding-top:20px;'></div>", unsafe_allow_html=True)
    st.progress((st.session_state.current_q + 1) / 40)
    st.markdown(f"<div style='text-align:right; font-size:12px; color:#00f3ff; margin-top:-10px; font-family:monospace;'>SCANNING: {st.session_state.current_q + 1} / 40</div>", unsafe_allow_html=True)
    
    st.markdown(f"<div style='margin: 40px 0 30px 0;'><h3 style='line-height:1.6; color:#ffffff !important; font-weight:600;'>{q_data['q']}</h3></div>", unsafe_allow_html=True)
    
    opts = [
        ("完全背离职业直觉", 1),
        ("较不符合习惯方式", 2),
        ("视具体业务场景而定", 3),
        ("比较符合决策风格", 4),
        ("精准复刻我的思维", 5)
    ]
    
    st.markdown("<div class='question-btn'>", unsafe_allow_html=True)
    for text, val in opts:
        if st.button(text, key=f"q_{st.session_state.current_q}_{val}"):
            answer_clicked(val, q_data['dim'])
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # ====== 降维打击级结果页 ======
    trigger_supernova() # 物理引擎爆炸
    
    res = st.session_state.total_scores
    mbti = ("E" if res["E"] >= 0 else "I") + ("S" if res["S"] >= 0 else "N") + ("T" if res["T"] >= 0 else "F") + ("J" if res["J"] >= 0 else "P")
    data = mbti_details.get(mbti)
    
    # 核心确权卡片
    st.markdown(f"""
    <div class="result-card">
        <div style="font-size:14px; color:#94a3b8; letter-spacing:4px; margin-bottom:15px;">基因序列解析完成</div>
        <div class="mbti-code">{mbti}</div>
        <div class="mbti-post">【 {data['role']} 】</div>
        <div class="mbti-desc">{data['desc']}</div>
        <div>
            {" ".join([f'<span class="cyber-tag">{t}</span>' for t in data['tags']])}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 交互式 3D 雷达图
    st.markdown("<div class='section-header'>🕸️ 核心算力拓扑矩阵 (可触控旋转)</div>", unsafe_allow_html=True)
    
    def get_intensity(score): return max(15, min(100, 50 + (score / 20 * 50)))
    val_E, val_I = get_intensity(res["E"]), 100 - get_intensity(res["E"])
    val_S, val_N = get_intensity(res["S"]), 100 - get_intensity(res["S"])
    val_T, val_F = get_intensity(res["T"]), 100 - get_intensity(res["T"])
    val_J, val_P = get_intensity(res["J"]), 100 - get_intensity(res["J"])
    
    categories = ['外向驱动(E)', '实务落地(S)', '理性风控(T)', '秩序掌控(J)', '内向沉思(I)', '宏观直觉(N)', '感性共鸣(F)', '灵活适配(P)']
    values = [val_E, val_S, val_T, val_J, val_I, val_N, val_F, val_P]
    values_loop = values + [values[0]]
    categories_loop = categories + [categories[0]]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_loop, theta=categories_loop, fill='toself',
        fillcolor='rgba(0, 243, 255, 0.25)', line=dict(color='#00f3ff', width=3),
        marker=dict(color='#ffd700', size=8, symbol='diamond')
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, showticklabels=False, range=[0, 100], gridcolor='rgba(0, 243, 255, 0.1)'),
            angularaxis=dict(tickfont=dict(color='#e2e8f0', size=14), linecolor='rgba(0, 243, 255, 0.3)', gridcolor='rgba(0, 243, 255, 0.2)')
        ),
        showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=30, b=30)
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # 潜意识时间追踪
    st.markdown("<div class='section-header'>⏱️ 潜意识决策引擎分析</div>", unsafe_allow_html=True)
    time_taken = st.session_state.end_time - st.session_state.start_time
    if time_taken < 100:
        s_tag, s_desc, color = "高频量化并发 (极速直觉)", "您的潜意识引擎处于超频状态。擅长在瞬息万变的交易盘口进行瞬时压迫性决策，具有极高的直觉穿透力。", "#ff00ff"
    elif time_taken < 220:
        s_tag, s_desc, color = "均衡算力调度 (敏捷研判)", "直觉与逻辑的完美平衡。能在有限信息下快速建立风控模型，是标准数据资产化项目中最稳健的决策节拍。", "#00f3ff"
    else:
        s_tag, s_desc, color = "深度逻辑推演 (战略风控)", "决策引擎处于深潜状态。擅长处理极其庞杂的合规变量与底层架构规划，绝不盲从，是顶层制度设计的天然基石。", "#ffd700"
        
    st.markdown(f"""
    <div style='background:rgba(15, 23, 42, 0.8); border-left: 4px solid {color}; padding:20px; border-radius:12px; box-shadow:0 10px 20px rgba(0,0,0,0.3);'>
        <div style='color:{color}; font-size:18px; font-weight:bold; margin-bottom:10px;'>{s_tag}</div>
        <div style='color:#e2e8f0; font-size:14px; line-height:1.6;'>测算耗时：{int(time_taken)} 秒<br><br>{s_desc}</div>
    </div>
    """, unsafe_allow_html=True)

    # 链上确权名片 (极其装逼)
    st.markdown("<div class='section-header'>⛓️ 资产确权社交凭证</div>", unsafe_allow_html=True)
    hash_code = hex(hash(mbti + str(time_taken) + str(res["E"])))[-10:].upper()
    share_card = f"""【SDE 全息人才资产确权凭证】
======================
◈ 基因序列：{mbti}
◈ 系统职衔：{data['role']}
◈ 核心算力：{' · '.join(data['tags'])}
◈ 决策频段：{s_tag.split(' ')[0]}
======================
确权哈希：0x{hash_code}E9
（来自SDE内部测算终端）"""
    st.code(share_card, language="text")
    st.caption("☝️ 长按代码框复制，发送至微信宣告你的数字主权。")

    # 底部重启
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<div class='start-btn'>", unsafe_allow_html=True)
    if st.button("重启系统 RESET_TERMINAL()", use_container_width=True):
        st.session_state.started = False
        st.session_state.current_q = 0
        st.session_state.total_scores = {"E": 0, "S": 0, "T": 0, "J": 0}
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- 7. 专属高亮版权 ---
st.markdown("""
    <div style='text-align:center; margin-top:60px; margin-bottom:20px; font-family:monospace;'>
        <div style='color:#00f3ff; font-size:11px; opacity:0.6; letter-spacing:2px; margin-bottom:8px;'>
            POWERED BY DATA ELEMENT ENGINE
        </div>
        <div style='color:#ffd700; font-size:13px; font-weight:900; letter-spacing:3px; text-shadow:0 0 15px rgba(255,215,0,0.8);'>
            © 版权归属无名逆流所有
        </div>
    </div>
""", unsafe_allow_html=True)
