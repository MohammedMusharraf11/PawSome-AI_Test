import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="PawSome-AI", 
    page_icon="🐾", 
    layout="centered", 
    initial_sidebar_state="auto"
)

with st.sidebar:
    selected = option_menu(
        'PawSome AI',
        ['Welcome', 'Petcare', 'ChatBot','Prescription-Analyzer', 'About', 'Feedback'],
        icons=['house-door-fill', 'robot', 'chat-right-fill', 'file-earmark-break-fill', 'info', 'star'],
        menu_icon="🐶",
        default_index=0
    )

if selected == 'Welcome':
    import welcome
    welcome.welcome()


if selected == 'Petcare':
    import model
    model.model()


if selected == 'ChatBot':
    import chatbot
    chatbot.chatbot()

if selected == 'Prescription-Analyzer':
    import prescription
    prescription.presc_analyze()

