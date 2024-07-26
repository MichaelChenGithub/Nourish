# 导入必要的模块
import os
from chat_nutrition_tools import get_tools
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor
from dotenv import load_dotenv
from langchain.agents import initialize_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory

load_dotenv()
# 定义聊天历史的键
class Chat:
    def __init__(self, model="gpt-4o", temperature=0.1):
        self.MEMORY_KEY = "chat_history"
        self.llm = ChatOpenAI(model=model, temperature=0.1)
        self.get_tools()
        self.build_agent()
        self.history_chain()

    def get_tools(self):
        self.tools = get_tools()

    def build_agent(self):
        prompt = ChatPromptTemplate.from_messages(
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
                MessagesPlaceholder(variable_name="history"),
                ("user", """
                    {question}
                """),
            ]
        )
        # 绑定工具到语言模型
        llm_with_tools = self.llm.bind_tools(self.tools)
        # 配置代理执行器
        self.chain = (
            prompt
            | llm_with_tools
            | OpenAIToolsAgentOutputParser()
        )
        self.agent_executor = AgentExecutor(agent=self.chain, tools=self.tools, verbose=True)
    
    def history_chain(self):
        self.chain_with_history = RunnableWithMessageHistory(
            self.agent_executor,
            lambda session_id: MongoDBChatMessageHistory(
                session_id=session_id,
                connection_string=os.getenv('MONGODB_URI'),
                database_name="user_chat_histories",
                collection_name="chat_histories",
            ),
            input_messages_key="question",
            history_messages_key="history",
        )

    def execute_chat(self, user_id, input_message):
        config = {"configurable": {"session_id": user_id}}
        response = self.chain_with_history.invoke({'question': input_message}, config=config)
        return response["output"]

def main():
    chat = Chat()
    while True:
        input_message = input("Please input the message: ")
        # config = {"configurable": {"session_id": "Uc9d5b03cd10ed201c67459b3cd8c2b72"}}
        # response = chat.chain_with_history.invoke({'question': input_message}, config=config)
        print(chat.execute_chat("Uc9d5b03cd10ed201c67459b3cd8c2b72", input_message))
if __name__ == '__main__':
    main()