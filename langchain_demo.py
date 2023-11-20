from qwen_llm import QwenLLM
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import ChatGLM
from ChatGLM3 import ChatGLM3
from Tool.mail_tool import SendMailTool
import os
os.environ["SERPAPI_API_KEY"] = '9333902da63642ef782fd41fb732587cbb22abf913554dbc7f4f2273345a50f9'

llm = QwenLLM()
tools = load_tools(["serpapi", "llm-math"], llm=llm)
#tools.append(SendMailTool())
# 工具加载后都需要初始化，verbose 参数为 True，会打印全部的执行详情
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# 执行代理
print(agent.run("我帮查询巴以冲突的最新进展"))
