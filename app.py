import streamlit as st
import google.generativeai as genai
import os
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
API_KEY = os.getenv("GOOGLE_API_KEY")

def configure_genai():
    """Configures the AI client and returns a valid model instance."""
    if not API_KEY:
        return None, "Error: API Key not found. Please check your .env file."

    try:
        genai.configure(api_key=API_KEY)
        
        # Dynamic Model Selection
        available_models = [
            m.name for m in genai.list_models() 
            if 'generateContent' in m.supported_generation_methods
        ]

        if not available_models:
            return None, "Error: No compatible AI models found."

        # Priority list
        target_model = None
        priority_order = [
            'models/gemini-1.5-flash',
            'models/gemini-1.5-flash-latest',
            'models/gemini-pro',
            'models/gemini-1.0-pro'
        ]

        for model in priority_order:
            if model in available_models:
                target_model = model
                break
        
        if not target_model:
            target_model = available_models[0]

        return genai.GenerativeModel(target_model), None

    except Exception as e:
        return None, f"Configuration Error: {str(e)}"

def get_agent_response(model, user_input):
    """Generates the response using the system prompt."""
    try:
        system_prompt = """
        You are a Customer Support Agent.
        
        Knowledge Base:
        - Rate Limits: 1000 requests per minute.
        - Billing: Invoices generated on the 1st of the month.
        - Service Status: US-East-1 is currently experiencing outages.
        
        Instructions:
        1. Analyze the user's Persona (Technical, Frustrated, or Executive).
        2. Adapt your tone accordingly.
        3. ESCALATION RULE: 
           If the user is angry, rude, or asks for a human, you must escalate.
           Output the response in this exact format:
           
           [ESCALATE] <A polite, reassuring message confirming you are transferring them to a supervisor.>
           
           Example: [ESCALATE] I apologize for the trouble. I am opening a priority ticket for you right now.
        """
        
        full_prompt = f"{system_prompt}\n\nUser Query: {user_input}"
        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        return f"Generation Error: {str(e)}"

# --- Streamlit UI Setup ---
st.set_page_config(page_title="Support Agent", layout="centered")
st.title("Persona-Adaptive Support Agent")
st.markdown("System Status: Online | Model: Adaptive")

# Initialize the AI Model
model, error_msg = configure_genai()

if error_msg:
    st.error(error_msg)
    st.stop()

# Chat Session Management
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display History
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])
        
        # If this message was an escalation, show the ticket info
        if chat.get("is_escalated"):
            st.warning(f"System: Ticket #{chat['ticket_id']} created. Transferred to Human Agent.")

# Input Handling
if user_query := st.chat_input("Type your support request here..."):
    # 1. Display User Message
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.chat_history.append({"role": "user", "content": user_query})

    # 2. Generate and Display AI Response
    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            raw_response = get_agent_response(model, user_query)
            
            # 3. Check for Escalation Flag
            is_escalated = False
            ticket_id = None
            final_text = raw_response

            if "[ESCALATE]" in raw_response:
                is_escalated = True
                ticket_id = random.randint(10000, 99999)
                # Remove the flag so the user just sees the polite text
                final_text = raw_response.replace("[ESCALATE]", "").strip()

            st.markdown(final_text)
            
            if is_escalated:
                st.warning(f"System: Ticket #{ticket_id} created. Transferred to Human Agent.")
    
    # Save to history with extra metadata for escalations
    st.session_state.chat_history.append({
        "role": "assistant", 
        "content": final_text,
        "is_escalated": is_escalated,
        "ticket_id": ticket_id
    })