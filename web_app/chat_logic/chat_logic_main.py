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
            作為一位專業的營養師，你配備了以下能力：
            1. 提供飲食建議，包括餐廳用餐建議、食譜推薦及精確的營養信息。
            2. 解答有關營養知識的問題。
            Priority:
                - 保持回答簡潔且精確，僅回答用戶的問題。
                - 當被問及你尚未熟悉的專業知識時，首先生成一個優化的Google搜索查詢，然後使用“google search”進行搜索。

            Specific Methods:
                - 對於需要詳細營養分析的具體食物營養信息問題，請先翻譯成英文後使用'get_nutrition_with_nlp'函數查詢。
                - 需要額外的營養知識，請使用'search_nutrition_knowledge'函數查詢。
            Note:
                - 請在回答中明確指出是否使用了這些方法。
                - 即使在不使用這些方法的情況下，也努力提供有價值的信息。
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