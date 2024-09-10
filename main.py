import streamlit as st
import requests
import pandas as pd
import pythonwhois
import dns.resolver
import dns.reversename
import regex as re
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
from phish import phishing
from passchecker import PasswordStrengthChecker
from look_up import lookup

# Set page configuration
st.set_page_config(page_title="Allsafe - Cybersecurity Tools", page_icon="🔐", layout="wide")

# Function to apply local CSS styling
def localcss(filename):
    with open(filename) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

localcss("style.css")

# Add custom CSS for text input and file uploader
custom_css = """
<style>
/* Customize the text input box */
div.stTextInput > div > input {
    color: black; /* Change text color to black */
}

/* Customize the file uploader box */
div.stFileUploader > div > input {
    color: black; /* Change text color to black */
}

/* Optional: Change the border color and background of the input fields */
div.stTextInput > div > input {
    border: 2px solid #0077B5;
    background-color: #f0f0f0;
    border-radius: 4px;
    padding: 8px;
}
div.stFileUploader > div > input {
    border: 2px solid #0077B5;
    background-color: #f0f0f0;
    border-radius: 4px;
    padding: 8px;
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Background image and sidebar styling
pg_bg_img = f"""
<style>
[data-testid="stApp"] {{
background-image: url("https://i.imgur.com/vs1KasL.jpeg");
background-size: cover;
background-repeat: no-repeat;
background-attachment: local;
background-position: top left;
}}
[data-testid="stHeader"]{{
background-color: rgba(0,0,0,0);
}}

[data-testid="stSidebar"]{{
background-image : url("https://i.imgur.com/ZNSMsiR.jpeg");
background-size: cover;
}}
</style>
"""

st.markdown(pg_bg_img, unsafe_allow_html=True)

# Sidebar branding
c1, c2 = st.sidebar.columns(2)
with c1:
    st.markdown("""
        <style>
        .st-emotion-cache-1v0mbdj > img {
        border-radius: 40%;
        }
        </style>
        """, unsafe_allow_html=True)
    st.image("nsrit.jpeg")  # Replace with your project's logo

with c2:
    st.empty()

# Sidebar for navigation
st.sidebar.title("Allsafe - Cybersecurity Tools")

# Tool selection
tool_option = st.sidebar.selectbox("What would you like to do?", [
    "Menu", "Phishing Detector Tool", "Password Strength Checker", 
    "Bulk IP Address Translator", "Cybersecurity Blogs", 
    "Interactive Quizzes", 
])

# Main content area
if tool_option == "Menu":
    st.title("Allsafe - Cybersecurity Tools")
    st.header("Welcome to Allsafe!")
    st.write("""
        Allsafe is your go-to platform for learning and securing your digital presence. 
        Our tools are designed to help you stay safe online and keep up with the latest trends in cybersecurity.
    """)
    st.subheader("Objective")
    st.write("""
        The objective of Allsafe is to provide accessible tools and resources for users and students 
        to enhance their cybersecurity knowledge and protect themselves from online threats.
    """)

    # Footer for additional information
    st.markdown("""
    <div style="text-align: center; padding:50px;">
        <p>Made with ❤️ by the Allsafe Team</p>
        <p>Contact us at: contact@allsafe.com</p>
    </div>
    """, unsafe_allow_html=True)

elif tool_option == "Phishing Detector Tool":
    st.header("Phishing Detector Tool")
    def main():
        phish_instance = phishing()
        phish_instance.run()
    if __name__ == '__main__':
        main()

elif tool_option == "Password Strength Checker":
    st.header("Password Strength Checker")
    def main():
        phish_instance = PasswordStrengthChecker()
        phish_instance.run()
    if __name__ == '__main__':
        main()

elif tool_option == "Bulk IP Address Translator":
    st.header("Bulk IP Address Translator")
    def main():
        lookup_app = lookup()  # Instantiate the Notes class
        lookup_app.run()      # Run the Notes application
    if __name__ == "__main__":
        main()

elif tool_option == "Cybersecurity Blogs":
    st.header("Cybersecurity Blogs")
    # Add Cybersecurity Blogs code here

elif tool_option == "Interactive Quizzes":
    st.header("Interactive Quizzes")
    # Add Interactive Quizzes code here

# Footer with social links
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)

st.sidebar.markdown("""
<style>
.made-by {
    font-family: monospace;
    color: #0C2637;
    font-size: 30px;
    text-align: center;
}
.made-by-links {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    margin: 10px 0;
}
.made-by-link {
    margin: 5px;
    text-decoration: none;
    color: #0C2637;
    font-size: 18px;
    transition: color 0.3s ease;
}
.made-by-link:hover {
    color: #0077B5;
}
.made-by-link img {
    width: 24px;
    height: 24px;
    margin-right: 5px;
}
</style>

<div class="made-by">💙 Made by the Allsafe Team</div>
<div class="made-by-links">
    <a href="https://github.com/allsafeteam" target="_blank" class="made-by-link">
        <img src="https://img.icons8.com/ios-glyphs/30/000000/github.png"/> GitHub
    </a>
    <a href="https://www.linkedin.com/in/allsafe-team" target="_blank" class="made-by-link">
        <img src="https://img.icons8.com/ios-glyphs/30/000000/linkedin.png"/> LinkedIn
    </a>
    <a href="https://twitter.com/allsafe_team" target="_blank" class="made-by-link">
        <img src="https://img.icons8.com/ios-glyphs/30/000000/twitter.png"/> Twitter
    </a>
</div>
""", unsafe_allow_html=True)
