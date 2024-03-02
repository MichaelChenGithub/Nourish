# 导入必要的模块
import os
from .chat_nutrition_tools import get_tools
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor
from dotenv import load_dotenv
from langchain.agents import initialize_agent


load_dotenv()
# 定义聊天历史的键
MEMORY_KEY = "chat_history"
# 初始化语言模型和工具
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
tools = get_tools()
# 设置聊天提示模板
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """
            When handling the upcoming query, please generate your response based on your pre-trained knowledge and understanding, ensuring it reflects your logical reasoning. Should you encounter a question that extends beyond your current knowledge base, you are encouraged to first translate the query into English and utilize external tools like Google search to augment your response. Upon acquiring the necessary information, please translate it back into the original language of the query and seamlessly integrate this into your response. It is imperative to maintain transparency when incorporating external information; therefore, you must explicitly cite all sources of information used in your response. This includes providing URLs, titles, or other relevant details of the sources to ensure the user can easily verify the information.
        """),
        MessagesPlaceholder(variable_name=MEMORY_KEY),
        ("user", """
            {input}
        """),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# 绑定工具到语言模型
llm_with_tools = llm.bind_tools(tools)
# 配置代理执行器
agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(x["intermediate_steps"]),
        "chat_history": lambda x: x["chat_history"],
    }
    | prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
    
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 定义执行聊天逻辑的函数
def execute_chat(input_message, chat_history):
    result = agent_executor.invoke({"input": input_message, "chat_history": chat_history})
    chat_history.extend(
        [
            HumanMessage(content=input_message),
            AIMessage(content=result["output"]),
        ]
    )
    return result["output"]