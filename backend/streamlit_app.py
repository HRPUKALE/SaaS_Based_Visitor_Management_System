import streamlit as st
from assistant_core import run_assistant
import time

# Page configuration
st.set_page_config(
    page_title="Kanishka Appointment Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid;
    }
    
    .user-message {
        background-color: #F397881;
        border-left-color: #2196f3;
        margin-left: 2rem;
    }
    
    .assistant-message {
        background-color: #F397881;
        border-left-color: #9c27b0;
        margin-right: 2rem;
    }
    
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        padding: 1rem;
        border-top: 1px solid #e0e0e0;
        z-index: 1000;
    }
    
    .chat-container {
        margin-bottom: 100px;
    }
    
    .success-box {
        background: linear-gradient(90deg, #4caf50, #45a049);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #5a6fd8 0%, #6a4190 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "state" not in st.session_state:
    st.session_state.state = None
if "confirmed" not in st.session_state:
    st.session_state.confirmed = False
if "booking_json" not in st.session_state:
    st.session_state.booking_json = None
if "processing" not in st.session_state:
    st.session_state.processing = False
if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

# Header
st.markdown("""
<div class="main-header">
    <h1>🤖 Kanishka Software Appointment Assistant</h1>
    <p>I'm your AI-powered assistant. Tell me who you'd like to meet and I'll help you book an appointment.</p>
</div>
""", unsafe_allow_html=True)

# Main chat container
chat_container = st.container()

with chat_container:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display chat messages
    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>👤 You:</strong><br>
                {msg['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>🤖 Assistant:</strong><br>
                {msg['content']}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Success message for booking
if st.session_state.booking_json:
    st.markdown("""
    <div class="success-box">
        <h3>✅ Appointment Booked Successfully!</h3>
        <p>Your appointment has been confirmed. Here are the details:</p>
    </div>
    """, unsafe_allow_html=True)
    st.json(st.session_state.booking_json)

# Input section
st.markdown('<div class="input-container">', unsafe_allow_html=True)

col1, col2, col3 = st.columns([4, 1, 1])

with col1:
    # Use a unique key that changes when we want to clear the input
    input_key = "user_input" if not st.session_state.clear_input else f"user_input_{int(time.time())}"
    user_input = st.text_input(
        "Type your message here...",
        key=input_key,
        placeholder="Tell me who you'd like to meet...",
        disabled=st.session_state.processing,
        on_change=None,
        help=""
    )
    
    # Reset the clear_input flag after the input is rendered
    if st.session_state.clear_input:
        st.session_state.clear_input = False

with col2:
    send_button = st.button(
        "Send",
        key="send_button",
        disabled=st.session_state.processing or not user_input.strip()
    )

with col3:
    if st.button("Clear Chat", key="clear_button"):
        st.session_state.messages = []
        st.session_state.state = None
        st.session_state.confirmed = False
        st.session_state.booking_json = None
        st.session_state.processing = False
        st.session_state.clear_input = True
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Add JavaScript for Enter key support
st.markdown("""
<script>
    // Function to handle Enter key press
    function handleEnterKey(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            // Find and click the send button
            const sendButton = document.querySelector('button[kind="primary"]');
            if (sendButton && !sendButton.disabled) {
                sendButton.click();
            }
        }
    }
    
    // Add event listener to text input
    document.addEventListener('DOMContentLoaded', function() {
        const textInput = document.querySelector('input[data-testid="stTextInput"]');
        if (textInput) {
            textInput.addEventListener('keydown', handleEnterKey);
        }
    });
    
    // Re-attach event listener after Streamlit reruns
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                const textInput = document.querySelector('input[data-testid="stTextInput"]');
                if (textInput && !textInput.hasAttribute('data-enter-handler')) {
                    textInput.setAttribute('data-enter-handler', 'true');
                    textInput.addEventListener('keydown', handleEnterKey);
                }
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
</script>
""", unsafe_allow_html=True)

# Process user input
if send_button and user_input.strip() and not st.session_state.processing:
    # Set processing state
    st.session_state.processing = True
    
    # Store the message content before clearing
    message_content = user_input.strip()
    
    # Clear the input field by changing the key
    st.session_state.clear_input = True
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": message_content})
    
    # Check for confirmation
    if (len(st.session_state.messages) >= 2 and 
        st.session_state.messages[-2]["content"].lower().endswith("type yes to confirm") and 
        message_content.lower() in {"yes", "haan", "ho", "chalega", "done", "ok", "okay", "yup", "sure", "si", "oui", "да", "はい", "evet", "correct", "confirm"}):
        st.session_state.confirmed = True
    
    # Get assistant response
    try:
        with st.spinner("🤖 Assistant is thinking..."):
            assistant_response, st.session_state.state, booking_json, ask_confirm = run_assistant(
                st.session_state.messages, st.session_state.state, st.session_state.confirmed
            )
        
        # Add assistant response
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        
        # Handle booking completion
        if booking_json:
            st.session_state.booking_json = booking_json
            st.session_state.processing = False
            st.rerun()
        
        st.session_state.confirmed = ask_confirm
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.session_state.messages.append({"role": "assistant", "content": "I apologize, but I encountered an error. Please try again."})
    
    finally:
        st.session_state.processing = False
        st.rerun()

# Auto-scroll to bottom
st.markdown("""
<script>
    window.scrollTo(0, document.body.scrollHeight);
</script>
""", unsafe_allow_html=True) 