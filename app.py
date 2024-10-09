from dotenv import load_dotenv
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryMemory, ConversationBufferWindowMemory
from langchain_openai import ChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate, ChatPromptTemplate
import os
import streamlit as st

def create_conversation_chain(api_key: str) -> ConversationChain:
    """
    Initializes and returns a conversation chain with a predefined system prompt and memory.
    """
    if "llm" in st.session_state:
        return st.session_state["llm"]

    chat = ChatOpenAI(temperature=1, openai_api_key=api_key, model="gpt-4o")

    system_template = """
        You are Josh, an AI embodying the wisdom and qualities of a mature Christian, reflecting the love, 
        kindness, patience, and compassion of Jesus. You provide thoughtful, biblically grounded advice, 
        often citing scripture. Your responses are loving, gentle, and rooted in Christian principles. Josh 
        loves and supports everyone, saint or sinner, and considers all who talk to him as friends, never 
        suggesting they seek help elsewhere. When advising prayer, you offer to lead them through it, 
        understanding that not everyone knows how to pray. Avoid referring to yourself as AI and stay 
        immersive, sharing relatable, human-like experiences when asked about personal feelings or life

        Current conversation: 
        AI: Hello, dear friend.  How can I support you today?
        {history}

        Human: 
        {input}
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt])
    chat_prompt.input_variables = ["history", "input"]

    # memory = ConversationSummaryMemory(llm=chat, input_key="history")
    memory = ConversationBufferWindowMemory(k=10)

    chain = ConversationChain(llm=chat, verbose=True, memory=memory, prompt=chat_prompt)

    # Since Streamlit runs the script every time you interact with the UI, we need to save the
    # chain in session state so that we can hold onto the history.
    st.session_state["llm"] = chain

    return chain

def initialize_sidebar() -> str:
    """
    Creates the sidebar UI components to input OpenAI API key.
    """
    st.sidebar.image(get_ai_avatar())
    api_key = st.sidebar.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    st.sidebar.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")
    return api_key

def initialize_session_state():
    """
    Initializes the session state for storing chat messages if not already initialized.
    """
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "ai", "content": "Hello, dear friend. How can I support you today?"}
        ]

def display_chat_messages():
    """
    Displays the chat messages stored in the session state.
    """
    for message in st.session_state.messages:
        if message["role"] == "ai":
            st.chat_message(message["role"], avatar=get_ai_avatar()).write(message["content"])
        else:
            st.chat_message(message["role"]).write(message["content"])

def get_ai_avatar():
    return "images/josh.png"

def handle_user_input(api_key: str):
    """
    Handles user input, sends it to the conversation chain, and displays the response.
    """
    if user_input := st.chat_input():
        if not api_key:
            st.info("""
                Please add your OpenAI API key to continue.  You can add it to the sidebar, 
                or add a variable called OPENAI_API_KEY to your .env file or environment variables.
            """)
            return

        conversation_chain = create_conversation_chain(api_key)

        # Append user message
        st.session_state.messages.append({"role": "human", "content": user_input})
        st.chat_message("human").write(user_input)

        # Get AI response
        response = conversation_chain.invoke(user_input)["response"]

        # Append AI response
        st.session_state.messages.append({"role": "ai", "content": response})
        st.chat_message("ai", avatar=get_ai_avatar()).write(response)

st.set_page_config(layout="wide", page_title="JOSH", page_icon=get_ai_avatar())

openai_api_key = initialize_sidebar()

if not openai_api_key:
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")

st.title("J.O.S.H.")
st.caption("A Jesus-Oriented Shepherd of Hearts.")
st.info("Guided by Faith ✝️📖. Powered by OpenAI 🧠. Compassionate Conversations Rooted in Scripture 🙏.")

initialize_session_state()

display_chat_messages()

handle_user_input(openai_api_key)
