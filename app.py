import streamlit as st
import json
import os
from openai import OpenAI

# ==================== 宗门秘钥配置 ====================
API_KEY = "sk-c11570678aed425eba774814cd514c02"
DATA_FILE = "yu_jian.json"
AI_MODEL = "deepseek-chat"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

def load_questions():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_questions(questions):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

def check_answer_with_ai(question, user_answer):
    """天机长老评判答案"""
    try:
        client = OpenAI(
            api_key=API_KEY,
            base_url="https://api.deepseek.com"
        )
        
        prompt = f"""你是修真界Python宗门的天机长老，负责评判弟子的试炼答案。

【试炼题目】
{question}

【弟子作答】
{user_answer}

请你以修仙宗门长老的身份进行评判：
1. 判断答案是否正确
2. 如有错误，指出心魔所在（问题所在）
3. 传授正确功法（给出正确思路和代码）
4. 用修仙风格的鼓励语言点评

请以JSON格式返回：
{{"correct": true或false, "feedback": "完整的评判内容，使用修仙风格语言"}}
"""
        
        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        return {
            "correct": False, 
            "feedback": f"⚠️ 天机长老正在闭关，暂无法评判。错误信息：{str(e)}"
        }

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="虫虫宗·Python修炼殿", 
    page_icon="🏯", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 自定义CSS ====================
st.markdown("""
<style>
    /* 整体背景 */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #e8e8e8;
    }
    
    /* 标题样式 */
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        color: #ffd700;
        text-shadow: 0 0 10px #ffd700, 0 0 20px #ffd700;
        margin-bottom: 0.5rem;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 10px #ffd700, 0 0 20px #ffd700; }
        to { text-shadow: 0 0 20px #ffd700, 0 0 30px #ffd700, 0 0 40px #ffd700; }
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #b0b0b0;
        font-style: italic;
        margin-bottom: 2rem;
    }
    
    /* 关卡卡片 */
    .question-card {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid #ffd700;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(255, 215, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .level-badge {
        background: linear-gradient(135deg, #ffd700, #ffed4e);
        color: #1a1a2e;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }
    
    /* 成功/失败提示 */
    .success-box {
        background: linear-gradient(135deg, rgba(0, 255, 0, 0.1), rgba(0, 200, 0, 0.1));
        border: 2px solid #00ff00;
        border-radius: 10px;
        padding: 15px;
        margin-top: 10px;
    }
    
    .error-box {
        background: linear-gradient(135deg, rgba(255, 0, 0, 0.1), rgba(200, 0, 0, 0.1));
        border: 2px solid #ff4444;
        border-radius: 10px;
        padding: 15px;
        margin-top: 10px;
    }
    
    /* 侧边栏 */
    .sidebar-text {
        color: #ffd700;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 主页面 ====================
st.markdown('<div class="main-title">🏯 虫虫宗 · Python修炼殿 🏯</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">"道法自然，代码即神通" —— 天机长老寄语</div>', unsafe_allow_html=True)

# ==================== 侧边栏 ====================
with st.sidebar:
    st.markdown("## 📜 撰写新试炼")
    st.divider()
    
    with st.form("add_form", clear_on_submit=True):
        st.markdown("### ✨ 录入新功法")
        question = st.text_area("🎯 试炼题目\n(描述功法难题)", height=120, placeholder="例如：如何用Python计算斐波那契数列？")
        hint = st.text_area("💡 修炼提示\n(可选，助弟子悟道)", height=80, placeholder="例如：可以使用递归或迭代方法")
        
        submit = st.form_submit_button("⚡ 铭刻入玉简", use_container_width=True, type="primary")
        
        if submit:
            if not question.strip():
                st.error("❌ 试炼题目不可为空！")
            else:
                questions = load_questions()
                questions.append({
                    "question": question.strip(),
                    "hint": hint.strip() if hint else ""
                })
                save_questions(questions)
                st.success("✅ 试炼已录入宗门玉简！")
                st.rerun()
    
    st.divider()
    st.markdown("### 📊 修炼统计")
    questions = load_questions()
    st.metric("📜 试炼总数", len(questions))
    
    st.divider()
    st.markdown("### 🎋 宗门言")
    st.caption("""
    > 千里之行，始于足下  
    > 万行代码，源于一念  
    >  
    > 每日练功，大道可期  
    > 天道酬勤，功不唐捐
    """)

# ==================== 试炼展示区 ====================
st.markdown("### 📖 宗门试炼录")
st.divider()

questions = load_questions()

if not questions:
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px; background: rgba(255, 215, 0, 0.05); border-radius: 15px; border: 2px dashed #ffd700;">
        <h2 style="color: #ffd700;">⛩️ 玉简空空如也</h2>
        <p style="color: #b0b0b0; font-size: 1.1rem;">
            请在左侧撰写第一道试炼，开启修仙之旅<br>
            <span style="color: #808080; font-style: italic;">"万丈高楼平地起，一行代码一重天"</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    # 使用两列布局
    cols = st.columns(2)
    
    for idx, q in enumerate(questions):
        col_idx = idx % 2
        
        with cols[col_idx]:
            st.markdown(f"""
            <div class="question-card">
                <div class="level-badge">第 {idx + 1} 关</div>
                <p style="font-size: 1.1rem; margin-top: 10px; line-height: 1.6;">{q['question']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if q.get("hint"):
                with st.expander("💡 查看修炼提示"):
                    st.info(q["hint"], icon="📿")
            
            user_answer = st.text_area(
                "✍️ 你的悟道之答",
                key=f"ans_{idx}",
                height=180,
                placeholder="在此写下你的代码或答案...\n\n天道酬勤，静心作答",
                label_visibility="visible"
            )
            
            # 操作按钮
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("🔮 请天机长老评判", key=f"check_{idx}", use_container_width=True, type="primary"):
                    if not user_answer.strip():
                        st.warning("⚠️ 尚未作答，如何评判？", icon="⚠️")
                    else:
                        with st.spinner("🔮 天机长老正在推演天机..."):
                            result = check_answer_with_ai(q["question"], user_answer)
                            st.session_state[f"result_{idx}"] = result
            
            with col_btn2:
                if st.button("🗑️ 焚毁此卷", key=f"del_{idx}", use_container_width=True):
                    questions.pop(idx)
                    save_questions(questions)
                    st.success("🔥 此卷已焚毁", icon="🔥")
                    st.rerun()
            
            # 显示评判结果
            if f"result_{idx}" in st.session_state:
                result = st.session_state[f"result_{idx}"]
                feedback = result.get("feedback", "")
                
                if result.get("correct"):
                    st.markdown(f"""
                    <div class="success-box">
                        <h3 style="color: #00ff00; margin-top: 0;">🎉 道心通明！</h3>
                        <p style="line-height: 1.8; white-space: pre-wrap;">{feedback}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="error-box">
                        <h3 style="color: #ff4444; margin-top: 0;">❌ 心魔未除</h3>
                        <p style="line-height: 1.8; white-space: pre-wrap;">{feedback}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # 添加间距
        if col_idx == 1:
            st.markdown("<br>", unsafe_allow_html=True)

# ==================== 页脚 ====================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #808080; padding: 20px;">
    <p>🏯 虫虫宗修炼殿 · Python问道之旅 🏯</p>
    <p style="font-size: 0.9rem;">"代码之道，生生不息；bug之劫，终可化解"</p>
</div>
""", unsafe_allow_html=True)
