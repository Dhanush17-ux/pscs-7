import streamlit as st
import requests
import base64
from googletrans import Translator

# --------------------------
# 1. PAGE CONFIGURATION
# --------------------------
st.set_page_config(
    page_title="Chacha Chaudhary Chatbot",
    page_icon="🤠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --------------------------
# 2. FILE PATHS
# --------------------------
BG_PATH = r"background.png"
AVATAR_PATH = r"avatar.png"

# --------------------------
# 3. IMAGE LOADER
# --------------------------
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        return ""

base64_bg = get_base64_image(BG_PATH)

# --------------------------
# 4. CSS STYLING
# --------------------------
st.markdown(
    f"""
    <style>
    /* RESET MARGINS */
    html, body, .stApp {{
        margin: 0;
        padding: 0;
        font-family: sans-serif;
    }}

    /* BACKGROUND IMAGE CONFIGURATION */
    .stApp {{
        background-image: url("data:image/png;base64,{base64_bg}");
        background-repeat: no-repeat;
        background-position: center center;
        background-attachment: fixed;
        /* THIS FORCES THE IMAGE TO STRETCH TO FILL THE SCREEN EXACTLY */
        background-size: 100% 100%; 
    }}

    /* THE SINGLE GLASS CONTAINER */
    .block-container {{
        background-color: rgba(255, 255, 255, 0.65);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        padding: 3rem !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        max-width: 850px;
        margin-top: 40px;
        margin-bottom: 40px;
    }}

    /* TEXT & UI STYLES */
    h1 {{ color: #1e293b !important; font-weight: 800; margin-top: 0; }}
    p, label, div, span {{ color: #0f172a; }}
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* CHAT BUBBLES */
    .user-bubble {{
        background-color: #2563eb;
        color: white !important;
        padding: 12px 18px;
        border-radius: 18px 18px 2px 18px;
        margin: 8px 0;
        display: inline-block;
        float: right;
        clear: both;
        font-size: 16px;
    }}
    .bot-bubble {{
        background-color: #ffffff;
        color: #1e293b !important;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 2px;
        margin: 8px 0;
        display: inline-block;
        float: left;
        clear: both;
        font-size: 16px;
        border: 1px solid #cbd5e1;
    }}

    /* INPUT & SELECT BOX STYLING */
    .stTextInput > div > div > input {{
        background-color: rgba(255, 255, 255, 0.8);
        border: 1px solid #94a3b8;
        color: #0f172a;
        border-radius: 12px;
        padding: 10px;
    }}
    .stSelectbox > div > div {{
        background-color: rgba(255, 255, 255, 0.8) !important;
        color: #0f172a !important;
        border-radius: 10px;
    }}
    .stButton > button {{
        background-color: #2563eb;
        color: white;
        border-radius: 12px;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s;
    }}
    .stButton > button:hover {{
        background-color: #1d4ed8;
        transform: scale(1.02);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------
# 5. INITIALIZE SESSION
# --------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------
# 6. HEADER & LANGUAGE SELECTOR
# --------------------------
col1, col2 = st.columns([1, 4])

with col1:
    try:
        st.image(AVATAR_PATH, width=110)
    except:
        st.write("🤠")

with col2:
    st.title("Chacha Chaudhary Chatbot")
    st.write("Your guide to the Namami Gange Mission!")

lang_col1, lang_col2 = st.columns([2, 1])
with lang_col1:
    lang_options = {
        "English": "en",
        "Hindi (हिंदी)": "hi",
        "Bengali (বাংলা)": "bn",
        "Marathi (मराठी)": "mr",
        "Telugu (తెలుగు)": "te",
        "Tamil (தமிழ்)": "ta",
        "Gujarati (ગુજરાતી)": "gu",
        "Kannada (ಕನ್ನಡ)": "kn",
        "Malayalam (മലയാളം)": "ml",
        "Punjabi (ਪੰਜਾਬੀ)": "pa",
        "Urdu (اردو)": "ur",
        "Odia (ଓଡ଼ିଆ)": "or"
    }
    selected_lang_name = st.selectbox("Choose Language / भाषा चुनें:", list(lang_options.keys()))
    target_lang_code = lang_options[selected_lang_name]

st.markdown("---")

# --------------------------
# 7. CHAT DISPLAY AREA
# --------------------------
chat_container = st.container()

with chat_container:
    for m in st.session_state.messages:
        if m["role"] == "user":
            st.markdown(f"<div class='user-bubble'>{m['content']}</div>", unsafe_allow_html=True)
            st.markdown("<div style='clear: both;'></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-bubble'>{m['content']}</div>", unsafe_allow_html=True)
            st.markdown("<div style='clear: both;'></div>", unsafe_allow_html=True)

# --------------------------
# 8. INPUT FORM
# --------------------------
st.markdown("<br>", unsafe_allow_html=True)

with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here...", key="user_text")
    c1, c2 = st.columns([5, 1])
    with c2:
        submit_button = st.form_submit_button("Send ➤")

# --------------------------
# 9. BACKEND LOGIC
# --------------------------
translator = Translator()

def ask_backend(query, lang_code):
    try:
        if lang_code != "en":
            query_en = translator.translate(query, dest="en").text
        else:
            query_en = query
    except:
        query_en = query

    try:
        response = requests.post(
            "http://127.0.0.1:8000/api/chat",
            json={"query": query_en},
            timeout=300 
        )
        if response.status_code == 200:
            answer_en = response.json()["answer"]
            if lang_code != "en":
                try:
                    return translator.translate(answer_en, dest=lang_code).text
                except:
                    return answer_en
            return answer_en
        else:
            return "Server Error: Could not get a response."
    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to the backend server."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# --------------------------
# 10. HANDLE SUBMISSION
# --------------------------
if submit_button and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Chacha Chaudhary is thinking..."):
        answer = ask_backend(user_input, target_lang_code)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()