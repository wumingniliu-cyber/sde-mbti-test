import streamlit as st
import pandas as pd
import random
import time
import math
import hashlib
import plotly.graph_objects as go

# --- 1. 页面与全局配置 ---
st.set_page_config(
    page_title="SDE 核心人才资产引擎",
    page_icon="💠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. 靶向级 UI 引擎注入 (彻底抹杀白色框，重塑赛博全息感) ---
st.markdown("""
<style>
    /* 1. 强制深空背景 */
    .stApp { background-color: #030712 !important; }
    [data-testid="stAppViewContainer"] { 
        background-color: transparent !important;
        background-image: 
            radial-gradient(circle at 50% 0%, #0f172a 0%, #030712 80%),
            linear-gradient(0deg, rgba(0,243,255,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0,243,255,0.03) 1px, transparent 1px) !important;
        background-size: 100% 100%, 30px 30px, 30px 30px !important;
    }
    
    .stMarkdown, p, span, h1, h2, h3, h4, li, div { color: #f8fafc !important; }
    
    /* 2. 标题与高定光感 */
    .hero-title { 
        font-size: 40px !important; font-weight: 900 !important; text-align: center; 
        color: #ffffff !important; letter-spacing: 3px; margin-bottom: 5px;
        text-shadow: 0 0 20px rgba(0,243,255,0.8), 0 0 40px rgba(0,243,255,0.5);
    }
    .hero-subtitle { text-align: center; color: #00f3ff !important; font-size: 13px; letter-spacing: 5px; opacity: 0.9; margin-bottom: 30px; font-family: monospace; }
    
    /* ========================================================
       3. 彻底重构选项按钮 (再也不会出现白色框！)
       ======================================================== */
    button[data-testid="baseButton-secondary"] {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.95), rgba(2, 6, 23, 0.95)) !important; 
        border: 1px solid rgba(0, 243, 255, 0.3) !important; 
        border-left: 4px solid rgba(0, 243, 255, 0.6) !important; /* 赛博侧边能量条 */
        border-radius: 8px !important; min-height: 65px !important; width: 100% !important;
        padding: 12px 20px !important; text-align: left !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.8), inset 0 0 10px rgba(0,243,255,0.05) !important; 
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        margin-bottom: 8px !important;
    }
    button[data-testid="baseButton-secondary"] p { 
        color: #e2e8f0 !important; font-size: 15px !important; line-height: 1.6 !important; 
        white-space: normal !important; font-weight: 500 !important; letter-spacing: 1px;
    }
    /* 悬停态：荧光爆发与右移 */
    button[data-testid="baseButton-secondary"]:hover { 
        background: linear-gradient(90deg, rgba(0, 243, 255, 0.2) 0%, rgba(15, 23, 42, 0.9) 100%) !important; 
        border-color: #00f3ff !important; border-left: 6px solid #00f3ff !important;
        box-shadow: 0 0 25px rgba(0,243,255,0.3), inset 0 0 15px rgba(0,243,255,0.2) !important; 
        transform: translateX(6px) !important; 
    }
    button[data-testid="baseButton-secondary"]:hover p { color: #ffffff !important; text-shadow: 0 0 8px #00f3ff; }
    button[data-testid="baseButton-secondary"]:active { transform: scale(0.98) !important; }

    /* 操作按钮 (Primary) */
    button[data-testid="baseButton-primary"] {
        background: linear-gradient(90deg, #00f3ff, #0088ff) !important; border: none !important; border-radius: 8px !important;
        min-height: 65px !important; width: 100% !important; box-shadow: 0 0 25px rgba(0,243,255,0.4) !important; transition: all 0.2s !important;
    }
    button[data-testid="baseButton-primary"] p { color: #030712 !important; font-weight: 900 !important; font-size: 18px !important; letter-spacing: 2px !important; }
    button[data-testid="baseButton-primary"]:hover { transform: translateY(-2px) scale(1.02) !important; box-shadow: 0 0 40px rgba(0,243,255,0.8) !important; }
    
    /* 4. 进度条发光 */
    .stProgress > div > div > div > div { background-image: linear-gradient(90deg, #00f3ff, #ff00ff) !important; box-shadow: 0 0 15px rgba(0, 243, 255, 0.8) !important; }

    /* 5. 结果视窗与协同赋能框 */
    .result-card {
        padding: 40px 25px; border-radius: 16px; background-color: #0b1120 !important; 
        border: 1px solid rgba(255,215,0,0.3); border-top: 6px solid #ffd700; 
        text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.9), inset 0 0 30px rgba(255,215,0,0.05); margin-bottom: 30px;
    }
    .mbti-code { font-size: 85px; font-weight: 900; color: #ffd700 !important; line-height: 1.1; letter-spacing: 2px; text-shadow: 0 0 30px rgba(255,215,0,0.5); margin: 0;}
    .mbti-post { font-size: 22px; font-weight: bold; color: #00f3ff !important; margin: 15px 0; }
    
    .synergy-box { 
        background: rgba(16, 185, 129, 0.05); border-left: 4px solid #10b981; 
        padding: 20px; border-radius: 8px; font-size: 14px; line-height: 1.7; 
        color: #e2e8f0 !important; border: 1px solid rgba(16, 185, 129, 0.2); 
        box-shadow: inset 0 0 20px rgba(16,185,129,0.05); margin: 15px 0 25px 0;
    }
    .synergy-title { color: #34d399 !important; font-weight: bold; font-size: 15px; margin-bottom: 8px; font-family: monospace;}

    /* 超新星炸裂动画 */
    .firework-center { position: fixed; top: 50%; left: 50%; z-index: 99999; pointer-events: none; font-weight: 900; font-family: monospace; color: transparent; -webkit-text-stroke: 1.5px #00f3ff; text-shadow: 0 0 20px #00f3ff, 0 0 40px #ffffff; animation: supernova 2s cubic-bezier(0.1, 0.9, 0.2, 1) forwards; }
    @keyframes supernova { 0% { transform: translate(-50%, -50%) scale(0.1) rotate(0deg); opacity: 1; filter: brightness(2); } 20% { opacity: 1; filter: brightness(3); } 100% { transform: translate(calc(-50% + var(--tx)), calc(-50% + var(--ty))) scale(var(--s)) rotate(var(--rot)); opacity: 0; filter: brightness(1) hue-rotate(180deg); } }
</style>
""", unsafe_allow_html=True)

def trigger_supernova():
    html_str = ""
    symbols = ["666", "1", "0", "DATA", "SDE"]
    for _ in range(80): 
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(300, 1200)
        tx, ty = distance * math.cos(angle), distance * math.sin(angle)
        scale = random.uniform(1.2, 3.5)
        rot = random.randint(-360, 360)
        delay = random.uniform(0, 0.2)
        text = random.choice(symbols)
        html_str += f'<div class="firework-center" style="--tx:{tx}px; --ty:{ty}px; --s:{scale}; --rot:{rot}deg; animation-delay:{delay}s; font-size:{random.randint(18, 32)}px;">{text}</div>'
    st.markdown(html_str, unsafe_allow_html=True)

# --- 3. 题库库 ---
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

# --- 4. 画像数据库 (高定职场赋能版) ---
mbti_details = {
    "INTJ": {"role": "首席制度架构师 / CSO", "desc": "数据要素世界的“架构师”，致力于构建严密的数据治理公理体系。", "tags": ["逻辑闭环", "顶层设计", "制度自信"], "partner": "ENTJ (强效执行节点) / INTP (极客算法节点)", "advice": "在构建宏大的底层规则架构时，请适当为业务部门预留“沙盒容错”空间；倾听一线的非结构化反馈，能让你的制度更具生命力。"},
    "INTP": {"role": "风控模型专家 / 首席科学家", "desc": "穿透迷雾，寻找业务背后底层的逻辑漏洞与算力平衡。你是极客精神的代表。", "tags": ["黑客思维", "算法驱动", "极致解构"], "partner": "INTJ (框架锚定节点) / ENTP (模式发散节点)", "advice": "尝试将你极其高维的理论模型降维封装，形成非技术人员也能看懂的业务操作手册，让优秀的逻辑转化为具体的生产力。"},
    "ISTJ": {"role": "首席合规审查官 / 运营基石", "desc": "交易所的守夜人，你的名字本身就是安全、严谨、零失误的代名词。", "tags": ["绝对合规", "程序正义", "数据护法"], "partner": "ESTJ (业务推进节点) / ISFJ (后勤保障节点)", "advice": "在死守数据合规底线的同时，面对狂飙突进的创新产品，试着用“如何让它合规地上架”来指导业务，成为创新的护航者。"},
    "ESTJ": {"role": "业务统筹总监 / COO", "desc": "无可争议的项目推进器，擅长将复杂的国家政策转化为可落地的KPI体系。", "tags": ["统帅力", "结果主义", "流程大师"], "partner": "ISTJ (品控审查节点) / ISTP (危机拆弹节点)", "advice": "在推进高压任务时，适度向团队释放情绪价值。一支拥有高凝聚力和信任感的团队，往往比单纯的数字化目标走得更稳健。"},
    "INFJ": {"role": "产业生态智库 / 战略合伙人", "desc": "具备极强的行业共情能力，能精准预判数据流通对未来文明产生的深远变革。", "tags": ["远见卓识", "使命驱动", "人文视角"], "partner": "ENFJ (共识布道节点) / ENFP (火种传播节点)", "advice": "学会用精确的财务数据、合规条文来锚定你的宏大产业愿景。将“先知感知”转化为具体的业务政策专报，提升落地的说服力。"},
    "INFP": {"role": "品牌价值主张官 / 文化引领", "desc": "数据背后的灵魂捕捉者，擅长构建不仅专业而且动人的数商生态故事。", "tags": ["感召力", "价值观构建", "组织粘合"], "partner": "ENFJ (外部护航节点) / ISFP (美学交互节点)", "advice": "在跨部门协同博弈中，学会熟练利用预算工具和业务导向来捍卫你的核心价值主张，将柔性文化转化为硬性的机构资产。"},
    "ENTJ": {"role": "市场开拓领军人 / 核心合伙人", "desc": "天生的建设者，在数据资源化、产品化的无人区中展现极强的破局能力。", "tags": ["开疆拓土", "战略铁腕", "极速成交"], "partner": "INTJ (战略智囊节点) / ISTP (技术攻坚节点)", "advice": "在极速开疆拓土时，请时刻保持与中台合规团队的数据同步。有时放慢半拍听听风控建议，能让你避开隐蔽的系统性风险。"},
    "ENTP": {"role": "产品创新顾问 / 业务极客", "desc": "交易规则的敏锐挑战者，致力于通过跨界思维寻找下一代交易范式。", "tags": ["模式创新", "辩才无碍", "思维跳变"], "partner": "INTP (逻辑验证节点) / ESTP (市场收割节点)", "advice": "适当收敛发散思维，选择一个极具潜力的创新点（如特定数据产权凭证），深度闭环跟进至最终交付，用结果验证你的前瞻性。"},
    "ENFJ": {"role": "数商成功与生态总监", "desc": "数交所的魅力中心，能通过卓越的共识构建能力，将竞争方聚拢为生态盟友。", "tags": ["关系枢纽", "温情领导力", "利益协调"], "partner": "INFJ (深度研究节点) / ESFJ (落地协同节点)", "advice": "在协调多方利益分配时，大胆引入客观的量化算法与刚性指标，确保“生态和谐”建立在牢不可破的规则基石之上。"},
    "ENFP": {"role": "资源链接大使 / 活动策划", "desc": "充满感染力的生态火苗，让每一场路演都变成数据要素市场的信仰共识。", "tags": ["无限创意", "跨界纽带", "热情驱动"], "partner": "INFJ (导航纠偏节点) / INTJ (架构落地节点)", "advice": "引入严密的日程表与里程碑管理。将你天马行空的生态创意，转化为可追踪的业务转化漏斗，大幅提升创新的商业核算价值。"},
    "ISFJ": {"role": "高级行政主管 / 内部运营", "desc": "最坚韧的底层支点，于无声处通过极致细节支撑起整个平台的专业信誉。", "tags": ["利他主义", "执行力巅峰", "运营专家"], "partner": "ESFJ (对外链接节点) / ISTJ (品控审核节点)", "advice": "在完美支撑中后台高速运转之余，尝试主动提出针对现有冗余流程的优化提案。你的实操经验极具价值，应当被更多人看见。"},
    "ESFJ": {"role": "商务关系主管 / 渠道主管", "desc": "超级连接器，擅长经营多维度的商务关系，是前台业务的最强润滑剂。", "tags": ["协作典范", "细节控制", "社会化支撑"], "partner": "ISFJ (精细支持节点) / ESTJ (宏观决策节点)", "advice": "在维护复杂商务生态时，建立更独立的风险评估过滤网，在照顾合作方诉求的同时，保持对业务底线的绝对清醒。"},
    "ISTP": {"role": "危机管理专家 / 技术压舱石", "desc": "数据底座的实干极客，只对事实和逻辑负责，是突发故障时的定海神针。", "tags": ["极简实干", "危机直觉", "技术硬核"], "partner": "ESTP (前线实战节点) / INTP (算法优化节点)", "advice": "尝试将你极度内隐的危机处理经验，沉淀为可视化的预案文档。打破技术沟通壁垒，将个人的技术赋能给整个团队系统。"},
    "ISFP": {"role": "视觉交互与品牌设计专家", "desc": "赋予枯燥数据以美学价值，致力于提升资产评估与路演的颜值与专业质感。", "tags": ["审美溢价", "感官叙事", "独立纯粹"], "partner": "ESFP (公众表达节点) / INFP (共情叙事节点)", "advice": "在追求数字展示的美学溢价时，适度增加对核心业务逻辑和底层交易规则的理解，这会让你的作品拥有直击商业痛点的力量。"},
    "ESTP": {"role": "大客户成交官 / 谈判先锋", "desc": "数据交易的敏锐猎手，能极快捕捉到瞬息万变的市场红利与应用空间。", "tags": ["现场感", "博弈高手", "结果收割"], "partner": "ISTP (底层兜底节点) / ENTJ (战略统筹节点)", "advice": "在捕捉市场瞬时机遇、展现高效行动力时，务必将前置合规审查纳入你的操作雷达之内，为强劲的业务冲刺装上安全的制动阀。"},
    "ESFP": {"role": "公共关系与外联大使", "desc": "交易所形象代言人，天生具备将复杂的业务逻辑转化为大众传播话术的天赋。", "tags": ["表现力", "当下主义", "快乐源泉"], "partner": "ISFP (视觉美学节点) / ENFP (创意破局节点)", "advice": "花时间深潜研究数据要素的底层逻辑与政策文件。将你的绝佳表现力建立在扎实的产业根基上，形成无可替代的权威影响力。"}
}

job_models = {
    "合规风控官": {"E": -2, "S": 5, "T": 5, "J": 5},
    "数商生态总监": {"E": 6, "S": 1, "T": -2, "J": 0},
    "数据产品专家": {"E": 2, "S": 3, "T": 3, "J": 2},
    "行业战略智库": {"E": 0, "S": -4, "T": 4, "J": 1},
    "清算结算骨干": {"E": -4, "S": 6, "T": 4, "J": 6}
}

# --- 5. 状态路由管理 ---
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

# --- 6. 渲染引擎 ---
if not st.session_state.started:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 class='hero-title'>上海数据交易所<br>人才图谱全息引擎</h1>", unsafe_allow_html=True)
    st.markdown("<div class='hero-subtitle'>▶ SDE MATRIX V18.0_READY</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(0,243,255,0.4); padding: 25px; border-radius: 12px; font-family: monospace; font-size: 14px; color: #e2e8f0; box-shadow: inset 0 0 20px rgba(0,243,255,0.1), 0 10px 30px rgba(0,0,0,0.8); margin-bottom: 40px;'>
        <span style='color:#94a3b8;'>[SYSTEM]</span> Establishing secure connection to SDE Core...<br>
        <span style='color:#94a3b8;'>[SYSTEM]</span> Loading Capability Matrix Algorithm... <span style='color:#00f3ff;'>[OK]</span><br>
        <span style='color:#10b981;'>[MODULE]</span> Initializing Synergy Network...<br><br>
        <span style='color:#ffffff; font-size: 15px; font-family: sans-serif; line-height: 1.8;'>在数据要素化的高速演进中，业务创新与底线合规并存。本终端将深度扫描您的<b>底层能力雷达、决策模型与生态协同潜能</b>。请凭职场第一直觉响应指令。</span>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("▶ 启动图谱解析引擎", type="primary", use_container_width=True):
        start_assessment()
        st.rerun()
    
    st.markdown("<div style='text-align:center; color:#475569; font-size:12px; margin-top:50px;'>END-TO-END ENCRYPTED · SDE INTERNAL</div>", unsafe_allow_html=True)

elif st.session_state.current_q < 40:
    # ====== 新增亮点：全息数据块 HUD 答题界面 ======
    q_data = questions[st.session_state.current_q]
    
    # 根据维度生成高逼格模块名
    dim_map = {"E": "生态节点拓扑 (NODE_SYNERGY)", "S": "资产颗粒存证 (ASSET_GRANULARITY)", "T": "交易共识逻辑 (LOGIC_CONSENSUS)", "J": "架构秩序引擎 (SYS_GOVERNANCE)"}
    module_name = dim_map.get(q_data['dim'], "特征算力提取 (CORE_EXTRACTION)")
    
    # 生成动态校验哈希
    dynamic_hash = hashlib.sha256(f"{q_data['q']}{time.time()}".encode()).hexdigest()[:10].upper()
    
    st.markdown("<div style='padding-top:10px;'></div>", unsafe_allow_html=True)
    st.progress((st.session_state.current_q + 1) / 40)
    
    # 极客感 HUD 题框
    st.markdown(f"""
    <div style='background: rgba(2, 6, 23, 0.8); border: 1px solid rgba(0, 243, 255, 0.4); border-radius: 12px; padding: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.5), inset 0 0 15px rgba(0, 243, 255, 0.05); margin-top: 15px; margin-bottom: 25px; border-left: 5px solid #00f3ff;'>
        <div style='display:flex; justify-content:space-between; font-family:monospace; color:#00f3ff; font-size:12px; margin-bottom:15px; border-bottom: 1px solid rgba(0,243,255,0.2); padding-bottom:10px;'>
            <span>▶ MODULE: {module_name}</span>
            <span>BLOCK: 0x{dynamic_hash}</span>
        </div>
        <div style='font-size: 18px; color: #ffffff; line-height: 1.6; font-weight: bold;'>
            {q_data['q']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 选项带有量化前缀，增加仪式感
    opts = [
        ("[ 0% ] 拒绝指令：完全背离业务直觉", 1),
        ("[ 25% ] 偏离轨道：较不符合执行习惯", 2),
        ("[ 50% ] 待定挂起：视具体交易场景而定", 3),
        ("[ 75% ] 拟合特征：比较符合决策链路", 4),
        ("[ 100% ] 强制锁定：完全复刻底层逻辑", 5)
    ]
    
    for text, val in opts:
        if st.button(text, type="secondary", key=f"q_{st.session_state.current_q}_{val}"):
            answer_clicked(val, q_data['dim'])
            st.rerun()

else:
    trigger_supernova()
    
    res = st.session_state.total_scores
    mbti = ("E" if res["E"] >= 0 else "I") + ("S" if res["S"] >= 0 else "N") + ("T" if res["T"] >= 0 else "F") + ("J" if res["J"] >= 0 else "P")
    data = mbti_details.get(mbti)
    
    st.markdown(f"""
    <div class="result-card">
        <div style="font-size:14px; color:#94a3b8; letter-spacing:4px; margin-bottom:15px; font-family:monospace;">MATRIX DECODED SUCCESSFULLY</div>
        <div class="mbti-code">{mbti}</div>
        <div class="mbti-post">【 {data['role']} 】</div>
        <div style="color:#ffffff; font-size:16px; line-height:1.8; margin-bottom:20px;">{data['desc']}</div>
        <div>
            {" ".join([f'<span style="background:#1e293b; color:#00f3ff; border:1px solid #00f3ff; padding:5px 14px; border-radius:6px; font-size:12px; font-weight:700; margin:4px; display:inline-block;">{t}</span>' for t in data['tags']])}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h4 style='color:#00f3ff; border-left:4px solid #00f3ff; padding-left:10px;'>🕸️ 核心能力拓扑矩阵</h4>", unsafe_allow_html=True)
    def get_intensity(score): return max(15, min(100, 50 + (score / 20 * 50)))
    val_E, val_I = get_intensity(res["E"]), 100 - get_intensity(res["E"])
    val_S, val_N = get_intensity(res["S"]), 100 - get_intensity(res["S"])
    val_T, val_F = get_intensity(res["T"]), 100 - get_intensity(res["T"])
    val_J, val_P = get_intensity(res["J"]), 100 - get_intensity(res["J"])
    categories = ['外向(E)', '实务(S)', '理性(T)', '秩序(J)', '内向(I)', '直觉(N)', '感性(F)', '灵活(P)']
    values = [val_E, val_S, val_T, val_J, val_I, val_N, val_F, val_P]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself', fillcolor='rgba(0, 243, 255, 0.2)', line=dict(color='#00f3ff', width=2), marker=dict(color='#ffd700', size=6)))
    fig.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100]), angularaxis=dict(tickfont=dict(color='#e2e8f0', size=13), linecolor='rgba(0,243,255,0.2)', gridcolor='rgba(0,243,255,0.1)')), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=35, r=35, t=20, b=20), height=300)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<h4 style='color:#00f3ff; border-left:4px solid #00f3ff; padding-left:10px;'>🎛️ 业务决策偏好仪表</h4>", unsafe_allow_html=True)
    risk_score = max(5, min(95, 50 + (res["P"] * 1.5) - (res["S"] * 1.5)))
    if risk_score < 35: r_tag, r_color, r_desc = "严谨风控导向", "#4ade80", "行事稳健，对合规红线有天然敏锐度，适合把守数据存证与风控命脉。"
    elif risk_score < 65: r_tag, r_color, r_desc = "动态平衡导向", "#ffd700", "能够在政策框架内灵活捕捉机遇，适合主导数据产品架构与业务统筹。"
    else: r_tag, r_color, r_desc = "前沿开拓导向", "#f43f5e", "极度渴望打破思维定式，拥有极强创新力，能快速抢占新兴生态阵地。"
    
    fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=risk_score, number={'suffix': "%", 'font': {'color': r_color, 'size': 35}}, title={'text': f"<span style='color:{r_color}; font-size:16px;'>{r_tag}</span>", 'font': {'color': '#94a3b8'}}, gauge={'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#334155"}, 'bar': {'color': r_color}, 'bgcolor': "rgba(255,255,255,0.05)", 'steps': [{'range': [0, 35], 'color': "rgba(74, 222, 128, 0.1)"}, {'range': [35, 65], 'color': "rgba(255, 215, 0, 0.1)"}, {'range': [65, 100], 'color': "rgba(244, 63, 94, 0.1)"}]}))
    fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "#94a3b8"}, height=250, margin=dict(l=20, r=20, t=30, b=0))
    st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})
    st.markdown(f"<div style='color:#e2e8f0; font-size:13px; text-align:center; margin-top:-20px; margin-bottom:20px;'>{r_desc}</div>", unsafe_allow_html=True)

    st.markdown("<h4 style='color:#10b981; border-left:4px solid #10b981; padding-left:10px;'>💡 职场生态协同指南</h4>", unsafe_allow_html=True)
    st.markdown(f"<div class='synergy-box'><div class='synergy-title'>[ 黄金协作搭档 ]</div><div style='margin-bottom:15px; color:#ffffff; font-weight:bold;'>{data['partner']}</div><div class='synergy-title'>[ 职场进阶建议 ]</div><div>{data['advice']}</div></div>", unsafe_allow_html=True)

    time_taken = st.session_state.end_time - st.session_state.start_time
    st.markdown("<h4 style='color:#00f3ff; border-left:4px solid #00f3ff; padding-left:10px;'>💠 专属数字身份标识</h4>", unsafe_allow_html=True)
    hash_code = hex(hash(mbti + str(time_taken) + str(res["S"])))[-10:].upper()
    share_card = f"""【SDE 人才能力图谱解析报告】
======================
◈ 特征序列：{mbti} ({data['role'].split(' / ')[0]})
◈ 核心素质：{' · '.join(data['tags'])}
◈ 决策偏好：{r_tag}
======================
全息校验码：0x{hash_code}E9
（解码职场潜能，驱动要素未来）"""
    st.markdown(f"<div style='background:#111827; padding:15px; border-radius:8px; font-family:monospace; font-size:13px; color:#ffffff; border:1px solid #334155; white-space:pre-wrap;'>{share_card}</div>", unsafe_allow_html=True)
    st.caption("☝️ 点击右上方复制按钮，或长按文本区发至微信分享你的专属图谱。")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("重启引擎系统 RESET()", type="primary", use_container_width=True):
        st.session_state.started = False
        st.session_state.current_q = 0
        st.session_state.total_scores = {"E": 0, "S": 0, "T": 0, "J": 0}
        st.rerun()

st.markdown("""
    <div style='text-align:center; margin-top:50px; margin-bottom:20px; font-family:monospace;'>
        <div style='color:#00f3ff; font-size:11px; opacity:0.5; letter-spacing:2px; margin-bottom:5px;'>
            POWERED BY DATA ELEMENT ENGINE
        </div>
        <div style='color:#ffd700; font-size:12px; font-weight:900; letter-spacing:3px; text-shadow:0 0 15px rgba(255,215,0,0.6);'>
            © 版权归属无名逆流所有
        </div>
    </div>
""", unsafe_allow_html=True)
