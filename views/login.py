import streamlit as st
from game.user_manager import UserManager
from utils.state import navigate_to

def show():
    try:
        user_manager = UserManager()

        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        
        st.markdown('<h1 class="big-title">F1 Simulator</h1>', unsafe_allow_html=True)

        # Create three columns for centering the login form
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Login form
            username = st.text_input(
                "Username",
                placeholder="Username", 
                key="username_input",
                label_visibility="collapsed"
            )
            
            password = st.text_input(
                "Password",
                placeholder="Password",
                type="password",
                key="password_input",
                label_visibility="collapsed"
            )
            
            # Login button
            if st.button("Login", key="login_button", type="primary", use_container_width=True):
                if username and password:
                    if user_manager.verify_login(username, password):
                        st.session_state.user = username
                        st.session_state.is_logged_in = True
                        navigate_to('welcome')
                    else:
                        st.error("Invalid username or password")
                else:
                    st.warning("Please enter both username and password")

            st.markdown('<div class="login-divider">or</div>', unsafe_allow_html=True)
            
            # Sign up section
            if st.button("Sign Up", key="signup_button", type="secondary", use_container_width=True):
                if username and password:
                    if user_manager.create_user(username, password):
                        st.success("Account created! You can now log in.")
                        st.session_state.user = username
                        st.session_state.is_logged_in = True
                        navigate_to('welcome')
                    else:
                        st.error("Username already exists")
                else:
                    st.warning("Please enter both username and password")
        
        st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error in login view: {str(e)}")
        st.write("Debug info:", str(e))  # Temporary debug line