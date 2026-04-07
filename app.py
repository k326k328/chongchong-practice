import streamlit as st
import json
import os

DATA_FILE = "yu_jian.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

def load_questions():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_questions(questions):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

st.set_page_config(page_title="虫虫宗Python练习籍", page_icon="⚡", layout="wide")

st.title("⚡ 虫虫宗 · Python 练习籍")
st.caption("“道法自然，代码即神通” — 宗门长老寄语")

with st.sidebar:
    st.header("📜 撰写新试炼")
    with st.form("add_form"):
        question = st.text_area("试炼题目(描述功法难题)", height=277)
        answer = st.text_area("心法答案(标准解法)", height=277)
        submitted = st.form_submit_button("✨ 铭刻入玉简", use_container_width=True)
        if submitted and question and answer:
            questions = load_questions()
            questions.append({"question": question, "answer": answer})
            save_questions(questions)
            st.success("✅ 试炼已录入宗门玉简！")
            st.rerun()
    st.divider()
    st.caption("“每日练功，大道可期”")

st.subheader("📖 宗门试炼录")
questions = load_questions()

if not questions:
    st.info("⛩️ 玉简空空如也，请在左侧撰写第一道试炼。")
else:
    for idx, q in enumerate(questions):
        with st.expander(f"第 {idx+1} 关 · {q['question'][:40]}……"):
            st.markdown(f"**试炼内容**：{q['question']}")
            user_answer = st.text_input("你的悟道之答", key=f"ans_{idx}")
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("🔍 验证道心", key=f"check_{idx}"):
                    if user_answer.strip() == q['answer'].strip():
                        st.success("🎉 道心通明！答案正确！")
                    else:
                        st.error(f"❌ 心魔未除……正确答案应是：{q['answer']}")
            with col2:
                if st.button("🗑️ 焚毁此卷", key=f"del_{idx}"):
                    questions.pop(idx)
                    save_questions(questions)
                    st.rerun()
