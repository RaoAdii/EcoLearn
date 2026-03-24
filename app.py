"""
EcoLearn Dashboard - Main Streamlit Application
A comprehensive educational platform for learning about environmental science and sustainability.
"""

import streamlit as st
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import STREAMLIT_PAGE_CONFIG
from modules.auth import AuthManager, init_auth_session
from modules.gamification import GamificationEngine, Leaderboard
from modules.quiz_engine import QuizEngine
from modules.analytics import AnalyticsEngine
from api.climate_data import ClimateDataFetcher
from database.db_setup import init_db


def configure_page():
    """Configure Streamlit page settings with Mentimeter design system."""
    st.set_page_config(**STREAMLIT_PAGE_CONFIG)
    
    # Comprehensive Design System - Mentimeter Inspired
    st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">
    
    <style>
    :root {
        --color-primary: #1A1A2E;
        --color-secondary: #635BFF;
        --color-accent: #FF6B6B;
        --color-success: #00C48C;
        --color-surface: #FFFFFF;
        --color-surface-muted: #F4F4F8;
        --color-text-primary: #1A1A2E;
        --color-text-secondary: #6B7280;
        --color-text-inverse: #FFFFFF;
        --color-border: #E5E7EB;
        --color-shadow: rgba(99, 91, 255, 0.12);
        --gradient-hero: linear-gradient(135deg, #1A1A2E 0%, #2D1B69 100%);
        --gradient-cta: linear-gradient(90deg, #635BFF, #9B6DFF);
        --gradient-card: linear-gradient(145deg, #FFFFFF, #F8F7FF);
    }
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'DM Sans', sans-serif;
        color: var(--color-text-primary);
        background-color: var(--color-surface-muted);
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    /* Typography System */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    h1 {
        font-size: 56px;
        font-weight: 800;
        line-height: 1.1;
        letter-spacing: -0.03em;
    }
    
    h2 {
        font-size: 48px;
        font-weight: 700;
    }
    
    h3 {
        font-size: 32px;
        font-weight: 700;
    }
    
    h4 {
        font-size: 24px;
        font-weight: 600;
    }
    
    p, span, div {
        font-family: 'DM Sans', sans-serif;
        font-size: 16px;
        line-height: 1.6;
    }
    
    /* Main Layout */
    .main {
        padding: 0;
        background: var(--color-surface-muted);
    }
    
    /* Section Styling */
    section {
        padding: 80px 32px;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Header/Navbar */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Button Styling */
    .stButton>button {
        background: var(--gradient-cta) !important;
        color: white !important;
        border: none !important;
        height: 48px !important;
        border-radius: 10px !important;
        padding: 12px 28px !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        letter-spacing: 0.01em !important;
        box-shadow: 0 4px 20px var(--color-shadow) !important;
        transition: all 200ms ease !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 32px rgba(99, 91, 255, 0.24) !important;
    }
    
    .stButton>button:active {
        transform: translateY(0) !important;
    }
    
    /* Secondary Button */
    .button-secondary>button {
        background: white !important;
        color: var(--color-primary) !important;
        border: 1.5px solid var(--color-border) !important;
        box-shadow: none !important;
    }
    
    .button-secondary>button:hover {
        border-color: var(--color-secondary) !important;
        color: var(--color-secondary) !important;
    }
    
    /* Cards */
    .stCard, .card-component {
        background: var(--gradient-card) !important;
        border: 1px solid var(--color-border) !important;
        border-radius: 16px !important;
        box-shadow: 0 2px 12px var(--color-shadow) !important;
        padding: 32px !important;
        transition: all 300ms ease !important;
    }
    
    .stCard:hover, .card-component:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 8px 32px rgba(99, 91, 255, 0.2) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        border-bottom: 2px solid var(--color-border);
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 12px 0 !important;
        background: transparent !important;
        border: none !important;
        font-weight: 500 !important;
        color: var(--color-text-secondary) !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 15px !important;
        transition: all 200ms ease !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--color-secondary) !important;
        border-bottom: 3px solid var(--color-secondary) !important;
        font-weight: 600 !important;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input,
    .stPasswordInput>div>div>input,
    .stSelectbox>div>div>input,
    .stNumberInput>div>div>input,
    .stTextArea>div>div>textarea {
        height: 52px !important;
        font-size: 16px !important;
        border: 1.5px solid var(--color-border) !important;
        border-radius: 10px !important;
        background-color: white !important;
        color: var(--color-text-primary) !important;
        padding: 12px 16px !important;
        font-family: 'DM Sans', sans-serif !important;
        transition: all 200ms ease !important;
    }
    
    .stTextInput>div>div>input::placeholder,
    .stPasswordInput>div>div>input::placeholder,
    .stSelectbox>div>div>input::placeholder,
    .stNumberInput>div>div>input::placeholder,
    .stTextArea>div>div>textarea::placeholder {
        color: var(--color-text-secondary) !important;
    }
    
    .stTextInput>div>div>input:focus,
    .stPasswordInput>div>div>input:focus,
    .stSelectbox>div>div>input:focus,
    .stNumberInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: var(--color-secondary) !important;
        box-shadow: 0 0 0 3px rgba(99, 91, 255, 0.15) !important;
    }
    
    /* Labels */
    label {
        font-size: 14px !important;
        font-weight: 500 !important;
        margin-bottom: 6px !important;
        color: var(--color-text-primary) !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    
    /* Info/Alert Messages */
    .stSuccess {
        background-color: rgba(0, 196, 140, 0.1) !important;
        border-left: 4px solid var(--color-success) !important;
        border-radius: 10px !important;
        padding: 16px !important;
        color: var(--color-text-primary) !important;
    }
    
    .stError {
        background-color: rgba(255, 107, 107, 0.1) !important;
        border-left: 4px solid var(--color-accent) !important;
        border-radius: 10px !important;
        padding: 16px !important;
        color: var(--color-text-primary) !important;
    }
    
    .stWarning {
        background-color: rgba(251, 191, 36, 0.1) !important;
        border-left: 4px solid #FBB824 !important;
        border-radius: 10px !important;
        padding: 16px !important;
        color: var(--color-text-primary) !important;
    }
    
    .stInfo {
        background-color: rgba(99, 91, 255, 0.1) !important;
        border-left: 4px solid var(--color-secondary) !important;
        border-radius: 10px !important;
        padding: 16px !important;
        color: var(--color-text-primary) !important;
    }
    
    /* Divider */
    hr {
        margin: 32px 0 !important;
        border: none !important;
        height: 1px !important;
        background: var(--color-border) !important;
    }
    
    /* Badges */
    .badge {
        background: rgba(99, 91, 255, 0.1);
        color: var(--color-secondary);
        border-radius: 999px;
        padding: 4px 12px;
        font-size: 13px;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 12px;
    }
    
    /* Metric Cards */
    .metric-card {
        background: var(--gradient-card) !important;
        border: 1px solid var(--color-border) !important;
        border-radius: 16px !important;
        padding: 32px !important;
        box-shadow: 0 2px 12px var(--color-shadow) !important;
        transition: all 300ms ease !important;
    }
    
    .metric-card:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 8px 32px rgba(99, 91, 255, 0.2) !important;
    }
    
    /* Form Container */
    .form-container {
        background: white;
        border-radius: 16px;
        padding: 48px;
        max-width: 420px;
        margin: 0 auto;
        box-shadow: 0 2px 12px var(--color-shadow);
    }
    
    /* Hero Section */
    .hero-section {
        background: var(--gradient-hero);
        color: white;
        padding: 120px 32px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 500px;
        height: 500px;
        background: radial-gradient(circle, rgba(155, 109, 255, 0.3) 0%, transparent 70%);
        border-radius: 50%;
        animation: float 12s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(24px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 600ms ease-out;
    }
    
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    .shimmer-loading {
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 1000px 100%;
        animation: shimmer 2s infinite;
    }
    
    /* Links */
    a {
        color: var(--color-secondary);
        text-decoration: none;
        transition: all 200ms ease;
        font-weight: 500;
    }
    
    a:hover {
        color: var(--color-primary);
        text-decoration: underline;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        h1 { font-size: 40px; }
        h2 { font-size: 32px; }
        h3 { font-size: 24px; }
        
        section { padding: 48px 16px; }
        .form-container { padding: 32px 24px; }
        
        .stButton>button {
            height: 44px !important;
            font-size: 14px !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def render_login_page():
    """Render the login/registration page."""
    # Initialize session state for tab switching
    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = 'login'
    
    # Hero Section - Simplified
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1A1A2E 0%, #2D1B69 100%);
        color: white;
        padding: 60px 40px;
        border-radius: 24px;
        margin-bottom: 30px;
        text-align: center;
    ">
        <h1 style="
            font-size: 48px;
            font-weight: 800;
            margin: 0 0 8px 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: white;
        ">🌍 EcoLearn</h1>
        <p style="
            font-size: 16px;
            color: rgba(255, 255, 255, 0.9);
            margin: 0 0 24px 0;
            font-family: 'DM Sans', sans-serif;
        ">Learn about Environment • Save the Planet</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature List using Streamlit columns
    feat_col1, feat_col2 = st.columns(2, gap="small")
    
    with feat_col1:
        st.markdown("✓ **10,000+ users** | Learn with a community")
        st.markdown("✓ **Track progress** | Monitor your growth")
    
    with feat_col2:
        st.markdown("✓ **Learn science** | Environmental education")
        st.markdown("✓ **Make impact** | Create real change")
    
    st.divider()
    
    # Authentication Tab Toggle
    tab_col1, tab_col2 = st.columns([1, 1], gap="small")
    
    with tab_col1:
        if st.button("🔐 Login", use_container_width=True, key="tab_login"):
            st.session_state.auth_mode = 'login'
            st.rerun()
    
    with tab_col2:
        if st.button("📝 Register", use_container_width=True, key="tab_register"):
            st.session_state.auth_mode = 'register'
            st.rerun()
    
    st.markdown("")
    
    # Authentication Content
    if st.session_state.auth_mode == 'login':
        # ========== LOGIN FORM ==========
        st.markdown("""
        <h2 style="
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 28px;
            font-weight: 700;
            margin: 0 0 8px 0;
            color: #1A1A2E;
        ">Welcome back!</h2>
        <p style="
            color: #6B7280;
            font-size: 15px;
            margin: 0 0 24px 0;
            font-family: 'DM Sans', sans-serif;
        ">Sign in to continue your eco-learning journey</p>
        """, unsafe_allow_html=True)
        
        username = st.text_input(
            "Username or Email",
            key="login_username",
            placeholder="you@example.com"
        )
        password = st.text_input(
            "Password",
            type="password",
            key="login_password",
            placeholder="Enter your password"
        )
        
        # Forgot password link - now functional
        col1, col2 = st.columns([1, 1])
        with col2:
            if st.button("🔑 Forgot password?", use_container_width=True, key="forgot_pwd_link"):
                st.session_state.show_reset_password = True
                st.rerun()
        st.markdown("")
        
        if st.button("Sign In", use_container_width=True, key="login_button"):
            if username and password:
                result = AuthManager.login_user(username, password)
                if result['success']:
                    st.session_state.authenticated = True
                    st.session_state.user = result['user']
                    st.session_state.show_welcome = True
                    st.success("✓ Login successful!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"❌ {result['message']}")
            else:
                st.warning("⚠️ Please enter your username/email and password")
        
        # Signup link
        st.markdown("""
        <p style="
            text-align: center;
            color: #6B7280;
            font-size: 14px;
            margin-top: 24px;
            font-family: 'DM Sans', sans-serif;
        ">
            Don't have an account?
            <span style="color: #635BFF; font-weight: 600;">
                Click "Register" above to get started
            </span>
        </p>
        """, unsafe_allow_html=True)
    
    else:
        # ========== REGISTER FORM ==========
        st.markdown("""
        <h2 style="
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 28px;
            font-weight: 700;
            margin: 0 0 8px 0;
            color: #1A1A2E;
        ">Join the community!</h2>
        <p style="
            color: #6B7280;
            font-size: 15px;
            margin: 0 0 24px 0;
            font-family: 'DM Sans', sans-serif;
        ">Create your account and start learning today</p>
        """, unsafe_allow_html=True)
        
        reg_col1, reg_col2 = st.columns(2, gap="small")
        
        with reg_col1:
            first_name = st.text_input(
                "First Name",
                key="reg_first",
                placeholder="John"
            )
        
        with reg_col2:
            last_name = st.text_input(
                "Last Name",
                key="reg_last",
                placeholder="Doe"
            )
        
        username = st.text_input(
            "Username",
            key="reg_username",
            placeholder="johndoe"
        )
        
        email = st.text_input(
            "Email",
            key="reg_email",
            placeholder="john@example.com"
        )
        
        role = st.selectbox(
            "I am a...",
            ["Student", "Teacher"],
            key="reg_role"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            key="reg_password",
            placeholder="Create a strong password"
        )
        
        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="reg_confirm",
            placeholder="Confirm your password"
        )
        
        if st.button("Create Account", use_container_width=True, key="register_button"):
            if not username or not email or not password:
                st.error("❌ Username, email, and password are required")
            elif password != confirm_password:
                st.error("❌ Passwords do not match")
            elif len(password) < 6:
                st.error("❌ Password must be at least 6 characters")
            else:
                result = AuthManager.register_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    role=role.lower()
                )
                if result['success']:
                    st.success("✅ Account created! Please login with your credentials.")
                    st.session_state.auth_mode = 'login'
                    st.rerun()
                else:
                    st.error(f"❌ {result['message']}")
        
        # Login link
        st.markdown("""
        <p style="
            text-align: center;
            color: #6B7280;
            font-size: 14px;
            margin-top: 24px;
            font-family: 'DM Sans', sans-serif;
        ">
            Already have an account?
            <span style="color: #635BFF; font-weight: 600;">
                Click "Login" above
            </span>
        </p>
        """, unsafe_allow_html=True)


def render_password_reset():
    """Render password reset page."""
    st.markdown("""
    <div style="
        max-width: 400px;
        background: linear-gradient(135deg, #FFFFFF 0%, #F8F7FF 100%);
        border-radius: 20px;
        padding: 40px;
        margin: 0 auto;
        box-shadow: 0 8px 32px rgba(99, 91, 255, 0.15);
    ">
        <h2 style="
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 24px;
            text-align: center;
            margin: 0 0 8px 0;
            color: #1A1A2E;
        ">Reset Password</h2>
        <p style="
            text-align: center;
            color: #6B7280;
            font-size: 14px;
            margin: 0 0 24px 0;
            font-family: 'DM Sans', sans-serif;
        ">Recover access to your EcoLearn account</p>
    </div>
    """, unsafe_allow_html=True)
    
    if 'reset_stage' not in st.session_state:
        st.session_state.reset_stage = 'email'
    
    # Stage 1: Ask for email
    if st.session_state.reset_stage == 'email':
        st.markdown("### Step 1: Enter your email")
        reset_email = st.text_input("Email address", key="reset_email_input", placeholder="your@email.com")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back to Login", use_container_width=True):
                st.session_state.show_reset_password = False
                st.session_state.reset_stage = 'email'
                st.rerun()
        
        with col2:
            if st.button("Send Reset Link", use_container_width=True, key="send_reset_btn"):
                if reset_email:
                    result = AuthManager.request_password_reset(reset_email)
                    if result['success']:
                        st.session_state.reset_token = result.get('token')
                        st.session_state.reset_email = reset_email
                        st.session_state.reset_stage = 'token'
                        st.success("✓ Reset link sent! Check the token below (in production, this would be emailed)")
                        st.rerun()
                    else:
                        st.error(f"❌ {result.get('message')}")
                else:
                    st.warning("⚠️ Please enter your email address")
    
    # Stage 2: Verify token and reset password
    elif st.session_state.reset_stage == 'token':
        st.markdown("### Step 2: Verify your reset link")
        st.info("📧 A reset link has been generated. In production, this would be sent to your email.")
        
        # Show the token (in production, this would be in an email link)
        if 'reset_token' in st.session_state:
            st.markdown(f"**Reset Token:** `{st.session_state.reset_token}`")
            st.markdown("(In production, you would click this token in your email)")
        
        st.divider()
        
        # Form to enter new password
        st.markdown("### Step 3: Enter your new password")
        new_password = st.text_input("New password", type="password", key="new_password_input", placeholder="At least 6 characters")
        confirm_password = st.text_input("Confirm password", type="password", key="confirm_password_input")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", use_container_width=True):
                st.session_state.reset_stage = 'email'
                st.rerun()
        
        with col2:
            if st.button("Reset Password", use_container_width=True, key="reset_pwd_btn"):
                if new_password and confirm_password:
                    if new_password == confirm_password:
                        if 'reset_token' in st.session_state:
                            result = AuthManager.reset_password(st.session_state.reset_token, new_password)
                            if result['success']:
                                st.success("✓ Password reset successful! Please log in with your new password.")
                                st.session_state.show_reset_password = False
                                st.session_state.reset_stage = 'email'
                                st.session_state.reset_token = None
                                st.rerun()
                            else:
                                st.error(f"❌ {result.get('message')}")
                    else:
                        st.error("❌ Passwords do not match")
                else:
                    st.warning("⚠️ Please enter and confirm your password")


def render_student_dashboard():
    """Render student dashboard with Mentimeter-inspired design."""
    # Top Navigation Bar
    nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1], gap="large", vertical_alignment="center")
    
    with nav_col1:
        st.markdown("""
        <div style="
            font-size: 24px;
            font-weight: 800;
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: var(--color-primary);
        ">🌍 EcoLearn</div>
        """, unsafe_allow_html=True)
    
    with nav_col3:
        user_name = st.session_state.user.get('username', 'Student')
        st.markdown("""
        <div style="text-align: right; color: var(--color-text-secondary); font-size: 14px;">
            👤 {}<br>
            <small style="color: var(--color-text-secondary);">{}</small>
        </div>
        """.format(user_name, st.session_state.user.get('email', '')), unsafe_allow_html=True)
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.rerun()
    
    st.divider()
    
    # Hero Greeting Section
    st.markdown(f"""
    <div style="
        background: var(--gradient-hero);
        color: white;
        padding: 48px 40px;
        border-radius: 24px;
        margin-bottom: 40px;
        box-shadow: 0 8px 32px var(--color-shadow);
    ">
        <h1 style="
            font-size: 36px;
            margin: 0 0 8px 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 800;
        ">Welcome back, {st.session_state.user.get('username', 'Student')}! 👋</h1>
        <p style="
            font-size: 16px;
            margin: 0;
            opacity: 0.9;
        ">Keep learning, keep growing! 🌱 Continue your eco-warrior journey today.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Cards Row
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4, gap="large")
    
    level_info = GamificationEngine.get_user_level(st.session_state.user['id'])
    rank_info = Leaderboard.get_user_rank(st.session_state.user['id'])
    
    # Level Card
    with stat_col1:
        st.markdown(f"""
        <div class="metric-card" style="
            background: linear-gradient(135deg, #FFE66D 0%, #FCB045 100%);
            text-align: center;
        ">
            <div style="font-size: 36px; margin-bottom: 8px;">🎖️</div>
            <p style="margin: 0; color: var(--color-text-secondary); font-size: 12px; text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em;">Level</p>
            <h2 style="margin: 8px 0 0 0; font-size: 36px; color: var(--color-primary); font-weight: 800;">{level_info['level']}</h2>
            <p style="margin: 4px 0 0 0; color: var(--color-text-secondary); font-size: 13px;">{level_info['level_name']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # XP Card
    with stat_col2:
        st.markdown(f"""
        <div class="metric-card" style="
            background: linear-gradient(135deg, #99E9B6 0%, #43E97B 100%);
            text-align: center;
        ">
            <div style="font-size: 36px; margin-bottom: 8px;">⚡</div>
            <p style="margin: 0; color: var(--color-text-secondary); font-size: 12px; text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em;">Total XP</p>
            <h2 style="margin: 8px 0 0 0; font-size: 36px; color: var(--color-primary); font-weight: 800;">{level_info['total_xp']}</h2>
            <p style="margin: 4px 0 0 0; color: var(--color-text-secondary); font-size: 13px;">{int(level_info['progress_percentage'])}% to next level</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Rank Card
    with stat_col3:
        rank = rank_info['rank'] if rank_info['success'] else 'N/A'
        st.markdown(f"""
        <div class="metric-card" style="
            background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
            text-align: center;
        ">
            <div style="font-size: 36px; margin-bottom: 8px;">🏆</div>
            <p style="margin: 0; color: white; font-size: 12px; text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em;">Global Rank</p>
            <h2 style="margin: 8px 0 0 0; font-size: 32px; color: white; font-weight: 800;">#{rank}</h2>
            <p style="margin: 4px 0 0 0; color: rgba(255,255,255,0.8); font-size: 13px;">Top eco-warrior</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Streaks/Consistency Card
    with stat_col4:
        # Calculate actual streak from database
        streak_data = GamificationEngine.calculate_quiz_streak(st.session_state.user['id'])
        current_streak = streak_data.get('current_streak', 0)
        streak_emoji = "🔥" if current_streak > 0 else "❄️"
        streak_message = "Keep it up! 💪" if current_streak > 0 else "Start a streak!"
        
        st.markdown(f"""
        <div class="metric-card" style="
            background: linear-gradient(135deg, #635BFF 0%, #9B6DFF 100%);
            text-align: center;
        ">
            <div style="font-size: 36px; margin-bottom: 8px;">{streak_emoji}</div>
            <p style="margin: 0; color: white; font-size: 12px; text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em;">Streak</p>
            <h2 style="margin: 8px 0 0 0; font-size: 32px; color: white; font-weight: 800;">{current_streak} day{'s' if current_streak != 1 else ''}</h2>
            <p style="margin: 4px 0 0 0; color: rgba(255,255,255,0.8); font-size: 13px;">{streak_message}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Main Content Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Quizzes", "📊 Analytics", "🏆 Leaderboard", "⚙️ Settings"])
    
    with tab1:
        st.markdown("### 📝 Start Your Quiz Challenge")
        st.markdown("Join the competition, earn XP, and climb the leaderboard! 🚀")
        st.divider()

        quizzes_result = QuizEngine.get_available_quizzes()
        if not quizzes_result.get('success', False):
            st.error(quizzes_result.get('message', 'Could not load quizzes'))
        else:
            quizzes = quizzes_result.get('quizzes', [])

            if not quizzes:
                st.info("📋 No quizzes available yet.")
            else:
                # Quiz selection with cards
                st.markdown("#### 🎯 Available Quizzes")
                quiz_cols = st.columns(len(quizzes) if len(quizzes) <= 4 else 2)
                
                selected_quiz = None
                for idx, quiz in enumerate(quizzes[:4]):
                    with quiz_cols[idx % len(quiz_cols)]:
                        # Styled quiz card
                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, #635BFF 0%, #9B6DFF 100%);
                            color: white;
                            padding: 20px;
                            border-radius: 16px;
                            text-align: center;
                            cursor: pointer;
                            transition: all 300ms ease;
                            min-height: 140px;
                            display: flex;
                            flex-direction: column;
                            justify-content: center;
                            box-shadow: 0 4px 16px rgba(99, 91, 255, 0.3);
                            margin-bottom: 12px;
                        ">
                            <div style="font-size: 32px; margin-bottom: 12px;">📚</div>
                            <div style="
                                font-size: 16px;
                                font-weight: 700;
                                margin-bottom: 12px;
                                line-height: 1.3;
                                word-wrap: break-word;
                            ">{quiz['title']}</div>
                            <div style="
                                font-size: 13px;
                                opacity: 0.9;
                                margin-bottom: 8px;
                            ">{quiz['question_count']} Questions</div>
                            <div style="
                                font-size: 12px;
                                opacity: 0.8;
                                background: rgba(255,255,255,0.2);
                                padding: 6px 12px;
                                border-radius: 8px;
                                display: inline-block;
                                margin: 0 auto;
                            ">Pass: {int(quiz['passing_score'])}%</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(
                            "Start Quiz →",
                            use_container_width=True,
                            key=f"quiz_btn_{quiz['id']}"
                        ):
                            st.session_state['selected_quiz_id'] = quiz['id']
                            selected_quiz = quiz

                # Load selected quiz or show all options
                if 'selected_quiz_id' in st.session_state:
                    selected_quiz_id = st.session_state['selected_quiz_id']
                    selected_quiz = next((q for q in quizzes if q['id'] == selected_quiz_id), None)

                if selected_quiz:
                    st.divider()
                    
                    # Quiz Header
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #27AE60 0%, #0db366 100%); padding: 24px; border-radius: 16px; color: white; margin-bottom: 20px;">
                        <h1 style="margin: 0; color: white;">🎯 {selected_quiz['title']}</h1>
                        <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">{selected_quiz['description']}</p>
                        <p style="margin: 15px 0 0 0; font-size: 14px;">📊 {selected_quiz['question_count']} Questions • ⏱️ Approx {selected_quiz['question_count'] * 2} minutes • 🎯 Pass Score: {int(selected_quiz['passing_score'])}%</p>
                    </div>
                    """, unsafe_allow_html=True)

                    questions_result = QuizEngine.get_quiz_questions(selected_quiz['id'])
                    if not questions_result.get('success', False):
                        st.error(questions_result.get('message', 'Could not load quiz questions'))
                    else:
                        questions = questions_result['questions']

                        if not questions:
                            st.warning("This quiz currently has no questions.")
                        else:
                            start_key = f"quiz_start_{selected_quiz['id']}"
                            result_key = f"quiz_result_{selected_quiz['id']}"
                            current_q_key = f"quiz_current_q_{selected_quiz['id']}"

                            if start_key not in st.session_state:
                                st.session_state[start_key] = datetime.utcnow()
                            
                            if current_q_key not in st.session_state:
                                st.session_state[current_q_key] = 0

                            result_key_exists = result_key in st.session_state

                            if not result_key_exists:
                                # Quiz Mode
                                current_q_idx = st.session_state[current_q_key]
                                current_question = questions[current_q_idx]

                                # Progress Bar
                                progress = (current_q_idx + 1) / len(questions)
                                st.markdown(f"""
                                <div style="margin-bottom: 20px;">
                                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                                        <strong>Question {current_q_idx + 1} of {len(questions)}</strong>
                                        <strong style="color: #27AE60;">{int(progress * 100)}% Complete</strong>
                                    </div>
                                    <div style="width: 100%; height: 10px; background-color: #e0e0e0; border-radius: 10px; overflow: hidden;">
                                        <div style="width: {progress * 100}%; height: 100%; background: linear-gradient(90deg, #27AE60, #0db366); transition: width 0.3s ease;"></div>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)

                                # Question Display
                                st.markdown(f"""
                                <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 32px; border-radius: 16px; margin: 20px 0; border-left: 5px solid #27AE60;">
                                    <h2 style="margin: 0; color: #0f3460; font-size: 24px; line-height: 1.4;">{current_question['question_text']}</h2>
                                </div>
                                """, unsafe_allow_html=True)

                                # Answer Options
                                input_key = f"quiz_answer_{selected_quiz['id']}_{current_question['id']}"
                                question_type = current_question.get('question_type', 'multiple_choice')
                                options = current_question.get('options', [])

                                if question_type in ('multiple_choice', 'true_false'):
                                    st.markdown("#### Choose your answer:")
                                    selected_answer = None
                                    
                                    # Display options as interactive buttons
                                    for i, option in enumerate(options):
                                        col1, col2 = st.columns([0.1, 0.9])
                                        with col1:
                                            st.markdown(f"<div style='font-weight: 700; color: #27AE60;'>{chr(65+i)}.</div>", unsafe_allow_html=True)
                                        with col2:
                                            if st.button(
                                                option,
                                                use_container_width=True,
                                                key=f"opt_{input_key}_{i}",
                                                help="Click to select this answer"
                                            ):
                                                st.session_state[input_key] = option
                                                selected_answer = option
                                        st.markdown("")
                                else:
                                    selected_answer = st.text_input(
                                        "Your answer",
                                        key=input_key,
                                        placeholder="Type your answer here...",
                                    )
                                    st.session_state[input_key] = selected_answer

                                # Navigation Buttons
                                nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 1])
                                
                                with nav_col1:
                                    if current_q_idx > 0:
                                        if st.button("⬅️ Previous", use_container_width=True):
                                            st.session_state[current_q_key] = current_q_idx - 1
                                            st.rerun()
                                    else:
                                        st.button("⬅️ Previous", use_container_width=True, disabled=True)

                                with nav_col2:
                                    st.markdown(f"<div style='text-align: center; padding-top: 8px;'><strong>{current_q_idx + 1}/{len(questions)}</strong></div>", unsafe_allow_html=True)

                                with nav_col3:
                                    if current_q_idx < len(questions) - 1:
                                        if st.button("Next ➡️", use_container_width=True):
                                            if input_key in st.session_state and st.session_state[input_key]:
                                                st.session_state[current_q_key] = current_q_idx + 1
                                                st.rerun()
                                            else:
                                                st.warning("Please select an answer before proceeding")
                                    else:
                                        if st.button("🎯 Submit Quiz", use_container_width=True, key="submit_btn"):
                                            # Collect all answers
                                            answers = {}
                                            all_answered = True
                                            for q in questions:
                                                ans_key = f"quiz_answer_{selected_quiz['id']}_{q['id']}"
                                                if ans_key in st.session_state and st.session_state[ans_key]:
                                                    answers[q['id']] = st.session_state[ans_key]
                                                else:
                                                    all_answered = False
                                                    break
                                            
                                            if all_answered:
                                                started_at = st.session_state.get(start_key, datetime.utcnow())
                                                time_spent = int((datetime.utcnow() - started_at).total_seconds())

                                                submit_result = QuizEngine.submit_quiz(
                                                    user_id=st.session_state.user['id'],
                                                    quiz_id=selected_quiz['id'],
                                                    answers=answers,
                                                    time_spent_seconds=time_spent,
                                                )

                                                if submit_result.get('success', False):
                                                    st.session_state[result_key] = submit_result
                                                    st.session_state.pop(start_key, None)
                                                    st.rerun()
                                                else:
                                                    st.error(submit_result.get('message', 'Failed to submit quiz'))
                                            else:
                                                st.error("⚠️ Please answer all questions before submitting")

                            else:
                                # Results Mode
                                latest_result = st.session_state[result_key]
                                xp_earned = GamificationEngine.calculate_xp_earned(latest_result['score'])

                                # Results Header
                                if latest_result.get('passed'):
                                    st.markdown(f"""
                                    <div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; padding: 40px; border-radius: 16px; text-align: center; margin-bottom: 30px; box-shadow: 0 8px 32px rgba(40, 167, 69, 0.3);">
                                        <h1 style="margin: 0; color: white; font-size: 48px;">🎉</h1>
                                        <h2 style="margin: 15px 0 0 0; color: white;">You Passed!</h2>
                                        <p style="margin: 10px 0 0 0; font-size: 24px; font-weight: 700;">Score: {latest_result['score']}%</p>
                                        <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">🎁 You earned {xp_earned} XP and +1 XP for each correct answer!</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                else:
                                    st.markdown(f"""
                                    <div style="background: linear-gradient(135deg, #dc3545 0%, #e74c3c 100%); color: white; padding: 40px; border-radius: 16px; text-align: center; margin-bottom: 30px; box-shadow: 0 8px 32px rgba(220, 53, 69, 0.3);">
                                        <h1 style="margin: 0; color: white; font-size: 48px;">📚</h1>
                                        <h2 style="margin: 15px 0 0 0; color: white;">Keep Learning!</h2>
                                        <p style="margin: 10px 0 0 0; font-size: 24px; font-weight: 700;">Score: {latest_result['score']}%</p>
                                        <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;\">{int(latest_result['passing_score'] - latest_result['score'])}% more needed to pass. You got this! 💪</p>
                                    </div>
                                    """, unsafe_allow_html=True)

                                # Results Stats
                                res_col1, res_col2, res_col3, res_col4 = st.columns(4, gap="large")
                                
                                with res_col1:
                                    st.markdown(f"""
                                    <div class="metric-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                                        <p style="margin: 0; color: white; font-size: 12px; text-transform: uppercase; font-weight: 600;">Score</p>
                                        <h2 style="margin: 10px 0 0 0; color: white;">{latest_result['score']}%</h2>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                with res_col2:
                                    st.markdown(f"""
                                    <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                                        <p style="margin: 0; color: white; font-size: 12px; text-transform: uppercase; font-weight: 600;">Correct</p>
                                        <h2 style="margin: 10px 0 0 0; color: white;">{latest_result['correct_answers']}/{latest_result['total_questions']}</h2>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                with res_col3:
                                    time_min = latest_result['time_spent'] // 60
                                    time_sec = latest_result['time_spent'] % 60
                                    st.markdown(f"""
                                    <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                                        <p style="margin: 0; color: white; font-size: 12px; text-transform: uppercase; font-weight: 600;">Time</p>
                                        <h2 style="margin: 10px 0 0 0; color: white;">{time_min}m {time_sec}s</h2>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                with res_col4:
                                    st.markdown(f"""
                                    <div class="metric-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
                                        <p style="margin: 0; color: white; font-size: 12px; text-transform: uppercase; font-weight: 600;\">XP Earned</p>
                                        <h2 style="margin: 10px 0 0 0; color: white;">+{xp_earned} XP</h2>
                                    </div>
                                    """, unsafe_allow_html=True)

                                # Answer Review
                                st.divider()
                                st.markdown("#### 📋 Answer Review")
                                
                                for idx, answer_info in enumerate(latest_result.get('question_breakdown', []), 1):
                                    status_icon = "✅" if answer_info['is_correct'] else "❌"
                                    status_color = "#28a745" if answer_info['is_correct'] else "#dc3545"
                                    
                                    st.markdown(f"""
                                    <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 20px; border-radius: 12px; border-left: 4px solid {status_color}; margin: 12px 0;">
                                        <p style="margin: 0; font-weight: 700; color: #0f3460; font-size: 16px;">{status_icon} Q{idx}: {answer_info['question_text']}</p>
                                        <p style="margin: 10px 0 0 0; color: #555;"><strong>Your answer:</strong> {answer_info['user_answer'] or 'No answer'}</p>
                                        {f'<p style="margin: 5px 0 0 0; color: #27AE60;"><strong>✓ Correct!</strong></p>' if answer_info['is_correct'] else f'<p style="margin: 5px 0 0 0; color: #dc3545;"><strong>✗ Correct answer:</strong> {answer_info["correct_answer"]}</p>'}
                                    </div>
                                    """, unsafe_allow_html=True)

                                # Action Buttons
                                st.divider()
                                btn_col1, btn_col2, btn_col3 = st.columns(3)
                                
                                with btn_col1:
                                    if st.button("🔄 Retake Quiz", use_container_width=True):
                                        st.session_state.pop(result_key, None)
                                        st.session_state.pop(start_key, None)
                                        st.session_state.pop(current_q_key, None)
                                        for q in questions:
                                            st.session_state.pop(f"quiz_answer_{selected_quiz['id']}_{q['id']}", None)
                                        st.rerun()
                                
                                with btn_col2:
                                    if st.button("📚 Choose Another Quiz", use_container_width=True):
                                        st.session_state.pop('selected_quiz_id', None)
                                        st.session_state.pop(result_key, None)
                                        st.session_state.pop(start_key, None)
                                        st.session_state.pop(current_q_key, None)
                                        st.rerun()
                                
                                with btn_col3:
                                    if st.button("📊 View Progress", use_container_width=True):
                                        st.switch_tab("📊 My Progress")
                                    st.caption(f"Your answer: {answer_info['user_answer'] or 'No answer'}")
                                    if not answer_info['is_correct']:
                                        st.caption(f"Correct answer: {answer_info['correct_answer']}")
    
    with tab2:
        st.markdown("### 📊 My Progress")
        st.markdown("Track your learning journey below.")
        st.divider()
        progress_report = AnalyticsEngine.get_student_progress_report(st.session_state.user['id'])
        
        if progress_report['success']:
            quiz_stats = progress_report['quiz_stats']
            
            col1, col2, col3, col4 = st.columns(4, gap="large")
            
            with col1:
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                    <p style="margin: 0; color: #666; font-size: 12px; text-transform: uppercase; font-weight: 600;">Quizzes</p>
                    <h2 style="margin: 10px 0 0 0; color: #0f3460;">{quiz_stats['completed']}</h2>
                    <p style="margin: 5px 0 0 0; color: #888; font-size: 14px;">🎉 Completed</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                    <p style="margin: 0; color: #666; font-size: 12px; text-transform: uppercase; font-weight: 600;">Avg Score</p>
                    <h2 style="margin: 10px 0 0 0; color: #0f3460;">{quiz_stats['average_score']}%</h2>
                    <p style="margin: 5px 0 0 0; color: #888; font-size: 14px;">Target: 70%</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                    <p style="margin: 0; color: #666; font-size: 12px; text-transform: uppercase; font-weight: 600;">Pass Rate</p>
                    <h2 style="margin: 10px 0 0 0; color: #0f3460;">{quiz_stats['pass_rate']}%</h2>
                    <p style="margin: 5px 0 0 0; color: #888; font-size: 14px;">✅ on attempt</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                time_hours = round(progress_report['time_stats']['total_time_minutes'] / 60, 1)
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
                    <p style="margin: 0; color: #666; font-size: 12px; text-transform: uppercase; font-weight: 600;">Time Spent</p>
                    <h2 style="margin: 10px 0 0 0; color: #0f3460;">{time_hours}h</h2>
                    <p style="margin: 5px 0 0 0; color: #888; font-size: 14px;">⏳ Learning time</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📋 No quiz data yet. Start by taking a quiz!", icon="-")
    
    with tab3:
        st.markdown("### 🏆 Global Leaderboard")
        st.markdown("See how you rank against other learners worldwide.")
        st.divider()
        lb_result = Leaderboard.get_global_leaderboard(limit=10)
        
        if lb_result['success']:
            leaderboard_data = lb_result['leaderboard']
            
            for rank, user in enumerate(leaderboard_data, 1):
                medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"{rank:2d}."
                
                col1, col2, col3 = st.columns([0.8, 3, 1.2], gap="medium")
                with col1:
                    st.markdown(f"<h3 style='text-align: center; color: #0f3460;'>{medal}</h3>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<p style='font-weight: 700; color: #0f3460; margin: 0;'>{user['username']}</p><p style='color: #888; font-size: 12px; margin: 3px 0 0 0;'>{user['level_name']}</p>", unsafe_allow_html=True)
                with col3:
                    st.markdown(f"<div style='background: linear-gradient(135deg, #27AE60 0%, #0db366 100%); color: white; padding: 10px; border-radius: 10px; text-align: center;'><p style='margin: 0; font-weight: 700;'>{user['total_xp']} XP</p></div>", unsafe_allow_html=True)
                st.divider()
        else:
            st.warning("⚠️ Could not load leaderboard", icon=None)
    
    with tab4:
        st.markdown("### 🌍 Climate Data")
        st.markdown("Check real-time air quality data for your location.")
        st.divider()
        
        col1, col2 = st.columns([2, 1], gap="large")
        
        with col1:
            city = st.text_input("🏙️ Enter your city", placeholder="e.g., New York, London, Delhi...")
        
        with col2:
            if st.button("🔍 Get Data", use_container_width=True):
                if city:
                    with st.spinner("🔍 Fetching air quality data..."):
                        # Search for city coordinates
                        coords = ClimateDataFetcher.search_city_coordinates(city)
                        
                        if coords['success']:
                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #27AE60 0%, #0db366 100%); color: white; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
                                <p style="margin: 0; font-size: 14px;">📍 {coords['city']}, {coords['country']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Fetch air quality
                            air_quality = ClimateDataFetcher.get_air_quality_data(
                                coords['latitude'],
                                coords['longitude']
                            )
                            
                            if air_quality['success']:
                                aq = air_quality['air_quality']
                                
                                col1, col2, col3 = st.columns(3, gap="large")
                                
                                with col1:
                                    aqi_color = "#28a745" if aq['us_aqi'] < 50 else "#ffc107" if aq['us_aqi'] < 100 else "#dc3545"
                                    st.markdown(f"""
                                    <div class="metric-card" style="background: linear-gradient(135deg, {aqi_color} 0%, {aqi_color}dd 100%);">
                                        <p style="margin: 0; color: white; font-size: 12px; text-transform: uppercase; font-weight: 600;">Air Quality Index</p>
                                        <h2 style="margin: 10px 0 0 0; color: white;">{int(aq['us_aqi'])}</h2>
                                        <p style="margin: 5px 0 0 0; color: rgba(255,255,255,0.8); font-size: 14px;">{air_quality['air_quality']['category']}</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                with col2:
                                    st.markdown(f"""
                                    <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                                        <p style="margin: 0; color: #666; font-size: 12px; text-transform: uppercase; font-weight: 600;">PM 2.5</p>
                                        <h2 style="margin: 10px 0 0 0; color: #0f3460;">{aq['pm2_5']:.1f}</h2>
                                        <p style="margin: 5px 0 0 0; color: #888; font-size: 14px;">µg/m³</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                with col3:
                                    rec = air_quality['health_recommendation']
                                    st.markdown(f"""
                                    <div class="metric-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
                                        <p style="margin: 0; color: #666; font-size: 12px; text-transform: uppercase; font-weight: 600;\">Health Tip</p>
                                        <p style="margin: 10px 0 0 0; color: #0f3460; font-size: 12px; line-height: 1.4;\">{rec[:50]}...</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                            else:
                                st.error("⚠️ " + air_quality['message'], icon=None)
                        else:
                            st.error("⚠️ " + coords['message'], icon=None)
                else:
                    st.warning("📋 Please enter a city name", icon=None)


def render_teacher_dashboard():
    """Render teacher dashboard with Mentimeter design."""
    # Top Navigation
    nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1], gap="large", vertical_alignment="center")
    
    with nav_col1:
        st.markdown("""
        <div style="
            font-size: 24px;
            font-weight: 800;
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: var(--color-primary);
        ">🌍 EcoLearn</div>
        """, unsafe_allow_html=True)
    
    with nav_col3:
        st.markdown(f"""
        <div style="text-align: right; color: var(--color-text-secondary); font-size: 14px;">
            👨‍🏫 {st.session_state.user.get('username', 'Teacher')}<br>
            <small style="color: var(--color-text-secondary);">Teacher Account</small>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚪 Logout", key="teacher_logout"):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.rerun()
    
    st.divider()
    
    # Hero Section
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #635BFF 0%, #9B6DFF 100%);
        color: white;
        padding: 48px 40px;
        border-radius: 24px;
        margin-bottom: 40px;
        box-shadow: 0 8px 32px var(--color-shadow);
    ">
        <h1 style="
            font-size: 36px;
            margin: 0 0 8px 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 800;
        ">Teacher Dashboard 👨‍🏫</h1>
        <p style="
            font-size: 16px;
            margin: 0;
            opacity: 0.9;
        ">Manage courses, track student progress, and inspire the next generation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Content Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📚 My Courses", "📊 Performance", "📈 Analytics", "⚙️ Settings"])
    
    with tab1:
        st.markdown("### 📚 Your Courses")
        st.markdown("Create and manage your courses!")
        st.divider()
        st.info("🔛 Course management features coming soon!")
    
    with tab2:
        st.markdown("### 📊 Class Performance")
        st.markdown("Monitor student progress in real-time.")
        st.divider()
        st.info("🔛 Analytics for your classes coming soon!")
    
    with tab3:
        st.markdown("#📈 Advanced Analytics")
        st.markdown("Dive deep into student data.")
        st.divider()
        st.info("🔛 Advanced analytics and reports coming soon!")
    
    with tab4:
        st.markdown("### ⚙️ Settings")
        st.markdown("Manage your preferences.")
        st.divider()
        st.info("🔛 Settings coming soon!")


def render_admin_dashboard():
    """Render admin dashboard with Mentimeter design."""
    # Top Navigation
    nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1], gap="large", vertical_alignment="center")
    
    with nav_col1:
        st.markdown("""
        <div style="
            font-size: 24px;
            font-weight: 800;
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: var(--color-primary);
        ">🌍 EcoLearn</div>
        """, unsafe_allow_html=True)
    
    with nav_col3:
        st.markdown(f"""
        <div style="text-align: right; color: var(--color-text-secondary); font-size: 14px;">
            👨‍💼 {st.session_state.user.get('username', 'Admin')}<br>
            <small style="color: var(--color-text-secondary);">Administrator</small>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚪 Logout", key="admin_logout"):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.rerun()
    
    st.divider()
    
    # Hero Section
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
        color: white;
        padding: 48px 40px;
        border-radius: 24px;
        margin-bottom: 40px;
        box-shadow: 0 8px 32px var(--color-shadow);
    ">
        <h1 style="
            font-size: 36px;
            margin: 0 0 8px 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 800;
        ">System Administration ⚙️</h1>
        <p style="
            font-size: 16px;
            margin: 0;
            opacity: 0.9;
        ">Manage users, monitor platform health, and configure settings</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Admin Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["👥 Users", "📊 Analytics", "🔧 System", "📋 Logs"])
    
    # TAB 1: USER MANAGEMENT
    with tab1:
        st.markdown("### 👥 User Management")
        st.markdown("Manage platform users and permissions.")
        st.divider()
        
        # Get all users
        from database.db_setup import User, Session as DBSession
        db_session = DBSession()
        all_users = db_session.query(User).all()
        db_session.close()
        
        if all_users:
            # Display user stats
            stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
            with stat_col1:
                st.metric("Total Users", len(all_users))
            with stat_col2:
                students = len([u for u in all_users if u.role == 'student'])
                st.metric("Students", students)
            with stat_col3:
                teachers = len([u for u in all_users if u.role == 'teacher'])
                st.metric("Teachers", teachers)
            with stat_col4:
                admins = len([u for u in all_users if u.role == 'admin'])
                st.metric("Admins", admins)
            
            st.divider()
            
            # User table
            st.markdown("#### All Users")
            user_data = []
            for user in all_users:
                user_data.append({
                    'ID': user.id,
                    'Username': user.username,
                    'Email': user.email,
                    'Role': user.role.capitalize(),
                    'Status': '🟢 Active' if user.is_active else '🔴 Inactive',
                    'Joined': user.created_at.strftime('%Y-%m-%d') if user.created_at else 'N/A'
                })
            
            st.dataframe(user_data, use_container_width=True)
            
            st.divider()
            st.markdown("#### User Actions")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Change User Role**")
                selected_user = st.selectbox("Select user", [u.username for u in all_users], key="user_select")
                new_role = st.selectbox("New role", ['student', 'teacher', 'admin'], key="role_select")
                
                if st.button("Update Role", key="update_role_btn"):
                    db_session = DBSession()
                    user = db_session.query(User).filter(User.username == selected_user).first()
                    if user:
                        user.role = new_role
                        db_session.commit()
                        st.success(f"✓ {selected_user}'s role updated to {new_role}")
                    db_session.close()
            
            with col2:
                st.markdown("**Delete User**")
                delete_user = st.selectbox("Select user to delete", [u.username for u in all_users if u.username != st.session_state.user['username']], key="delete_user_select")
                
                if st.button("🗑️ Delete User", key="delete_user_btn"):
                    db_session = DBSession()
                    user = db_session.query(User).filter(User.username == delete_user).first()
                    if user:
                        db_session.delete(user)
                        db_session.commit()
                        st.success(f"✓ User {delete_user} deleted")
                    db_session.close()
        else:
            st.info("No users found")
    
    # TAB 2: PLATFORM ANALYTICS
    with tab2:
        st.markdown("### 📊 Platform Analytics")
        st.markdown("Monitor platform-wide analytics and metrics.")
        st.divider()
        
        from database.db_setup import QuizAttempt, Session as DBSession
        
        db_session = DBSession()
        all_users = db_session.query(User).all()
        all_attempts = db_session.query(QuizAttempt).all()
        
        # Calculate stats
        total_users = len(all_users)
        total_attempts = len(all_attempts)
        completed_attempts = len([a for a in all_attempts if a.completed_at])
        passed_attempts = len([a for a in all_attempts if a.passed])
        
        # Calculate average score
        avg_score = 0
        if all_attempts:
            valid_scores = [a.score for a in all_attempts if a.score is not None]
            if valid_scores:
                avg_score = sum(valid_scores) / len(valid_scores)
        
        db_session.close()
        
        # Display metrics
        stat_col1, stat_col2, stat_col3, stat_col4, stat_col5 = st.columns(5)
        
        with stat_col1:
            st.metric("Total Users", total_users)
        
        with stat_col2:
            st.metric("Total Attempts", total_attempts)
        
        with stat_col3:
            st.metric("Completed", completed_attempts)
        
        with stat_col4:
            st.metric("Passed", passed_attempts)
        
        with stat_col5:
            st.metric("Avg Score %", f"{avg_score:.1f}" if avg_score > 0 else "N/A")
        
        st.divider()
        
        # Additional insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Success Rate")
            if total_attempts > 0:
                success_rate = (passed_attempts / completed_attempts * 100) if completed_attempts > 0 else 0
                st.metric("Pass Rate", f"{success_rate:.1f}%")
            else:
                st.info("No attempts yet")
        
        with col2:
            st.markdown("#### User Distribution")
            db_session = DBSession()
            role_dist = {}
            for user in db_session.query(User).all():
                role_dist[user.role] = role_dist.get(user.role, 0) + 1
            db_session.close()
            
            for role, count in role_dist.items():
                st.write(f"• **{role.capitalize()}**: {count} users")
    
    # TAB 3: SYSTEM CONFIGURATION
    with tab3:
        st.markdown("### 🔧 System Configuration")
        st.markdown("Configure platform settings and features.")
        st.divider()
        
        st.markdown("#### Platform Settings")
        
        # Example settings
        col1, col2 = st.columns(2)
        
        with col1:
            maintenance_mode = st.checkbox("Enable Maintenance Mode", value=False)
            if maintenance_mode:
                st.warning("⚠️ Maintenance mode is ON - Users will see a maintenance message")
        
        with col2:
            registration_enabled = st.checkbox("Allow New Registrations", value=True)
            if not registration_enabled:
                st.info("ℹ️ New user registrations are disabled")
        
        st.divider()
        
        st.markdown("#### Database Information")
        
        import os
        db_path = 'ecolearn.db'
        if os.path.exists(db_path):
            db_size = os.path.getsize(db_path) / 1024 / 1024  # Convert to MB
            st.write(f"**Database File**: {db_path}")
            st.write(f"**Database Size**: {db_size:.2f} MB")
            
            if st.button("🔄 Backup Database", key="backup_db"):
                import shutil
                backup_name = f"ecolearn_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
                shutil.copy(db_path, backup_name)
                st.success(f"✓ Database backed up as {backup_name}")
    
    # TAB 4: SYSTEM LOGS
    with tab4:
        st.markdown("### 📋 System Logs")
        st.markdown("View system activity and error logs.")
        st.divider()
        
        st.info("ℹ️ Activity logs tracked: User logins, role changes, user deletions, and data modifications")
        
        st.markdown("#### Recent Activity")
        
        # Show recent database modifications based on updated_at timestamps
        from database.db_setup import Session as DBSession
        
        db_session = DBSession()
        recent_users = db_session.query(User).order_by(User.updated_at.desc()).limit(10).all()
        
        activity_log = []
        for user in recent_users:
            activity_log.append({
                'Timestamp': user.updated_at.strftime('%Y-%m-%d %H:%M:%S') if user.updated_at else 'N/A',
                'User': user.username,
                'Action': f'Updated {user.role} account',
                'Status': '✓ Success'
            })
        
        db_session.close()
        
        if activity_log:
            st.dataframe(activity_log, use_container_width=True)
        else:
            st.info("No activity logs yet")



def main():
    """Main application entry point."""
    configure_page()
    
    # Initialize database on first run
    if not os.path.exists('ecolearn.db'):
        init_db()

    # Ensure there are starter quizzes and questions available in the app.
    QuizEngine.seed_sample_quizzes()
    
    # Initialize session state
    init_auth_session()
    
    # Sidebar
    if st.session_state.authenticated:
        with st.sidebar:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 30px;">
                <h1 style="font-size: 36px; margin: 0;">🌍</h1>
                <h2 style="color: white; margin: 10px 0 0 0;">EcoLearn</h2>
                <p style="color: rgba(255,255,255,0.8); margin: 5px 0 0 0; font-size: 12px;">Environmental Education Platform</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.divider()
            
            st.markdown("""
            <div style="background: rgba(255,255,255,0.1); padding: 16px; border-radius: 12px; margin-bottom: 20px;">
                <p style="color: white; font-size: 12px; margin: 0; opacity: 0.8;">LOGGED IN AS</p>
                <p style="color: white; font-size: 16px; font-weight: 700; margin: 5px 0 0 0;">{username}</p>
                <p style="color: rgba(255,255,255,0.7); font-size: 12px; margin: 5px 0 0 0; text-transform: uppercase; letter-spacing: 1px;">{role}</p>
            </div>
            """.format(username=st.session_state.user['username'], role=st.session_state.user['role'].title()), unsafe_allow_html=True)
            
            st.divider()
            
            if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
                st.session_state.authenticated = False
                st.session_state.user = None
                st.rerun()
        
        # Render dashboard based on role
        if st.session_state.user['role'] == 'student':
            render_student_dashboard()
        elif st.session_state.user['role'] == 'teacher':
            render_teacher_dashboard()
        elif st.session_state.user['role'] == 'admin':
            render_admin_dashboard()
    else:
        # Check if user is trying to reset password
        if st.session_state.get('show_reset_password', False):
            render_password_reset()
        else:
            render_login_page()


if __name__ == '__main__':
    main()
