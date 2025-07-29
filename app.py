import streamlit as st
from openai import OpenAI
import os
import dotenv
# Load environment variables from .env file
# Ensure you have a .env file with your OpenAI API key
dotenv.load_dotenv()

# Setting up API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Page configuration
st.set_page_config(page_title="Mental Health Bot", layout="wide", page_icon="🏥")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


st.markdown("## Mental Health Bot👨🏽‍⚕️")
st.markdown("####  Hey, I am here to assist you. Feel free to tell me what is wrong")

# Input box
with st.container():
    
    with st.form(key="question_form", clear_on_submit=True):
        question = st.text_input("💬 Your question:", placeholder="")
        submit = st.form_submit_button("📤 Submit Question")

# submission stage
if submit and question.strip():
    # Save user's question to chat history
    st.session_state.messages.append({"role": "user", "content": question})

    # Display thinking spinner and get response
    with st.spinner("💭 Thinking..."):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "You are a Mental health assistant. be empathic and help full to others inoder to help their mental health."}] +
                         [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                temperature=0.5,
                max_tokens=600
            )
            answer = response.choices[0].message.content.strip()
            st.session_state.messages.append({"role": "assistant", "content": answer})

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Display chat history
for message in reversed(st.session_state.messages):
    role = message["role"]
    content = message["content"]

    if role == "user":
        st.markdown(f'<div class="chat-message user-message"><strong>You:</strong><br>{content}</div>', unsafe_allow_html=True)
    elif role == "assistant":
        st.markdown(f'<div class="chat-message bot-message"><strong>Mentaal Health Bot:</strong><br>{content}</div>', unsafe_allow_html=True)

# Footer effect
st.markdown("---")
st.markdown("© 2025 smart Mental health bot| Built with ❤️ using [Streamlit](https://streamlit.io/) and [OpenAI GPT-3.5](https://platform.openai.com)")
