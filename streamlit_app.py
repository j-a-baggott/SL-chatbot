import streamlit as st
import requests

st.set_page_config(page_title="Insurance Chatbot", page_icon="💬")
st.title("💬 Insurance Support Chatbot")

# 🔒 SnapLogic API details — replace with your actual values
SNAPLOGIC_URL = "https://emea.snaplogic.com/api/1/rest/slsched/feed/ConnectFasterInc/projects/Jonny%20Baggott/JB%20-%20Policy%20Query%20Task"
BEARER_TOKEN = "RH6OjJkwrXKF3UFHcVj76rTXdRH4WJin"

# Initialize session state
if 'chat_started' not in st.session_state:
    st.session_state.chat_started = False

# Step 1: Ask if user has a question (policy number should be included)
if not st.session_state.chat_started:
    with st.form("question_form"):
        st.subheader("👋 What would you like to ask about your insurance policy?")
        st.markdown("➡️ Please include your policy number in your question.")
        question = st.text_area("Your question")
        submitted = st.form_submit_button("Submit")

        if submitted and question.strip():
            st.session_state.question = question.strip()
            st.session_state.chat_started = True
        elif submitted:
            st.warning("Please enter your question including your policy number.")
else:
    st.write(f"📨 **You asked:** {st.session_state.question}")

    # Step 2: Send to SnapLogic
    with st.spinner("🔍 Checking your policy details..."):
        try:
            combined_prompt = st.session_state.question

            payload = [
                {
                    "prompt": combined_prompt
                }
            ]

            headers = {
                "Authorization": f"Bearer {BEARER_TOKEN}",
                "Content-Type": "application/json"
            }

            response = requests.post(
                SNAPLOGIC_URL,
                headers=headers,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            if isinstance(data, list) and len(data) > 0 and "answer" in data[0]:
                answer = data[0]["answer"]
            elif isinstance(data, dict) and "answer" in data:
                answer = data["answer"]
            else:
                answer = "❓ I couldn't find the answer to your question."

        except Exception as e:
            answer = f"❌ There was an error: {e}"

    st.success("Here's what I found:")
    st.write(f"🤖 {answer}")

    # Step 3: Follow-up question
    st.subheader("📍 Can I help you with anything else today?")
    more_help = st.text_input("Ask another question (or leave blank to end)")

    if more_help.strip():
        st.session_state.question = more_help.strip()
        st.experimental_rerun()
