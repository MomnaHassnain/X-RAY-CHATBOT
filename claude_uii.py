import streamlit as st
import requests
from PIL import Image
import base64
import io

# API Configuration
API_URL = "http://34.172.140.11:8080/predict"

# Page Configuration
st.set_page_config(
    page_title="EMRChains - Medical AI Assistant", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
        color: white;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit default elements */
    .stDeployButton {display: none;}
    #MainMenu {visibility: hidden;}
    .stHeader {display: none;}
    footer {visibility: hidden;}
    
    /* Header Styling */
    .main-header {
        background: rgba(0, 0, 0, 0.9);
        backdrop-filter: blur(20px);
        padding: 1rem 2rem;
        border-bottom: 1px solid rgba(0, 255, 132, 0.2);
        margin: -1rem -1rem 2rem -1rem;
        position: sticky;
        top: 0;
        z-index: 100;
    }
    
    .header-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .logo {
        font-size: 1.8rem;
        font-weight: 700;
        color: #00ff84;
        text-decoration: none;
    }
    
    .nav-links {
        display: flex;
        gap: 2rem;
        margin: 0;
        padding: 0;
        list-style: none;
    }
    
    .nav-link {
        color: #ffffff;
        text-decoration: none;
        opacity: 0.8;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .nav-link:hover {
        opacity: 1;
        color: #00ff84;
    }
    
    /* Main Title */
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        margin: 2rem 0 1rem 0;
        background: linear-gradient(45deg, #00ff84, #00cc6a);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .subtitle {
        text-align: center;
        opacity: 0.8;
        margin-bottom: 3rem;
        font-size: 1.2rem;
        font-weight: 400;
    }
    
    /* Language Selector */
    .language-section {
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .stSelectbox > div > div {
        background: rgba(0, 255, 132, 0.1) !important;
        border: 2px solid #00ff84 !important;
        border-radius: 8px !important;
        color: white !important;
    }
    
    /* Upload Section */
    .upload-container {
        background: rgba(0, 40, 26, 0.6);
        border: 2px dashed rgba(0, 255, 132, 0.3);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        margin-bottom: 2rem;
    }
    
    .upload-container:hover {
        border-color: #00ff84;
        background: rgba(0, 40, 26, 0.8);
    }
    
    .upload-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .upload-text {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #00ff84;
    }
    
    .upload-subtext {
        opacity: 0.7;
        font-size: 1rem;
        margin-bottom: 1rem;
    }
    
    /* File Uploader Styling */
    .stFileUploader > div > div {
        background: transparent !important;
        border: none !important;
    }
    
    .stFileUploader label {
        background: linear-gradient(45deg, #00ff84, #00cc6a) !important;
        color: #000 !important;
        border-radius: 8px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 600 !important;
        border: none !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader label:hover {
        transform: scale(1.05) !important;
    }
    
    /* Chat Section */
    .chat-container {
        background: rgba(0, 40, 26, 0.3);
        border: 1px solid rgba(0, 255, 132, 0.2);
        border-radius: 15px;
        backdrop-filter: blur(10px);
        height: 600px;
        display: flex;
        flex-direction: column;
    }
    
    .chat-header {
        padding: 1.5rem;
        border-bottom: 1px solid rgba(0, 255, 132, 0.2);
        background: rgba(0, 255, 132, 0.05);
        border-radius: 15px 15px 0 0;
    }
    
    .chat-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #00ff84;
        margin-bottom: 0.5rem;
    }
    
    .chat-subtitle {
        opacity: 0.8;
        font-size: 1rem;
    }
    
    .chat-messages {
        flex: 1;
        padding: 1.5rem;
        overflow-y: auto;
        max-height: 400px;
        background: rgba(0, 0, 0, 0.2);
    }
    
    .message-container {
        margin-bottom: 1.5rem;
        padding: 1rem;
        border-radius: 10px;
        animation: slideIn 0.3s ease;
    }
    
    .user-message {
        background: rgba(0, 255, 132, 0.1);
        border-left: 4px solid #00ff84;
        margin-left: 2rem;
    }
    
    .ai-message {
        background: rgba(255, 255, 255, 0.05);
        border-left: 4px solid #888;
        margin-right: 2rem;
    }
    
    .message-header {
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #00ff84;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .ai-message .message-header {
        color: #ffffff;
    }
    
    .message-content {
        line-height: 1.6;
        font-size: 1rem;
    }
    
    /* Input Section */
    .chat-input-section {
        padding: 1.5rem;
        border-top: 1px solid rgba(0, 255, 132, 0.2);
        background: rgba(0, 0, 0, 0.2);
        border-radius: 0 0 15px 15px;
    }
    
    .stTextInput > div > div > input {
        background: rgba(0, 0, 0, 0.5) !important;
        border: 2px solid rgba(0, 255, 132, 0.3) !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 1rem !important;
        font-size: 1rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #00ff84 !important;
        box-shadow: 0 0 10px rgba(0, 255, 132, 0.3) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #00ff84, #00cc6a) !important;
        color: #000 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 5px 15px rgba(0, 255, 132, 0.3) !important;
    }
    
    /* Quick Questions */
    .quick-questions {
        margin-top: 2rem;
        padding: 1.5rem;
        background: rgba(0, 40, 26, 0.3);
        border-radius: 10px;
        border: 1px solid rgba(0, 255, 132, 0.2);
    }
    
    .quick-title {
        color: #00ff84;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .question-btn {
        background: rgba(0, 255, 132, 0.1) !important;
        border: 1px solid rgba(0, 255, 132, 0.3) !important;
        color: white !important;
        margin: 0.3rem !important;
        padding: 0.6rem 1rem !important;
        border-radius: 6px !important;
        font-size: 0.9rem !important;
    }
    
    .question-btn:hover {
        background: rgba(0, 255, 132, 0.2) !important;
        border-color: #00ff84 !important;
    }
    
    /* Clear Button */
    .clear-btn {
        background: rgba(255, 100, 100, 0.2) !important;
        border: 1px solid rgba(255, 100, 100, 0.5) !important;
        color: #ff6464 !important;
        margin-top: 1rem !important;
        padding: 0.5rem 1rem !important;
        font-size: 0.9rem !important;
    }
    
    .clear-btn:hover {
        background: rgba(255, 100, 100, 0.3) !important;
    }
    
    /* Image Preview */
    .image-preview {
        margin-top: 1rem;
        border-radius: 10px;
        box-shadow: 0 10px 30px rgba(0, 255, 132, 0.2);
    }
    
    /* Success Message */
    .upload-success {
        color: #00ff84;
        font-weight: 600;
        margin-top: 1rem;
        font-size: 1rem;
    }
    
    /* Animations */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .nav-links {
            display: none;
        }
        
        .main-title {
            font-size: 2rem;
        }
        
        .chat-container {
            height: auto;
            min-height: 500px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header

# Main Title


# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None

st.markdown("<h1>EMRCHAINS</h1>", unsafe_allow_html=True)

# Main Interface Layout
col1, col2 = st.columns([1, 2])

# Left Column - Upload Section
with col1:
    st.markdown("""
    <div class="upload-container">
        <div class="upload-icon">📁</div>
        <div class="upload-text">Upload Medical Image</div>
        <div class="upload-subtext">Select X-ray, MRI, or CT scan</div>
        <div class="upload-subtext">Supports JPG, PNG, DICOM</div>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png", "dicom"], key="file_uploader")
    
    if uploaded_file:
        st.session_state.uploaded_image = uploaded_file
        image = Image.open(uploaded_file)
        st.image(image, caption="📷 Uploaded Medical Image", use_column_width=True, output_format="PNG")
        st.markdown('<p class="upload-success">✅ Image uploaded successfully</p>', unsafe_allow_html=True)
        
        # Add upload message to chat
    

# Right Column - Chat Section
# --- Right Column - Chat Section ---
with col2:
    # Chat input section
    st.markdown('<div class="chat-input-section">', unsafe_allow_html=True)

    input_col, btn_col = st.columns([4, 1])
    with input_col:
        user_input = st.text_input(
            "",
            placeholder="Ask anything about medical x-rays...",
            key="chat_input",
            label_visibility="collapsed"
        )
    with btn_col:
        send_clicked = st.button("Send", key="send_btn", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Handle Send Button
    if send_clicked and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        if st.session_state.uploaded_image:
            try:
                with st.spinner("Analyzing image with AI..."):
                    image_file = st.session_state.uploaded_image
                    image_bytes = image_file.getvalue()

                    import mimetypes
                    mime_type, _ = mimetypes.guess_type(image_file.name)
                    mime_type = mime_type or "image/jpeg"

                    files = {
                        "image": (image_file.name, image_bytes, mime_type)
                    }
                    data = {
                        "query": user_input
                    }

                    response = requests.post(API_URL, files=files, data=data)

                    if response.status_code == 200:
                        result = response.json()
                        ai_response = result.get("response", "").strip()
                    else:
                        ai_response = f"❌ API error {response.status_code}: {response.text}"

            except Exception as e:
                ai_response = f"❌ Unexpected error: {e}"

        else:
            ai_response = "⚠️ Please upload an image first."

        # ✅ Show messages inside the same block
        st.markdown("### 🧠 X-Ray Chatbot", unsafe_allow_html=True)
        st.markdown(f"**You:** {user_input}")
        st.markdown(f"**AI Assistant:** {ai_response}")
