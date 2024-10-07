import streamlit as st
import requests
import sys
import os
import base64

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from backend.app.utils import text2speech
from backend.app.utils import text2speech

st.title("NCERT Physics RAG application")

uploaded_file = st.file_uploader("Upload a pdf file")
status=False

if uploaded_file:
    pdf_file={
        "file": (uploaded_file.name, uploaded_file, "application/pdf")
    }

    response = requests.post("http://127.0.0.1:8000/upload_pdf/", files=pdf_file)
    
    if response.status_code == 200:
        data = response.json()
        parsed_text=data["text"]
        st.write(parsed_text)
        status=True

    else:
        print(response)
        st.error("Failed to process the PDF. Please try again.")

if status:

    import time
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if not st.session_state.messages:
        initial_message = "Hello! How can I assist you?"
        st.session_state.messages.append({"role": "assistant", "content": initial_message})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        try:
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            def response_generator(prompt):
                response=requests.post("http://127.0.0.1:8000/query/", json={"query": prompt})
                if response.status_code==200:
                    data=response.json()["text"]

                    for word in data.split():
                        yield word + " "
                        time.sleep(0.05)

                    audio_path, audio_data, audio_base64 = text2speech.txt2speech(data)

                    with open(audio_path, "wb") as f:
                        f.write(audio_data)

                    audio_html = f"""
                        <audio autoplay>
                        <source src="data:audio/wav;base64,{audio_base64}" type="audio/wav">
                        Your browser does not support the audio element.
                        </audio>
                        """

                    audio_placeholder = st.empty()
                    audio_placeholder.markdown(audio_html, unsafe_allow_html=True)

                else:
                    print(response)
                    st.error("Failed to query the vector db")
                    return "Could not process !!!"
                
            with st.chat_message("assistant"):
                response = st.write_stream(response_generator(prompt))

            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"{e}")