import streamlit as st
import uuid
from datetime import datetime
import textwrap
from st_audiorec import st_audiorec
import requests
import base64
import io

# --- URL BACKEND ---
CHATBOT_URL = "http://localhost:4096/answer"
WHISPER_URL = "http://localhost:8000/STT/"
TTS_URL = "http://localhost:8001/transcribe"

# --- Hàm gọi backend ---
def send_to_chatbot(prompt):
    try:
        res = requests.post(CHATBOT_URL, json={"prompt": prompt})
        if res.status_code == 200:
            return res.json().get("response", "Không có phản hồi.")
        else:
            return f"Lỗi chatbot: {res.status_code}"
    except Exception as e:
        return f"Lỗi gọi chatbot: {e}"

def speech_to_text(audio_bytes):
    try:
        files = {"file": ("audio.wav", audio_bytes, "audio/wav")}
        res = requests.post(WHISPER_URL, files=files)
        if res.status_code == 200:
            return res.json().get("output_text", "")
        return ""
    except Exception:
        return ""

def text_to_speech(text):
    try:
        res = requests.post(TTS_URL, data={"text_input": text})
        if res.status_code == 200:
            audio_base64 = res.json().get("output_sound")
            return base64.b64decode(audio_base64)
        return None
    except Exception:
        return None

# --- Setup Page ---
st.set_page_config(page_title="Chatbot", layout="wide")

# --- Initialize Session State ---
if "chats" not in st.session_state:
    st.session_state.chats = {}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None
if "show_recorder" not in st.session_state:
    st.session_state.show_recorder = False
if "last_audio" not in st.session_state:
    st.session_state.last_audio = None

# --- Sidebar ---
with st.sidebar:
    st.title("Lịch sử Chat")

    if st.button("Cuộc trò chuyện mới"):
        new_chat_id = str(uuid.uuid4())
        st.session_state.chats[new_chat_id] = {
            "title": "Cuộc trò chuyện mới",
            "messages": [],
            "created_at": datetime.now().strftime("%H:%M %d-%m-%Y")
        }
        st.session_state.current_chat = new_chat_id

    st.markdown("---")

    for chat_id, chat_data in st.session_state.chats.items():
        label = chat_data["title"]

        if st.button(label="", key=chat_id):
            st.session_state.current_chat = chat_id

        st.markdown(
            f"""
            <div style="
                display: flex;
                align-items: center;
                gap: 0.25rem;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                font-size: 15px;
                padding: 0.25rem 0.5rem;
                border: 1px solid #DDD;
                border-radius: 6px;
                margin-bottom: 5px;
                background-color: #f9f9f9;
            " title="{label}">
                <span>{label}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

# --- Main Chat Interface ---
st.markdown("<h1 style='text-align: center;'>Chatbot</h1>", unsafe_allow_html=True)

if st.session_state.current_chat is None:
    st.info("Hãy nhấn 'Cuộc trò chuyện mới' để bắt đầu.")
else:
    chat = st.session_state.chats[st.session_state.current_chat]

    # Hiển thị các tin nhắn đã gửi
    for msg in chat["messages"]:
        with st.chat_message(msg["role"]):
            if msg.get("type") == "audio":
                st.audio(msg["content"], format="audio/wav")
            else:
                st.markdown(msg["content"])

    # --- Input + Mic Button ---
    col1, col2 = st.columns([8, 1])
    with col1:
        prompt = st.chat_input("Nhập câu hỏi...")
    with col2:
        if st.button("Mic", use_container_width=True):
            st.session_state.show_recorder = not st.session_state.show_recorder

    # --- Xử lý nhập văn bản ---
    if prompt:
        chat["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if len(chat["messages"]) == 1:
            first_line = prompt.strip().split("\n")[0]
            short_title = textwrap.shorten(first_line, width=40, placeholder="...")
            chat["title"] = short_title or "Cuộc trò chuyện"

        response = send_to_chatbot(prompt)
        chat["messages"].append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

            audio = text_to_speech(response)
            if audio:
                st.audio(audio, format="audio/wav")

    # --- Giao diện ghi âm nhỏ gọn ---
    if st.session_state.show_recorder:
        with st.container():
            st.markdown("Ghi âm")

            audio_data = st_audiorec()

            if audio_data:
                st.session_state.last_audio = audio_data
                st.audio(audio_data, format="audio/wav")

                if st.button("Gửi"):
                    chat["messages"].append({
                        "role": "user",
                        "content": audio_data,
                        "type": "audio"
                    })
                    with st.chat_message("user"):
                        st.audio(audio_data, format="audio/wav")

                    text_transcribed = speech_to_text(audio_data)

                    if text_transcribed:
                        chat["messages"].append({
                            "role": "user",
                            "content": f"(Từ ghi âm): {text_transcribed}"
                        })
                        with st.chat_message("user"):
                            st.markdown(text_transcribed)

                        response = send_to_chatbot(text_transcribed)
                        chat["messages"].append({"role": "assistant", "content": response})
                        with st.chat_message("assistant"):
                            st.markdown(response)

                            audio = text_to_speech(response)
                            if audio:
                                st.audio(audio, format="audio/wav")

                    st.session_state.last_audio = None
                    st.session_state.show_recorder = False
