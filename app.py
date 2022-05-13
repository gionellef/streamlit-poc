import streamlit as st
from multiapp import MultiApp
from apps import home, student, admin_finance


st.set_page_config(
    "UPM Executive Dashboard",
    "📊",
    initial_sidebar_state="expanded",
    layout="wide",
)
app = MultiApp()

# Add all your application here
app.add_app("Home", home.app)
app.add_app("Student Affairs", student.app)
app.add_app("Administration and Finance", admin_finance.app)

# The main app
app.run()


