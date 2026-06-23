import streamlit as st
import requests
import json
from datetime import date

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="影の語り部 – Ancient Weight Loss Mentor",
    page_icon="🌸",
    layout="wide",
)

# ── CSS – dark Japanese aesthetic (matches original) + tracker panel ────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@300;400;600&family=Inter:wght@300;400;500&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    background-color: #1a1410 !important;
    color: #e8ddd0 !important;
    font-family: 'Inter', sans-serif;
}
.stApp { background-color: #1a1410; }

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; }

/* ── Title ── */
.app-title {
    font-family: 'Noto Serif JP', serif;
    font-size: 2.6rem;
    font-weight: 600;
    color: #e8c99a;
    letter-spacing: 0.05em;
    margin-bottom: 0;
}
.app-subtitle {
    font-size: 0.85rem;
    color: #8a7a68;
    letter-spacing: 0.12em;
    margin-bottom: 1.5rem;
}

/* ── Section headers ── */
.section-header {
    font-family: 'Noto Serif JP', serif;
    font-size: 1rem;
    color: #c4a882;
    letter-spacing: 0.08em;
    border-bottom: 1px solid #3a2e22;
    padding-bottom: 0.4rem;
    margin-bottom: 1rem;
}

/* ── Chat messages ── */
.chat-user, .chat-bot {
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.8rem;
    font-size: 0.93rem;
    line-height: 1.65;
    border: 1px solid #2e2418;
}
.chat-user {
    background: #231c14;
    border-left: 3px solid #c47a3a;
}
.chat-bot {
    background: #1e1812;
    border-left: 3px solid #6b8e6b;
    font-style: italic;
    color: #d4c8b8;
}

/* ── Input box ── */
.stTextArea textarea {
    background-color: #231c14 !important;
    border: 1px solid #3a2e22 !important;
    border-radius: 8px !important;
    color: #e8ddd0 !important;
    font-size: 0.9rem !important;
}
.stTextArea textarea:focus {
    border-color: #c47a3a !important;
    box-shadow: 0 0 0 1px #c47a3a33 !important;
}

/* ── Buttons ── */
.stButton > button {
    background: #2e2014 !important;
    color: #c4a882 !important;
    border: 1px solid #4a3828 !important;
    border-radius: 6px !important;
    font-size: 0.85rem !important;
    padding: 0.4rem 1rem !important;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: #3e2e1a !important;
    border-color: #c47a3a !important;
    color: #e8c99a !important;
}

/* ── Select box ── */
.stSelectbox > div > div {
    background-color: #231c14 !important;
    border: 1px solid #3a2e22 !important;
    color: #e8ddd0 !important;
    border-radius: 8px !important;
}

/* ── Number inputs ── */
.stNumberInput input {
    background-color: #231c14 !important;
    border: 1px solid #3a2e22 !important;
    color: #e8ddd0 !important;
    border-radius: 6px !important;
}

/* ── Tracker cards ── */
.macro-card {
    background: #231c14;
    border: 1px solid #3a2e22;
    border-radius: 10px;
    padding: 0.8rem 1rem;
    text-align: center;
    margin-bottom: 0.6rem;
}
.macro-value {
    font-size: 1.5rem;
    font-weight: 600;
    color: #e8c99a;
    font-family: 'Noto Serif JP', serif;
}
.macro-label {
    font-size: 0.72rem;
    color: #8a7a68;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.macro-remaining {
    font-size: 0.78rem;
    color: #6b8e6b;
    margin-top: 0.2rem;
}

/* ── Progress bar wrapper ── */
.progress-wrap {
    background: #2e2418;
    border-radius: 4px;
    height: 6px;
    margin: 0.4rem 0 0.8rem;
    overflow: hidden;
}
.progress-fill {
    height: 6px;
    border-radius: 4px;
    transition: width 0.4s ease;
}

/* ── Food log table ── */
.food-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.45rem 0;
    border-bottom: 1px solid #2e2418;
    font-size: 0.85rem;
    color: #c8b89a;
}
.food-row:last-child { border-bottom: none; }
.food-kcal { color: #c47a3a; font-weight: 500; }

/* ── Divider ── */
.col-divider {
    width: 1px;
    background: #2e2418;
    margin: 0 0.5rem;
}

/* ── Label override ── */
label, .stSelectbox label, .stNumberInput label {
    color: #8a7a68 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.06em !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session state init ──────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "food_log" not in st.session_state:
    st.session_state.food_log = []          # list of {name, kcal, p, c, f}
if "log_date" not in st.session_state:
    st.session_state.log_date = str(date.today())

# Reset log if it's a new day
if st.session_state.log_date != str(date.today()):
    st.session_state.food_log = []
    st.session_state.log_date = str(date.today())

# ── Sidebar – model selector & daily goals ────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="section-header">🌸 Spirit Guide</div>', unsafe_allow_html=True)

    # Fetch available Ollama models
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=3)
        models = [m["name"] for m in r.json().get("models", [])]
    except Exception:
        models = ["gemma3:4b"]

    selected_model = st.selectbox("Choose your spirit guide", models)

    st.markdown('<div class="section-header" style="margin-top:1.5rem">⚖️ Daily Goals</div>', unsafe_allow_html=True)
    goal_kcal = st.number_input("Calories (kcal)", min_value=800, max_value=4000, value=1800, step=50)
    goal_protein = st.number_input("Protein (g)", min_value=30, max_value=300, value=120, step=5)
    goal_carbs = st.number_input("Carbs (g)", min_value=30, max_value=500, value=180, step=5)
    goal_fat = st.number_input("Fat (g)", min_value=20, max_value=200, value=60, step=5)

    st.markdown('<div class="section-header" style="margin-top:1.5rem">📅 Today</div>', unsafe_allow_html=True)
    st.caption(str(date.today().strftime("%B %d, %Y")))

    if st.button("🗑️ Clear food log"):
        st.session_state.food_log = []
        st.rerun()

# ── Layout: chat (left) | tracker (right) ─────────────────────────────────────
col_chat, col_tracker = st.columns([3, 2], gap="medium")

# ═══════════════════════════════════════════════════════════════════════════════
# LEFT COLUMN – CHAT
# ═══════════════════════════════════════════════════════════════════════════════
with col_chat:
    st.markdown('<div class="app-title">🌸 影の語り部</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">Kage no Kataribe — Ancient Weight Loss Mentor</div>', unsafe_allow_html=True)

    # Chat history
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-user">🔴 {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-bot">🟠 {msg["content"]}</div>', unsafe_allow_html=True)

    # Input area
    user_input = st.text_area(
        label="speak",
        placeholder="Speak your thoughts…",
        height=80,
        label_visibility="collapsed",
        key="chat_input",
    )

    send_col, _ = st.columns([1, 4])
    with send_col:
        send_clicked = st.button("↑ Send", use_container_width=True)

    if send_clicked and user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input.strip()})

        system_prompt = (
            "You are Kage no Kataribe (影の語り部), the Shadow Speaker — an ancient, wise weight-loss mentor "
            "who blends Japanese philosophy with evidence-based nutrition and health advice. "
            "Speak with calm authority, poetic but clear. Use Japanese terms occasionally (in italics). "
            "When users mention food they've eaten, also naturally estimate its nutritional content "
            "(calories, protein, carbs, fat) in a concise JSON block at the END of your response, "
            "formatted exactly like this — and ONLY if food is mentioned:\n"
            "```json\n{\"food_logged\": true, \"name\": \"item\", \"kcal\": 0, \"protein_g\": 0, \"carbs_g\": 0, \"fat_g\": 0}\n```\n"
            "If no food is mentioned, do NOT include any JSON."
        )

        payload = {
            "model": selected_model,
            "messages": [{"role": "system", "content": system_prompt}]
                        + st.session_state.messages,
            "stream": False,
        }

        try:
            resp = requests.post(
                "http://localhost:11434/api/chat",
                json=payload,
                timeout=120,
            )
            bot_reply = resp.json()["message"]["content"]

            # Parse any food JSON out of the reply
            import re
            json_match = re.search(r"```json\s*(\{.*?\})\s*```", bot_reply, re.DOTALL)
            if json_match:
                try:
                    food_data = json.loads(json_match.group(1))
                    if food_data.get("food_logged"):
                        st.session_state.food_log.append({
                            "name": food_data.get("name", "Unknown"),
                            "kcal": int(food_data.get("kcal", 0)),
                            "p": int(food_data.get("protein_g", 0)),
                            "c": int(food_data.get("carbs_g", 0)),
                            "f": int(food_data.get("fat_g", 0)),
                        })
                    # Strip the JSON block from the visible reply
                    bot_reply = re.sub(r"```json\s*\{.*?\}\s*```", "", bot_reply, flags=re.DOTALL).strip()
                except Exception:
                    pass

            st.session_state.messages.append({"role": "assistant", "content": bot_reply})

        except Exception as e:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"*The shadows grow silent… ({e})*",
            })

        st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# RIGHT COLUMN – CALORIE / MACRO TRACKER
# ═══════════════════════════════════════════════════════════════════════════════
with col_tracker:
    st.markdown('<div class="section-header" style="margin-top:0.2rem">🍱 Today\'s Nourishment</div>', unsafe_allow_html=True)

    # Totals
    total_kcal  = sum(f["kcal"] for f in st.session_state.food_log)
    total_p     = sum(f["p"]    for f in st.session_state.food_log)
    total_c     = sum(f["c"]    for f in st.session_state.food_log)
    total_f     = sum(f["f"]    for f in st.session_state.food_log)

    def pct(val, goal):
        return min(int(val / goal * 100), 100) if goal > 0 else 0

    def bar_color(p):
        if p < 60:   return "#6b8e6b"   # green – under
        if p < 90:   return "#c4a244"   # amber – approaching
        if p <= 100: return "#c47a3a"   # orange – near goal
        return "#a04040"                 # red – over

    # Calories card
    p_kcal = pct(total_kcal, goal_kcal)
    rem_kcal = goal_kcal - total_kcal
    st.markdown(f"""
    <div class="macro-card">
        <div class="macro-value">{total_kcal}</div>
        <div class="macro-label">Calories consumed</div>
        <div class="macro-remaining">{"↑ " + str(abs(rem_kcal)) + " over goal" if rem_kcal < 0 else str(rem_kcal) + " remaining"}</div>
        <div class="progress-wrap">
            <div class="progress-fill" style="width:{p_kcal}%; background:{bar_color(p_kcal)};"></div>
        </div>
        <div style="font-size:0.72rem;color:#8a7a68;">Goal: {goal_kcal} kcal</div>
    </div>
    """, unsafe_allow_html=True)

    # Macro row
    m_col1, m_col2, m_col3 = st.columns(3)

    def macro_card(col, label, val, goal, unit="g"):
        p = pct(val, goal)
        col.markdown(f"""
        <div class="macro-card">
            <div class="macro-value" style="font-size:1.2rem">{val}{unit}</div>
            <div class="macro-label">{label}</div>
            <div class="progress-wrap">
                <div class="progress-fill" style="width:{p}%; background:{bar_color(p)};"></div>
            </div>
            <div style="font-size:0.7rem;color:#8a7a68;">{goal}{unit} goal</div>
        </div>
        """, unsafe_allow_html=True)

    macro_card(m_col1, "Protein", total_p, goal_protein)
    macro_card(m_col2, "Carbs",   total_c, goal_carbs)
    macro_card(m_col3, "Fat",     total_f, goal_fat)

    # ── Manual food entry ─────────────────────────────────────────────────────
    st.markdown('<div class="section-header" style="margin-top:1rem">✏️ Log Food Manually</div>', unsafe_allow_html=True)

    with st.expander("Add food entry", expanded=False):
        f_name = st.text_input("Food name", placeholder="e.g. Onigiri", key="fname")
        fc1, fc2 = st.columns(2)
        f_kcal = fc1.number_input("Calories", 0, 3000, 0, key="fkcal")
        f_p    = fc2.number_input("Protein (g)", 0, 200, 0, key="fp")
        fc3, fc4 = st.columns(2)
        f_c    = fc3.number_input("Carbs (g)", 0, 500, 0, key="fc")
        f_f    = fc4.number_input("Fat (g)", 0, 200, 0, key="ff")

        if st.button("Add to log", use_container_width=True):
            if f_name.strip():
                st.session_state.food_log.append({
                    "name": f_name.strip(),
                    "kcal": f_kcal,
                    "p": f_p,
                    "c": f_c,
                    "f": f_f,
                })
                st.rerun()

    # ── Food log ──────────────────────────────────────────────────────────────
    if st.session_state.food_log:
        st.markdown('<div class="section-header" style="margin-top:1rem">📋 Food Log</div>', unsafe_allow_html=True)
        for i, item in enumerate(st.session_state.food_log):
            log_col, del_col = st.columns([5, 1])
            with log_col:
                st.markdown(
                    f'<div class="food-row">'
                    f'<span>{item["name"]}</span>'
                    f'<span class="food-kcal">{item["kcal"]} kcal</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            with del_col:
                if st.button("✕", key=f"del_{i}"):
                    st.session_state.food_log.pop(i)
                    st.rerun()

    # ── Tip from the Shadow Speaker ───────────────────────────────────────────
    st.markdown('<div class="section-header" style="margin-top:1.2rem">🌿 Wisdom</div>', unsafe_allow_html=True)
    if total_kcal == 0:
        tip = "*Begin by observing — tell me what you have eaten today, and I shall guide the balance.*"
    elif pct(total_kcal, goal_kcal) > 100:
        tip = "*The river has overflowed its banks today. Rest, reflect, and return to stillness tomorrow.*"
    elif pct(total_kcal, goal_kcal) > 85:
        tip = "*You approach the threshold with intention. Choose your next meal with the mindfulness of the moon.*"
    elif total_p < goal_protein * 0.5:
        tip = "*The muscles hunger for sustenance — seek protein in your next meal, as the crane seeks still water.*"
    else:
        tip = "*You walk the path with steadiness. The body remembers every act of care.*"

    st.markdown(f'<div class="chat-bot" style="margin-top:0">{tip}</div>', unsafe_allow_html=True)
