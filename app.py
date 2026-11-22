import streamlit as st
import requests, time
from datetime import datetime

st.set_page_config(page_title="heyyy 💗", page_icon="💗", layout="centered")

FIREBASE_URL = "https://heyyy-7de35-default-rtdb.asia-southeast1.firebasedatabase.app"

if "my_user" not in st.session_state: st.session_state.my_user = ""
if "current_chat" not in st.session_state: st.session_state.current_chat = ""
if "page" not in st.session_state: st.session_state.page = "login"

st.markdown("""
<style>
.stApp{background-color:#FFF0F5;}
header{visibility:hidden;} .block-container{padding:0 !important; max-width:450px; margin-top:0 !important;}
.stTextInput input{border-radius:25px !important; border:1.5px solid #FFB6C1 !important; background:white !important; padding:12px 15px !important;}
.stButton > button{background:#FF4D8D !important; color:white !important; border:none !important; border-radius:25px !important; font-weight:bold !important;}
.pink-header{background:#FF4D8D; color:white; padding:14px; display:flex; align-items:center; gap:10px;}
.pink-avatar{width:42px; height:42px; background:white; color:#FF4D8D; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:20px; font-weight:bold;}
.bubble-me{background:#FFC0D6; padding:8px 10px; border-radius:12px 0px 12px 12px; margin:6px 0 6px auto; max-width:80%; width:fit-content; box-shadow:0 1px 2px rgba(0,0,0,0.08); font-size:15px;}
.bubble-friend{background:white; padding:8px 10px; border-radius:0px 12px 12px 12px; margin:6px auto 6px 0; max-width:80%; width:fit-content; box-shadow:0 1px 2px rgba(0,0,0,0.08); font-size:15px; border:1px solid #FFE0E8;}
.time{font-size:10px; color:#888; text-align:right;}
.contact-card{background:white; padding:12px; border-radius:15px; margin:6px 8px; display:flex; align-items:center; gap:10px; border:1px solid #FFE0E8;}
.chat-bg{background-color:#FFE4EE; background-image: radial-gradient(#FFB6C1 1.5px, transparent 1.5px), radial-gradient(#FFC0D6 1px, transparent 1px); background-size:32px 32px, 20px 20px; min-height:400px; padding:10px;}
</style>
""", unsafe_allow_html=True)

def get_friends(username):
    try:
        r = requests.get(f"{FIREBASE_URL}/users/{username}/friends.json", timeout=5)
        d = r.json()
        return list(d.keys()) if d else []
    except: return []

def add_friend(me, fr):
    requests.put(f"{FIREBASE_URL}/users/{me}/friends/{fr}.json", json=True, timeout=5)
    requests.put(f"{FIREBASE_URL}/users/{fr}/friends/{me}.json", json=True, timeout=5)

def get_msgs(room):
    try:
        r = requests.get(f"{FIREBASE_URL}/chats/{room}.json", timeout=5)
        data = r.json()
        if not data: return [], {}
        msgs = list(data.values())
        msgs.sort(key=lambda x: x.get("ts",0))
        return msgs, data
    except: return [], {}

# ========== 1. LOGIN / CREATE ACCOUNT ==========
if st.session_state.page == "login":
    st.markdown("<div style='background:#FF4D8D; color:white; padding:30px 20px; text-align:center; border-radius:0 0 30px 30px;'><h1 style='margin:0;'>heyyy 💗</h1><p>Pink WhatsApp</p><p style='font-size:13px; opacity:0.9;'>🌸 💌 🧸 💗 🧸 💌 🌸</p></div>", unsafe_allow_html=True)
    st.write("")
    st.markdown("<h3 style='text-align:center; color:#FF4D8D;'>Create Account / Login</h3>", unsafe_allow_html=True)
    u = st.text_input("Nee username pettu", placeholder="ex: bhavya, juliet2422...")
    if st.button("Continue 💗"):
        if u.strip():
            st.session_state.my_user = u.strip().lower()
            st.session_state.page = "chats"
            st.rerun()
        else:
            st.warning("Username pettu Bhavya!")
    st.markdown("<p style='text-align:center; color:#aaa; font-size:12px;'>Username okkate account.<br>Friend kuda thana username tho login avvali.</p>", unsafe_allow_html=True)
    st.stop()

me = st.session_state.my_user

# ========== 2. CHATS LIST - MULTIPLE FRIENDS ==========
if st.session_state.page == "chats":
    st.markdown(f"<div class='pink-header'><div class='pink-avatar'>{me[0].upper()}</div><div style='flex:1;'><div style='font-weight:700; font-size:18px;'>heyyy 💗</div><div style='font-size:12px; opacity:0.9;'>@{me} • online</div></div><span>📷 &nbsp; ⋮</span></div>", unsafe_allow_html=True)
    st.markdown("<p style='padding:8px 12px; color:#FF4D8D; font-weight:bold;'>💬 Chats &nbsp; &nbsp; <span style='color:#aaa;'>Status &nbsp; Calls</span></p>", unsafe_allow_html=True)

    st.markdown("<div style='padding:0 10px;'><b>Add New Friend</b></div>", unsafe_allow_html=True)
    c1, c2 = st.columns([3,1])
    with c1:
        new_fr = st.text_input("Friend username", placeholder="Friend username...", label_visibility="collapsed", key="new_fr")
    with c2:
        if st.button("Add +"):
            if new_fr.strip().lower() != me and new_fr.strip():
                add_friend(me, new_fr.strip().lower())
                st.rerun()

    friends = get_friends(me)
    if not friends:
        st.markdown("<p style='text-align:center; color:#aaa; margin-top:30px;'>No chats yet...<br>Friend username add chesi<br>heyyy cheppu 👋💗</p>", unsafe_allow_html=True)
    for f in friends:
        colA, colB = st.columns([4,1])
        with colA:
            st.markdown(f"<div class='contact-card'><div class='pink-avatar' style='background:#FFC0D6;'>{f[0].upper()}</div><div><b>@{f}</b><br><span style='font-size:12px; color:#888;'>Tap to chat 💗</span></div></div>", unsafe_allow_html=True)
        with colB:
            st.write("")
            if st.button("Chat 💬", key=f"chat_{f}"):
                st.session_state.current_chat = f
                st.session_state.page = "chat"
                st.rerun()
    st.write("")
    if st.button("Logout"):
        st.session_state.page = "login"
        st.session_state.my_user = ""
        st.rerun()
    st.stop()

# ========== 3. SINGLE CHAT - WHATSAPP STYLE PINK ==========
if st.session_state.page == "chat":
    friend = st.session_state.current_chat
    st.markdown(f"<div class='pink-header'><span style='font-size:20px;'>←</span><div class='pink-avatar'>{friend[0].upper()}</div><div style='flex:1;'><div style='font-weight:700;'>@{friend}</div><div style='font-size:11px;'>online • last seen recently</div></div><span>📹 &nbsp; 📞</span></div>", unsafe_allow_html=True)

    users = sorted([me, friend])
    room = f"{users[0]}_{users[1]}"
    msgs, raw = get_msgs(room)

    st.markdown("<div class='chat-bg'>", unsafe_allow_html=True)
    if not msgs:
        st.markdown(f"<div style='text-align:center;'><div style='background:#FFF2C9; padding:8px; border-radius:8px; font-size:12px; display:inline-block;'>🔒 Messages are end-to-end encrypted 💗</div><p style='color:#C07A8A; font-size:13px; margin-top:15px;'>Say heyyy to @{friend} 👋</p></div>", unsafe_allow_html=True)
    for k, m in zip(raw.keys() if raw else [], msgs):
        is_me = m.get("from") == me
        if is_me:
            st.markdown(f"<div class='bubble-me'>{m['text']}<div class='time'>{m.get('time','')} <span style='color:#FF4D8D;'>✓✓</span></div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bubble-friend'>{m['text']}<div class='time'>{m.get('time','')}</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns([5,1])
    with c1:
        msg = st.text_input("Message", placeholder="Message... 💕", label_visibility="collapsed", key="pink_msg")
    with c2:
        if st.button("➤"):
            if msg:
                payload = {"from": me, "text": msg, "time": datetime.now().strftime("%I:%M %p"), "ts": int(time.time()*1000)}
                requests.post(f"{FIREBASE_URL}/chats/{room}.json", json=payload, timeout=5)
                st.rerun()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh"):
            st.rerun()
    with col2:
        if st.button("⬅ Back to Chats"):
            st.session_state.page = "chats"
            st.rerun()