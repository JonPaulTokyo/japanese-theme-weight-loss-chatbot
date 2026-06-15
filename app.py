import streamlit as st
import ollama

# ================== WEIGHT LOSS MENTOR ==================
PERSONALITY = """
You are "Kage no Kataribe" (影の語り部), an ancient Japanese Shadow Mentor specializing in sustainable weight loss.
You combine bushido discipline, Zen mindfulness, and modern science. Speak calmly, wisely, and poetically.
Focus on healthy habits: calorie deficit, protein, strength training, walking, sleep, and hara hachi bu.
Never promote crash diets or pills.
"""
# ========================================================

st.set_page_config(page_title="影の語り部 | Weight Loss Mentor", page_icon="🌸", layout="centered")

# CSS that works great both online and offline
st.markdown("""
<style>
    /* Try to load beautiful Japanese fonts when online */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative&family=Noto+Serif+JP:wght@400;700&display=swap');

    .stApp {
        background: linear-gradient(180deg, #1a120b 0%, #2c1f14 100%);
        color: #e8d5b8;
        font-family: 'Noto Serif JP', system-ui, -apple-system, sans-serif;
    }

    h1 {
        font-family: 'Cinzel Decorative', cursive;
        color: #d4af37;
        text-shadow: 0 0 15px #8b5a2b;
        letter-spacing: 3px;
    }

    .stChatMessage {
        border-radius: 12px;
        border: 1px solid #8b5a2b;
        background: rgba(30, 20, 15, 0.95);
        box-shadow: 0 4px 15px rgba(139, 90, 43, 0.4);
    }

    .stChatMessage.user {
        background: rgba(139, 90, 43, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Falling Sakura (works 100% offline)
st.markdown("""
<script>
    function createPetal() {
        const petal = document.createElement('div');
        petal.className = 'sakura';
        petal.style.left = Math.random() * 100 + 'vw';
        petal.style.opacity = Math.random() * 0.6 + 0.4;
        petal.style.fontSize = Math.random() * 18 + 12 + 'px';
        petal.textContent = ['🌸','🌺','🍃'][Math.floor(Math.random() * 3)];
        petal.style.animationDuration = Math.random() * 12 + 14 + 's';
        petal.style.animationDelay = '-' + Math.random() * 15 + 's';
        document.body.appendChild(petal);
        setTimeout(() => petal.remove(), 20000);
    }
    setInterval(createPetal, 180);
    for (let i = 0; i < 12; i++) setTimeout(createPetal, i * 80);
</script>
<style>
    .sakura { position: fixed; top: -50px; z-index: -1; pointer-events: none; animation: fall linear infinite; }
    @keyframes fall { to { transform: translateY(105vh) rotate(360deg); } }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🌸 影の語り部")
st.caption("**Kage no Kataribe** — Ancient Weight Loss Mentor")

model = st.selectbox("Choose your spirit guide", ["gemma3:4b", "llama3.2", "phi3"], index=0)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": PERSONALITY}]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Speak your thoughts..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in ollama.chat(model=model, messages=st.session_state.messages, stream=True):
            full_response += response['message']['content']
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
