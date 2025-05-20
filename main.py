from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage

from tools.wikipedia_tool import search_wikipedia
from tools.tavily_tool import get_tavily
from tools.math_tool import math_tool
from prompts.prompt_template import prompt_template
from config.settings import GOOGLE_API_KEY

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', temperature=0)

tools = [search_wikipedia, get_tavily, math_tool]

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent = create_structured_chat_agent(llm=llm, tools=tools, prompt=prompt_template)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True
)

# CLI loop
if __name__ == "__main__":
    print("SmartScholar is ready. Type 'exit' to quit.")
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break

        memory.chat_memory.add_message(HumanMessage(content=user_input))
        response = agent_executor.invoke({"input": user_input})
        print(response["output"])
        memory.chat_memory.add_message(AIMessage(content=response["output"]))
