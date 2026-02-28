import streamlit as st
import pandas as pd
import random
import time
import plotly.graph_objects as go

# --- 1. 页面与官方主题强制配置 ---
st.set_page_config(
    page_title="SDE 数据要素菁英图谱",
    page_icon="🌌",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. 注入“光污染”赛博朋克级 UI 样式 & 烟花特效 ---
st.markdown("""
<style>
    /* 全局赛博深空背景 */
    [data-testid="stAppViewContainer"] { 
        background-color: #0b101e !important; 
        background-image: radial-gradient(circle at 50% 0%, #152336 0%, #0b101e 70%) !important;
    }
    
    /* 强制文本颜色 */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp p, .stApp span, .stApp div {
        color: #e2e8f0;
    }
    
    /* 光污染标题 */
    .stApp h1 { 
        color: #00f3ff !important; 
        text-shadow: 0 0 10px rgba(0,243,255,0.6), 0 0 20px rgba(0,243,255,0.4); 
        font-weight: 900 !important; text-align: center; margin-bottom: 5px; letter-spacing: 2px;
    }
    
    /* 进度条霓虹光效 */
    .stProgress > div > div > div > div {
        background-image: linear-gradient(90deg, #00f3ff, #ff00ff) !important;
        box-shadow: 0 0 15px rgba(0, 243, 255, 0.8) !important;
    }

    /* 选项按钮：毛玻璃 + 霓虹边框 */
    div.stButton > button {
        width: 100% !important; min-height: 65px !important; border-radius: 12px !important;
        background: rgba(20, 30, 48, 0.6) !important;
        border: 1px solid rgba(0, 243, 255, 0.3) !important;
        color: #e2e8f0 !important; font-size: 15px !important; text-align: left !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: inset 0 0 10px rgba(0, 243, 255, 0.05) !important;
        white-space: normal !important; padding: 12px 20px !important; line-height: 1.6 !important;
    }
    div.stButton > button:hover { 
        border-color: #00f3ff !important; background: rgba(0, 243, 255, 0.1) !important;
        box-shadow: 0 0 15px rgba(0, 243, 255, 0.4) !important;
        color: #ffffff !important; transform: translateY(-2px);
    }
    
    /* 结果大卡片：全息终端质感 */
    .result-card {
        padding: 35px 20px; border-radius: 24px; 
        background: linear-gradient(145deg, rgba(20, 30, 48, 0.8), rgba(11, 16, 30, 0.9));
        border: 1px solid rgba(255, 215, 0, 0.4);
        text-align: center; 
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.15);
        margin-bottom: 25px; position: relative; overflow: hidden;
    }
    .mbti-code { font-size: 78px; font-weight: 900; color: #ffd700 !important; line-height: 1; letter-spacing: 2px; text-shadow: 0 0 20px rgba(255, 215, 0, 0.6); margin: 10px 0;}
    .mbti-post { font-size: 24px; font-weight: bold; color: #00f3ff !important; margin: 12px 0; text-shadow: 0 0 10px rgba(0, 243, 255, 0.5);}
    
    /* 解析板块与标签 */
    .section-header { font-size: 18px; font-weight: 700; color: #00f3ff !important; border-left: 5px solid #ff00ff; padding-left: 12px; margin: 25px 0 15px 0; text-shadow: 0 0 8px rgba(0,243,255,0.4); }
    .expert-box { background: rgba(255,255,255,0.03); padding: 20px; border-radius: 12px; border: 1px solid rgba(0, 243, 255, 0.2); box-shadow: inset 0 0 15px rgba(0,0,0,0.5); margin-bottom: 15px; }
    .cyber-tag { background: rgba(0, 243, 255, 0.1); color: #00f3ff !important; border: 1px solid #00f3ff; padding: 4px 12px; border-radius: 4px; font-size: 12px; font-weight: 700; margin: 3px; display: inline-block; text-shadow: 0 0 5px rgba(0,243,255,0.5); }

    /* 烟花特效 */
    .firework-666 { position: fixed; font-weight: 900; z-index: 9999; pointer-events: none; color: transparent; -webkit-text-stroke: 1px #00f3ff; text-shadow: 0 0 20px #00f3ff, 0 0 40px #ff00ff; animation: explode 2.5s cubic-bezier(0.25, 1, 0.5, 1) forwards;}
    @keyframes explode { 0% { bottom: 20%; left: 50%; transform: scale(0.1) rotate(0deg); opacity: 1; } 100% { bottom: var(--endY); left: var(--endX); transform: scale(var(--endScale)) rotate(var(--endRot)); opacity: 0; filter: hue-rotate(360deg); } }
</style>
""", unsafe_allow_html=True)

def trigger_cyber_fireworks():
    html_str = ""
    for _ in range(60): 
        endX, endY = f"{random.randint(5, 95)}%", f"{random.randint(60, 110)}%"
        scale, rot, delay = random.uniform(1.0, 3.5), random.randint(-180, 180), random.uniform(0, 1.2)
        html_str += f'<div class="firework-666" style="--endX:{endX}; --endY:{endY}; --endScale:{scale}; --endRot:{rot}deg; animation-delay: {delay}s; font-size: 24px;">666</div>'
    st.markdown(html_str, unsafe_allow_html=True)

# --- 3. 40 道专家题库 (精简呈现，执行全量逻辑) ---
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
    "INTJ": {"role": "首席制度架构师 / CSO", "desc": "数据要素世界的“造物主”，构建严密的数据治理公理体系。", "tags": ["逻辑闭环", "顶层设计", "制度自信"]},
    "INTP": {"role": "风控模型专家 / 首席科学家", "desc": "穿透迷雾，寻找业务背后底层的逻辑漏洞与算力平衡。", "tags": ["黑客思维", "算法驱动", "极致解构"]},
    "ISTJ": {"role": "首席合规审查官 / 运营基石", "desc": "交易所的守夜人，名字本身就是安全、严谨、零失误的代名词。", "tags": ["绝对合规", "程序正义", "数据护法"]},
    "ESTJ": {"role": "业务统筹总监 / COO", "desc": "项目推进器，将复杂政策转化为可落地的KPI体系。", "tags": ["统帅力", "结果主义", "流程大师"]},
    "INFJ": {"role": "产业生态智库 / 战略合伙人", "desc": "具备极强的行业共情能力，预判数据流通带来的深远变革。", "tags": ["远见卓识", "使命驱动", "人文视角"]},
    "INFP": {"role": "品牌价值主张官 / 文化引领", "desc": "数据背后的灵魂捕捉者，构建动人的数商生态故事。", "tags": ["感召力", "价值观构建", "组织粘合"]},
    "ENTJ": {"role": "市场开拓领军人 / 核心合伙人", "desc": "天生的掠夺者与建设者，在数据产品化无人区中强势开路。", "tags": ["开疆拓土", "战略铁腕", "极速成交"]},
    "ENTP": {"role": "产品创新顾问 / 业务极客", "desc": "交易规则的创新颠覆者，致力于寻找下一代交易范式。", "tags": ["模式创新", "辩才无碍", "思维跳变"]},
    "ENFJ": {"role": "数商成功与生态总监", "desc": "交易所的魅力中心，将竞争对手转化为战略盟友。", "tags": ["关系枢纽", "温情领导力", "利益协调"]},
    "ENFP": {"role": "资源链接大使 / 活动策划主管", "desc": "生态火苗，让每一场路演都变成数据要素市场的信仰充值。", "tags": ["无限创意", "跨界纽带", "热情驱动"]},
    "ISFJ": {"role": "高级行政主管 / 内部运营", "desc": "最坚韧的底层支点，通过极致细节支撑起整个平台的信誉。", "tags": ["利他主义", "执行力巅峰", "运营专家"]},
    "ESFJ": {"role": "商务关系主管 / 渠道主管", "desc": "超级连接器，擅长经营多维商务关系，业务的润滑剂。", "tags": ["协作典范", "细节控制", "社会化支撑"]},
    "ISTP": {"role": "危机管理专家 / 技术压舱石", "desc": "数据底座拆弹专家，对事实负责，故障时的唯一指望。", "tags": ["极简实干", "危机直觉", "技术硬核"]},
    "ISFP": {"role": "视觉交互与品牌设计专家", "desc": "赋予数据美学价值，提升资产路演的颜值与质感。", "tags": ["审美溢价", "感官叙事", "独立纯粹"]},
    "ESTP": {"role": "大客户成交官 / 谈判先锋", "desc": "数据交易的猎手，捕捉转瞬即逝的市场红利与空间。", "tags": ["现场感", "博弈高手", "结果收割"]},
    "ESFP": {"role": "公共关系与外联大使", "desc": "交易所形象代言人，将复杂逻辑转化为传播话术的天赋。", "tags": ["表现力", "当下主义", "快乐源泉"]}
}

# --- 5. 状态管理与时间追踪 ---
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'total_scores' not in st.session_state:
    st.session_state.total_scores = {"E": 0, "S": 0, "T": 0, "J": 0}
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'end_time' not in st.session_state:
    st.session_state.end_time = None

def answer_clicked(val, dim):
    if st.session_state.current_q == 0:
        st.session_state.start_time = time.time()  # 记录潜意识决策开始瞬间
    st.session_state.total_scores[dim] += (val - 3)
    st.session_state.current_q += 1
    if st.session_state.current_q == 40:
        st.session_state.end_time = time.time()  # 记录完成瞬间

# --- 6. 交互界面渲染 ---
st.markdown("<h1>SDE 全息人才图谱</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#00f3ff; font-size:12px; margin-top:-5px; letter-spacing:1px; opacity:0.8;'>DATA ELEMENT ELITE MATRIX v12.0</p>", unsafe_allow_html=True)

if st.session_state.current_q < len(questions):
    q_data = questions[st.session_state.current_q]
    st.progress((st.session_state.current_q + 1) / 40)
    st.markdown(f"<div style='text-align:right; font-size:11px; color:#00f3ff; margin-top:-10px; opacity:0.7;'>神经元扫描：{st.session_state.current_q + 1} / 40</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='margin: 30px 0; min-height:85px;'><h4 style='line-height:1.6; font-size:17px; color:#fff !important;'>{q_data['q']}</h4></div>", unsafe_allow_html=True)
    
    opts = [("完全背离职业直觉", 1), ("较不符合习惯方式", 2), ("视具体业务场景而定", 3), ("比较符合决策风格", 4), ("精准复刻我的思维", 5)]
    for text, val in opts:
        if st.button(text, key=f"q_{st.session_state.current_q}_{val}"):
            answer_clicked(val, q_data['dim'])
            st.rerun()
else:
    # 触发赛博烟花
    trigger_cyber_fireworks()
    
    res = st.session_state.total_scores
    mbti = ("E" if res["E"] >= 0 else "I") + ("S" if res["S"] >= 0 else "N") + ("T" if res["T"] >= 0 else "F") + ("J" if res["J"] >= 0 else "P")
    data = mbti_details.get(mbti)
    
    # 核心结果
    st.markdown(f"""
    <div class="result-card">
        <div style="font-size:13px; color:#ffd700; letter-spacing:3px; margin-bottom:15px; opacity:0.8;">核心资产解码完成</div>
        <div class="mbti-code">{mbti}</div>
        <div class="mbti-post">【 {data['role']} 】</div>
        <p style="color:#cbd5e1 !important; font-size:15px; padding:0 10px;">{data['desc']}</p>
        <div style="margin-top:20px;">
            {" ".join([f'<span class="cyber-tag">{t}</span>' for t in data['tags']])}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- 新增装逼功能 1：3D 交互式动态雷达图 ---
    st.markdown("<div class='section-header'>🕸️ 核心算力拓扑矩阵 (可触控旋转)</div>", unsafe_allow_html=True)
    
    def get_intensity(score): return max(10, min(100, 50 + (score / 20 * 50)))
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
        fillcolor='rgba(0, 243, 255, 0.25)', line=dict(color='#00f3ff', width=2),
        marker=dict(color='#ffd700', size=6, symbol='diamond')
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, showticklabels=False, range=[0, 100], gridcolor='rgba(0, 243, 255, 0.1)'),
            angularaxis=dict(tickfont=dict(color='#00f3ff', size=13), linecolor='rgba(0, 243, 255, 0.3)', gridcolor='rgba(0, 243, 255, 0.15)')
        ),
        showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=30, r=30, t=20, b=20)
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # --- 新增装逼功能 2：决策算力速率追踪 ---
    st.markdown("<div class='section-header'>⏱️ 潜意识决策引擎分析</div>", unsafe_allow_html=True)
    time_taken = st.session_state.end_time - st.session_state.start_time
    if time_taken < 100:
        speed_tag, speed_desc = "高频量化并发 (极速直觉)", "您的潜意识决策引擎处于超频状态。擅长在瞬息万变的交易盘口进行瞬时压迫性决策，具有极高的直觉穿透力。"
        color = "#ff00ff"
    elif time_taken < 220:
        speed_tag, speed_desc = "均衡算力调度 (敏捷研判)", "直觉与逻辑的完美平衡。能在有限信息下快速建立风控模型，是标准数据资产化项目中最稳健的决策节拍。"
        color = "#00f3ff"
    else:
        speed_tag, speed_desc = "深度逻辑推演 (战略风控)", "决策引擎处于深潜状态。擅长处理极其庞杂的合规变量与底层架构规划，绝不盲从，是顶层制度设计的天然基石。"
        color = "#ffd700"
        
    st.markdown(f"""
    <div class='expert-box' style='border-left: 4px solid {color};'>
        <div style='color:{color}; font-size:16px; font-weight:bold; margin-bottom:8px;'>引擎状态：{speed_tag}</div>
        <div style='color:#94a3b8; font-size:13px;'>响应耗时：{int(time_taken)} 秒<br><br>{speed_desc}</div>
    </div>
    """, unsafe_allow_html=True)

    # 底部专属卡片
    st.markdown("<div class='section-header'>🪪 终端社交识别卡</div>", unsafe_allow_html=True)
    share_card = f"""【SDE 全息人才图谱解码】
======================
◈ 基因序列：{mbti}
◈ 系统职衔：{data['role']}
◈ 核心算力：{' · '.join(data['tags'])}
◈ 引擎频段：{speed_tag.split(' ')[0]}
======================
解码数据价值，定义要素未来
（来自SDE内部测算终端）"""
    st.code(share_card, language="text")

    if st.button("🔄 断开连接并重启系统", use_container_width=True):
        st.session_state.current_q = 0
        st.session_state.total_scores = {"E": 0, "S": 0, "T": 0, "J": 0}
        st.session_state.start_time = None
        st.session_state.end_time = None
        st.rerun()

# --- 7. 版权声明 ---
st.markdown("""
    <div style='text-align:center; margin-top:60px; margin-bottom:20px; font-family:monospace;'>
        <div style='color:#00f3ff; font-size:10px; opacity:0.6; letter-spacing:1px; margin-bottom:5px;'>
            POWERED BY DATA ELEMENT ENGINE
        </div>
        <div style='color:#ffd700; font-size:12px; font-weight:bold; letter-spacing:2px; text-shadow:0 0 10px rgba(255,215,0,0.5);'>
            © 版权归属无名逆流所有
        </div>
    </div>
""", unsafe_allow_html=True)
