# Persona-Adaptive Support Agent

A Streamlit-based AI agent that detects customer personas (Technical, Executive, Frustrated), adapts its response tone, and handles ticket escalation for angry users.

## Live Demo
You can try the running application here:
https://persona-adaptive-support-agent-nha4xtxmzvrymhyshzncqh.streamlit.app/

## Features
* **Persona Detection:** Classifies users as Technical Experts, Business Executives, or Frustrated Users.
* **Tone Adaptation:** Adjusts responses automatically (e.g., JSON logs for devs, ROI data for execs).
* **Smart Escalation:** Triggers a handoff ticket if the user is hostile.
* **Dynamic Model Selection:** Automatically finds the best available Google Gemini model.

## Tech Stack
* Python 3.8+
* Streamlit (Frontend)
* Google Gemini API (LLM Logic)

## Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/your-username/ai-support-agent.git](https://github.com/your-username/ai-support-agent.git)
    cd ai-support-agent
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure API Key**
    Create a `.env` file in the root folder and add your Google Gemini key:
    ```ini
    GOOGLE_API_KEY=AIzaSy...YourKeyHere...
    ```

## Usage

Run the application locally:
```bash
streamlit run app.py
