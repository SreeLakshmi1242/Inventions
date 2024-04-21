# import required libraries 
import streamlit as st

from langchain.chat_models import ChatOpenAI
from langchain.schema import(
AIMessage,
HumanMessage,
SystemMessage
)

# Title of the application
st.set_page_config(page_title="LangChain Demo", page_icon=":robot:")
st.header("Let's chat")

# Set a default sessionMessages
if 'sessionMessages' not in st.session_state:
    st.session_state.sessionMessages = [
        SystemMessage(content = 'You are a kind assistant')
    ]

# Function to give answers to questions asked
def load_answer(question):
    st.session_state.sessionMessages.append(HumanMessage(content=question))
    assistant_answer = chat(st.session_state.sessionMessages)
    st.session_state.sessionMessages.append(AIMessage(content=assistant_answer.content))
    return assistant_answer.content

    
# Function to receive input from user
def get_text():
    input_text = st.text_input("You: ", key="input")
    return input_text

# Model
chat = ChatOpenAI(temperature=0.7)

user_input=get_text()

submit = st.button('Generate')  

#If generate button is clicked
if submit:
    response = load_answer(user_input)
    st.subheader("Answer:")

    st.write(response,key=1)
