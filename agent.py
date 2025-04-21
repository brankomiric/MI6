# import os
from langchain_ollama import ChatOllama
# from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.tools import tool

from ip import get_caller_ip

llm = ChatOllama(
    model="llama3.2",
    temperature=0.1,
)

# llm = ChatOpenAI(
#     model="gpt-4o-mini",
#     temperature=0.1,
#     openai_api_key=os.getenv("OPENAI_API_KEY"),
#     streaming=True,
#     verbose=True,
#     max_tokens=100,
# )

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a helpful assistant. Respond in 20 words or fewer.
            If the user asks about their IP address, use the get_machine_ip tool. Otherwise, answer the question directly.""",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

store = {}

@tool
def get_machine_ip():
    """Returns IPv4 address."""
    return get_caller_ip()

toolkit = [get_machine_ip]

agent = create_tool_calling_agent(llm, toolkit, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=toolkit,
    verbose=True,
)

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

with_message_history = RunnableWithMessageHistory(
        agent_executor,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
)

def ask_ollama_stream(prompt, session_id):
    return with_message_history.stream({"input": prompt}, config={"configurable": {"session_id": session_id}})

def ask_ollama(prompt, session_id):
    return with_message_history.invoke({"input": prompt}, config={"configurable": {"session_id": session_id}})
