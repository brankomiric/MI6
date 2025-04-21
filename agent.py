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
from geo_data import get_geo_data_for_ip
from weather import weather_forecast_for_location

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
            If the user asks about their IP address, use the get_machine_ip tool. 
            If the user asks about their Geo data, use the get_geo_data tool. Use the ip address from the get_machine_ip tool. 
            If the user asks about the weather prognosis, use the get_weather tool. Use the city name from the get_geo_data tool. Pick only most relevant data from the response for each day.
            Otherwise, answer the question directly.""",
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

@tool
def get_geo_data(ip_address: str):
    """Returns geo data for the given IP address."""
    return get_geo_data_for_ip(ip_address)

@tool
def get_weather(location: str):
    """Returns weather forecast for the given location."""
    return weather_forecast_for_location(location)

toolkit = [get_machine_ip, get_geo_data, get_weather]

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
