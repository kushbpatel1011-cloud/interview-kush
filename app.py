import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Agentic Mock Interviewer", layout="centered")
st.title("🧠 Agentic Mock Interviewer + Feedback Generator")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.markdown("**Step 1:** Enter the role you're preparing for")

job_role = st.text_input("Enter Role (e.g., Data Scientist at Google)")

st.markdown("**Step 2:** Click below to get a question")
question = ""
if st.button("🎤 Generate Interview Question"):
    prompt = f"""You're an expert interviewer. Ask a challenging and relevant interview question for the role: {job_role}."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    question = response.choices[0].message.content
    st.session_state["question"] = question
    st.markdown(f"""### 🗨️ Interview Question:
{question}""")

# Input for user answer
if "question" in st.session_state:
    st.markdown("**Step 3:** Write your answer below")
    user_answer = st.text_area("Your Answer", height=200)

    if st.button("📝 Generate Feedback"):
        feedback_prompt = f"""You're a professional interviewer. Here is the question and the candidate's answer.

        Question: {st.session_state['question']}
        Answer: {user_answer}

        Provide constructive feedback in bullet points including strengths, weaknesses, and how the answer could be improved.
        """
        feedback = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": feedback_prompt}],
            temperature=0.7
        )
        st.subheader("📋 AI Feedback")
        st.markdown(feedback.choices[0].message.content)
        # Generate Rating out of 5
        rating_prompt = f"""You are an expert interviewer. Based on the following question and candidate's answer, give a rating out of 5 (where 5 is excellent and 1 is poor), along with a one-line justification.

        Question: {st.session_state['question']}
        Answer: {user_answer}

        Respond in this format:
        Rating: X/5
        Reason: <one-line justification>
        """

        rating_response = client.chat.completions.create(
           model="gpt-3.5-turbo",
           messages=[{"role": "user", "content": rating_prompt}],
           temperature=0.7)

        st.subheader("⭐ Final Rating")
        st.markdown(rating_response.choices[0].message.content)