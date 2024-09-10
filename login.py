import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
import json
import requests


# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate("cyberpunk-3a6a6-78a93eb47ae4.json")
    firebase_admin.initialize_app(cred)

def app():
    # Custom CSS to change the input text color
    st.markdown(
        """
        <style>
        input {
            color: black !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title('Welcome to :violet[All Safe] :sunglasses:')

    # Rest of your code...
    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''

    def sign_up_with_email_and_password(email, password, username=None, return_secure_token=True):
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": return_secure_token
            }
            if username:
                payload["displayName"] = username 
            payload = json.dumps(payload)
            r = requests.post(rest_api_url, params={"key": "AIzaSyApr-etDzcGcsVcmaw7R7rPxx3A09as7uw"}, data=payload)
            response = r.json()
            if "error" in response:
                st.warning(f"Signup failed: {response['error']['message']}")
            else:
                return response['email']
        except Exception as e:
            st.warning(f'Signup failed: {e}')

    def sign_in_with_email_and_password(email=None, password=None, return_secure_token=True):
        rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

        try:
            payload = {
                "returnSecureToken": return_secure_token
            }
            if email:
                payload["email"] = email
            if password:
                payload["password"] = password
            payload = json.dumps(payload)
            r = requests.post(rest_api_url, params={"key": "AIzaSyApr-etDzcGcsVcmaw7R7rPxx3A09as7uw"}, data=payload)
            response = r.json()
            if "error" in response:
                st.warning(f"Signin failed: {response['error']['message']}")
            else:
                user_info = {
                    'email': response['email'],
                    'username': response.get('displayName', 'Unknown User')  # Retrieve username if available
                }
                return user_info
        except Exception as e:
            st.warning(f'Signin failed: {e}')

    def reset_password(email):
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"
            payload = {
                "email": email,
                "requestType": "PASSWORD_RESET"
            }
            payload = json.dumps(payload)
            r = requests.post(rest_api_url, params={"key": "AIzaSyCUhGCBwCOW4NaxlWTfBrn8_zqJGMWqKKg"}, data=payload)
            response = r.json()
            if r.status_code == 200:
                st.success("Password reset email sent successfully.")
            else:
                st.warning(f"Password reset failed: {response.get('error', {}).get('message')}")
        except Exception as e:
            st.warning(f"Password reset failed: {e}")

    def f(): 
        try:
            userinfo = sign_in_with_email_and_password(st.session_state.email_input, st.session_state.password_input)
            if userinfo:
                st.session_state.username = userinfo['username']
                st.session_state.useremail = userinfo['email']
                st.session_state.signedout = True
                st.session_state.signout = True    
        except: 
            st.warning('Login Failed')

    def t():
        st.session_state.signout = False
        st.session_state.signedout = False   
        st.session_state.username = ''

    def forget():
        email = st.text_input('Email')
        if st.button('Send Reset Link'):
            reset_password(email)

    if "signedout" not in st.session_state:
        st.session_state["signedout"] = False
    if 'signout' not in st.session_state:
        st.session_state['signout'] = False    

    if not st.session_state["signedout"]:
        choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')
        st.session_state.email_input = email
        st.session_state.password_input = password

        if choice == 'Sign up':
            username = st.text_input("Enter your unique username")
            if st.button('Create my account'):
                user = sign_up_with_email_and_password(email=email, password=password, username=username)
                if user:
                    st.success('Account created successfully!')
                    st.markdown('Please Login using your email and password')
                    st.balloons()
        else:
            st.button('Login', on_click=f)
            forget()

    if st.session_state.signout:
        st.text(f'Name: {st.session_state.username}')
        st.text(f'Email id: {st.session_state.useremail}')
        st.button('Sign out', on_click=t)

    def ap():
        st.write('Posts')

if __name__ == "__main__":
    app()
