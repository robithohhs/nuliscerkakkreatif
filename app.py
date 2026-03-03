import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import base64

# 1. Konfigurasi API Gemini (Dapatkan di aistudio.google.com)
genai.configure(api_key="ISI_API_KEY_ANDA_DI_SINI")
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🎭 Wicara Tokoh Cerkak")
st.write("Wawancarai tokohmu lan rungokno suarane!")

# 2. Pengaturan Karakter (System Prompt)
system_prompt = "Kowe dadi Mbah Karso, tukang kebon sekolah sing misterius. Ngomongo nganggo basa Jawa Ngoko Alus."

if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilan Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input Siswa
if prompt := st.chat_input("Mangga badhe nyuwun pirsa napa?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respon AI
    with st.chat_message("assistant"):
        full_prompt = f"{system_prompt}\nPertanyaan Siswa: {prompt}"
        response = model.generate_content(full_prompt)
        jawaban_jawa = response.text
        st.markdown(jawaban_jawa)
        
        # 3. Mengubah Teks ke Suara (gTTS)
        tts = gTTS(text=jawaban_jawa, lang='jv') # 'jv' untuk Bahasa Jawa
        tts.save("respon.mp3")
        
        # Memutar audio otomatis di browser
        audio_file = open("respon.mp3", "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3", autoplay=True)

    st.session_state.messages.append({"role": "assistant", "content": jawaban_jawa})
