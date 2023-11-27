from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from Tool.mail_tool import SendMailTool,EmailAddressTool
from langchain.chat_models import ChatOpenAI
import os
os.environ["SERPAPI_API_KEY"] = '9333902da63642ef782fd41fb732587cbb22abf913554dbc7f4f2273345a50f9'
os.environ["OPENAI_API_KEY"] = 'none'
os.environ["OPENAI_API_BASE"] = 'http://region-9.seetacloud.com:25540/v1'


llm = ChatOpenAI(verbose=True)
tools = load_tools(["serpapi", "llm-math"], llm=llm)
tools.append(EmailAddressTool())
tools.append(SendMailTool())
# 工具加载后都需要初始化，verbose 参数为 True，会打印全部的执行详情
agent = initialize_agent(tools, llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# 执行代理
print(agent.run("帮我查询下以巴冲突的最新消息"))
