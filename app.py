from dotenv import load_dotenv
import os  
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from tools import *
import streamlit as st


# Load .env file
load_dotenv()

# Access environment variables
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key=GOOGLE_API_KEY)
agent = initialize_agent(tools, llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION)

# Streamlit UI
st.title("LangChain Tool Calling Project")
st.markdown("Interact with Calculator and Weather tools powered by Gemini API.")

# User input
user_input = st.text_input("Enter your query:", placeholder="Example: Sqaure of 5  or  Weather in Lahore ")

if st.button("Submit"):
    if user_input.strip():
        try:
            response = agent.run(user_input)
            st.success(f"Response: {response}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a valid query.")

# Footer
st.markdown("---")
st.markdown("**Built with LangChain,Google's Gemini API and Streamlit**")
