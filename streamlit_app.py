import streamlit as st
import openai

# ------------------ 配置 ------------------
# 将你的 OpenAI API Key 放在 Streamlit Secrets 中更安全
# 或者直接在本地测试时使用 openai.api_key = "YOUR_API_KEY"
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 测试输出（不会显示密钥，只显示前几位）
# st.write("✅ Secrets 已加载，当前 API Key 前缀：", openai.api_key[:8])

# ------------------ 页面标题 ------------------
st.set_page_config(page_title="📖 英语阅读理解伴读助手", layout="wide")
st.title("📖 英语阅读理解伴读助手")

# ------------------ 输入章节文本 ------------------
text = st.text_area("📋 复制或粘贴英文书本章节/段落", height=200)

# ------------------ 生成理解问题 ------------------
if st.button("📝 生成理解问题"):
    if not text.strip():
        st.warning("请先粘贴章节文本！")
    else:
        with st.spinner("生成问题中..."):
            prompt = f"""Read the following English text and generate 5 comprehension questions in English.
Text:
{text}"""
            response = openai.ChatCompletion.create(
                model="gpt-5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            questions = response.choices[0].message.content
            st.session_state.questions = questions
            st.subheader("❓ 理解问题：")
            st.text_area("Questions:", value=questions, height=150)

# ------------------ 用户答题 ------------------
if "questions" in st.session_state:
    st.subheader("✏️ 输入你的答案")
    answer = st.text_area("Write your answers here:", height=150)
    
    if st.button("✅ 检查理解"):
        if not answer.strip():
            st.warning("请先输入答案！")
        else:
            with st.spinner("AI 评估中..."):
                eval_prompt = f"""
Text:
{text}

Questions:
{st.session_state.questions}

User's answers:
{answer}

Evaluate the answers in terms of comprehension.
Provide feedback and a score out of 10.
"""
                eval_response = openai.ChatCompletion.create(
                    model="gpt-5-turbo",
                    messages=[{"role": "user", "content": eval_prompt}]
                )
                st.subheader("📊 AI 反馈与评分")
                st.write(eval_response.choices[0].message.content)

# ------------------ 保存答题记录（可选） ------------------
st.subheader("💾 保存记录（可选）")
if st.button("保存到本地文本文件"):
    if "questions" in st.session_state and answer.strip():
        with open("reading_record.txt", "a", encoding="utf-8") as f:
            f.write("\n\n=== 新章节 ===\n")
            f.write(text + "\n")
            f.write(st.session_state.questions + "\n")
            f.write("User Answer:\n" + answer + "\n")
        st.success("保存成功 ✅")
    else:
        st.warning("请先生成问题并填写答案！")