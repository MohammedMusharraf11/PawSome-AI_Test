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
        ['Welcome', 'Petcare', 'ChatBot', 'About', 'Feedback'],
        icons=['house-door-fill', 'robot', 'chat-right-fill', 'info', 'star'],
        menu_icon="🐶",
        default_index=0
    )

if selected == 'Welcome':
    import welcome
    welcome.welcome()

if selected == 'ChatBot':
    import chatbot
    st.info("ChatBot selected")  # Debug statement
    chatbot.chatbot()
