from langchain.memory import ConversationBufferMemory
from langchain.agents.conversational_chat.base import ConversationalChatAgent
from langchain.agents.structured_chat.base import StructuredChatAgent
from langchain.agents.structured_chat.output_parser import StructuredChatOutputParser
from langchain.agents import AgentExecutor, AgentOutputParser
from langchain.chat_models import ChatOpenAI
import Tool.mail_tool as my_tools
from langchain.schema.messages import HumanMessage, SystemMessage,AIMessage
import CustomOutputParser

SYSTEM_MESSAGE_PREFIX = """尽可能用中文回答以下问题。您可以使用以下工具"""

# 初始化大模型实例，可以是本地部署的，也可是是ChatGPT
# llm = ChatGLM(endpoint_url="http://你本地的实例地址")
llm = ChatOpenAI(openai_api_base="http://region-9.seetacloud.com:25540/v1",openai_api_key="none",temperature=0.8)
# 初始化工具
tools = [my_tools.SaveAddressBookTool(),my_tools.QueryAddressBookTool()]
# 初始化对话存储，保存上下文
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
# 配置agent
chat_agent = StructuredChatAgent.from_llm_and_tools(
    # prefix=SYSTEM_MESSAGE_PREFIX, # 指定提示词前缀
    llm=llm, tools=tools,
    verbose=True, # 是否打印调试日志，方便查看每个环节执行情况
    output_parser=StructuredChatOutputParser()#
)
agent = AgentExecutor.from_agent_and_tools(
    agent=chat_agent, tools=tools,  verbose=True,
    max_iterations=3 # 设置大模型循环最大次数，防止无限循环
)
# messages = [
#     HumanMessage(content="把张念驰,保存通讯录"),
#     AIMessage(content="请提供张念驰的邮箱地址"),
#     HumanMessage(content="231279478@qq.com"),
# ]

messages = [
    HumanMessage(content="查询张念驰的邮箱地址")
]
# agent.run("把张念驰,保存通讯录")
# agent.run("邮箱号是231279478@qq.com")

agent.invoke({'input':messages})


