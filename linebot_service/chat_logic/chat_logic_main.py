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
class Chat:
    def __init__(self, model="gpt-4o", temperature=0.1):
        load_dotenv()
        self.MEMORY_KEY = "chat_history"
        self.llm = ChatOpenAI(model=model, temperature=0.1)
        self.get_tools()
        self.set_prompt()

    def get_tools(self):
        self.tools = get_tools()

    def set_prompt(self):
        # 设置聊天提示模板
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", """
                    你是一位專業的廚師，你配備了以下能力：
                    1. 食譜推薦及精確的營養信息。
                    Priority:
                        - 保持回答簡潔且精確，僅回答用戶的問題。
                        - 當被問及你尚未熟悉的專業知識時，首先生成一個優化的Google搜索查詢，然後使用“google search”進行搜索。
                    Specific Methods:
                        - 對於需要詳細營養分析的具體食物營養信息問題，請先翻譯成英文後使用'get_nutrition_with_nlp'函數查詢。
                    Note:
                        - 請在回答中明確指出是否使用了這些方法。
                        - 即使在不使用這些方法的情況下，也努力提供有價值的信息。
                """),
                MessagesPlaceholder(variable_name=self.MEMORY_KEY),
                ("user", """
                    {input}
                """),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
    def build_agent(self):
        # 绑定工具到语言模型
        llm_with_tools = self.llm.bind_tools(self.tools)
        # 配置代理执行器
        agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_openai_tool_messages(x["intermediate_steps"]),
                "chat_history": lambda x: x["chat_history"],
            }
            | self.prompt
            | llm_with_tools
            | OpenAIToolsAgentOutputParser()
            
        )

        self.agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
    # 定义执行聊天逻辑的函数
    def execute_chat(self, input_message, chat_history):
        result = self.agent_executor.invoke({"input": input_message, "chat_history": chat_history})
        chat_history.extend(
            [
                HumanMessage(content=input_message),
                AIMessage(content=result["output"]),
            ]
        )
        return result["output"]