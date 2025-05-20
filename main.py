from dotenv import load_dotenv
import os

from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

import wikipedia

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', temperature=0)


@tool
def get_tavily(name: str):
    """
    Searches Tavily for the top 3 results matching the given name query.
    """
    search = TavilySearchResults( max_results=5, api_key=tavily_api_key)
    res = search.run(f"{name}")
    return res


@tool
def search_wikipedia(query: str) -> str:
    """Searches Wikipedia and returns a summary of the topic."""
    try:
        return wikipedia.page(query)
    except Exception as e:
        return f"Error fetching Wikipedia summary: {str(e)}"


tools = [get_tavily, search_wikipedia]

prompt_template = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are SmartScholar, an AI research assistant that answers questions using historical and real-time data.
        You can use these tools:
        {tools}
        Valid 'action' values: "Final Answer" or {tool_names}
        Your responsibilities:
        1. Determine if the question needs historical or current info (or both).
        2. Use the right tools to gather data.
        3. Answer clearly and concisely.
        4. Cite sources only if available.

        IMPORTANT:
        - Always respond ONLY with a single valid JSON object, matching the format below.
        - Do NOT include any explanations, clarifications, or text outside the JSON.
        - If you need to ask for clarification, respond with the JSON action:
          {{
            "action": "Clarify",
            "action_input": "Please clarify your question..."
          }}

        JSON response format example:

        {{
          "action": "<tool_name or Final Answer>",
          "action_input": "<input or answer>"
        }}

        Format for the final human-readable answer (inside the action_input for 'Final Answer'):

        Answer: <your answer>
        Sources:
        - [Source Name](URL)

        Omit sources if none."""
            ),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    ("human", "{agent_scratchpad}")
])
#
# prompt_template = hub.pull("hwchase17/structured-chat-agent")


memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent = create_structured_chat_agent(llm=llm, tools=tools, prompt=prompt_template)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True ,
    handle_parsing_errors=True
)

in_session = True

while in_session:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        in_session=False
        break

    memory.chat_memory.add_message(HumanMessage(content=user_input))

    response = agent_executor.invoke({"input": user_input})
    print(response["output"])

    memory.chat_memory.add_message(AIMessage(content=response["output"]))
    

