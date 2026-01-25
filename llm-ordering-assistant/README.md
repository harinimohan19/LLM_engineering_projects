## Introduction
This project is a Streamlit-based conversational application that integrates an LLM (i.e. OpenAI Chat Completions API) to power a stateful chat experience.

## Key technical components
### LLM Integration
- Uses OpenAI Chat Completions API
- Model: gpt-4o-mini
- Conversation handled through a structured messages list with roles (system, user, assistant)
- Deterministic-style responses via low temperature (i.e. 0.2)

### Prompt Engineering
- A system prompt defines assistant behavior and constraints
- User UI actions are converted into structured natural-language prompts before being sent to the LLM

### Frontend/UI: Built with Streamlit
- Chat-style interface using st.chat_message and st.chat_input
- Interactive sidebar widgets (multiselect, radio, button)
- Dynamic UI updates using st.session_state and st.rerun()

### State Management
- Persistent conversation history stored in st.session_state.messages
- Structured data stored separately in st.session_state.order
- Enables synchronization between UI selections and LLM conversation

## Steps to Reproduce
1. Clone the repository: 
```
git clone https://github.com/harinimohan19/LLM_engineering_projects.git
cd .\LLM_engineering_projects\
cd .\llm-ordering-assistant\
```

2. Create a Virtual Environment
```
python -m venv my_env
source venv/bin/activate      # macOS/Linux
.\my_env\Scripts\activate         # Windows
```

3. Install Dependencies
```
pip install streamlit openai python-dotenv
```

4. Set Your OpenAI API Key
Create a .env File in the root directory of the project (same folder as app.py) and add your OpenAI API key
```
OPENAI_API_KEY=your_openai_api_key_here
```

5. Run the Application
```
streamlit run app.py
```
Open the Streamlit will start a local server. Open the provided URL in terminal.